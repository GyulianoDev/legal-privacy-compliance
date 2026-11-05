import argparse
import re
from datetime import date
from pathlib import Path

from common import REVIEW, load_json, main_guard, new_output, timestamp, write_json

DOCUMENTS = {'terms-of-service', 'privacy-policy', 'cookie-policy', 'ai-policy', 'acceptable-use',
             'data-deletion', 'data-processing-agreement', 'consent-notice', 'incident-response'}
MODES = {'FULL': DOCUMENTS, 'TOS': {'terms-of-service'}, 'PRIVACY': {'privacy-policy'},
         'COOKIES': {'cookie-policy', 'consent-notice'}, 'AI': {'ai-policy', 'acceptable-use'}}
LABELS = {
    'pt-BR': ('Versão', 'Atualizado em', 'RASCUNHO PARA REVISÃO', 'Identificação e contato', 'Fontes', 'Pendências'),
    'en': ('Version', 'Updated', 'DRAFT FOR REVIEW', 'Identity and contact', 'Sources', 'Pending review'),
    'es': ('Versión', 'Actualizado', 'BORRADOR PARA REVISIÓN', 'Identificación y contacto', 'Fuentes', 'Pendientes'),
}


def render_document(brief, document, references):
    language = brief.get('language', 'pt-BR')
    labels = LABELS[language]
    identity = brief.get('identity', {})
    pending = list(brief.get('pending', [])) + list(document.get('pending', []))
    for field in ('legal_name', 'privacy_contact'):
        if not identity.get(field):
            pending.append(f'{REVIEW}: identity.{field}')
    sections = document.get('sections', [])
    if not sections:
        pending.append(f'{REVIEW}: document sections not drafted')
    source_ids = document.get('source_ids', [])
    if not source_ids:
        pending.append(f'{REVIEW}: no verified legal sources attached')
    for source_id in source_ids:
        if source_id not in references or references[source_id].get('status') != 'verified':
            pending.append(f'{REVIEW}: unverified source {source_id}')
        source = references.get(source_id, {})
        try:
            consulted = date.fromisoformat(source.get('consulted_at', ''))
            if consulted > date.today():
                raise ValueError('Future consultation date.')
        except (TypeError, ValueError):
            pending.append(f'{REVIEW}: invalid consultation date for {source_id}')
        if not re.match(r'^https://', source.get('url', '')) or not source.get('articles') or not source.get('applicability'):
            pending.append(f'{REVIEW}: incomplete source context for {source_id}')
    if not document.get('evidence_ids'):
        pending.append(f'{REVIEW}: no supporting project evidence attached')
    lines = [f"# {document.get('title') or document['type']}", '',
             f"{brief['product']} | {labels[0]}: {brief['version']} | {labels[1]}: {brief['updated_at']}", '',
             f"> {labels[2]}. {REVIEW}. Not approved for publication.", '', f'## {labels[3]}', '',
             f"{identity.get('legal_name') or REVIEW} | {identity.get('privacy_contact') or REVIEW}", '']
    for section in sections:
        if not isinstance(section.get('heading'), str) or not isinstance(section.get('body'), str):
            raise ValueError('Each section requires string heading and body.')
        lines += [f"## {section['heading']}", '', section['body'], '']
        if not section['body'].strip() or REVIEW in section['body'] or re.search(r'\{\{.*?\}\}', section['body']):
            pending.append(f"{REVIEW}: incomplete section {section['heading']}")
    lines += [f'## {labels[4]}', '']
    for source_id in source_ids:
        source = references.get(source_id, {})
        lines += [f"- [{source.get('title', source_id)}]({source.get('url', '')}) - {source.get('articles', '')}; consulted {source.get('consulted_at', REVIEW)}."]
    if pending:
        lines += ['', f'## {labels[5]}', ''] + [f'- {item}' for item in sorted(set(pending))]
    metadata = {'type': document['type'], 'title': document.get('title') or document['type'],
                'product': brief['product'], 'version': brief['version'], 'updated_at': brief['updated_at'],
                'language': language, 'status': 'draft', 'audience': 'internal' if document['type'] == 'incident-response' else 'public_draft',
                'source_ids': source_ids, 'evidence_ids': document.get('evidence_ids', []),
                'pending': sorted(set(pending)), 'publishable': False}
    return '\n'.join(lines) + '\n', metadata


def main():
    parser = argparse.ArgumentParser(description='Materialize agent-authored, evidence-backed sections into review drafts. Does not perform legal reasoning.')
    parser.add_argument('--brief', required=True)
    parser.add_argument('--sources', required=True, help='JSON array of researched sources, not an unverified seed registry.')
    parser.add_argument('--out', required=True)
    parser.add_argument('--mode', choices=MODES, default='FULL')
    args = parser.parse_args()
    brief = load_json(args.brief)
    source_items = load_json(args.sources)
    if not isinstance(brief, dict) or not isinstance(source_items, list):
        raise ValueError('Brief must be an object and sources must be an array.')
    if any(not isinstance(item, dict) or not isinstance(item.get('id'), str) for item in source_items):
        raise ValueError('Each source requires a string id.')
    references = {item['id']: item for item in source_items}
    if len(references) != len(source_items):
        raise ValueError('Duplicate source ids.')
    if brief.get('language', 'pt-BR') not in LABELS:
        raise ValueError('Supported languages: pt-BR, en, es.')
    for field in ('product', 'version', 'updated_at', 'documents'):
        if not brief.get(field):
            raise ValueError(f'Missing brief field: {field}')
    date.fromisoformat(brief['updated_at'])
    for field in ('product', 'version'):
        if not isinstance(brief[field], str) or '\n' in brief[field]:
            raise ValueError(f'{field} must be a single-line string.')
    if not isinstance(brief['documents'], list) or any(not isinstance(item, dict) for item in brief['documents']):
        raise ValueError('Documents must be an array of objects.')
    results = []
    seen = set()
    for document in brief['documents']:
        kind = document.get('type')
        if kind not in DOCUMENTS:
            raise ValueError(f'Unsupported document type: {kind}')
        if kind in seen:
            raise ValueError(f'Duplicate document type: {kind}')
        seen.add(kind)
        if kind not in MODES[args.mode] or document.get('applicable') is not True:
            continue
        if not document.get('applicability_reason'):
            raise ValueError('Applicable documents require an applicability reason.')
        results.append((kind, *render_document(brief, document, references)))
    if not results:
        raise ValueError('No explicitly applicable documents selected. Complete applicability analysis first.')
    out = new_output(args.out)
    for kind, text, metadata in results:
        (out / f'{kind}.md').write_text(text, encoding='utf-8')
        write_json(out / f'{kind}.json', metadata)
    write_json(out / 'metadata.json', {'schema_version': '1.0', 'generated_at': timestamp(), 'mode': args.mode,
        'product': brief['product'], 'version': brief['version'], 'status': 'draft', 'publishable': False,
        'documents': [item[0] for item in results]})
    write_json(out / 'legal-sources.json', list(references.values()))
    pending = sorted({item for _, _, metadata in results for item in metadata['pending']})
    (out / 'missing-information.md').write_text('# Pending human review\n\n' + '\n'.join(f'- {item}' for item in pending) + '\n', encoding='utf-8')
    print(f'Generated {len(results)} local drafts; {len(pending)} pending items. Publication is not authorized by generation.')


if __name__ == '__main__':
    main_guard(main)
