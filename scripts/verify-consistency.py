import argparse
import re
from pathlib import Path

from common import REVIEW, load_json, main_guard, write_json


def audit(profile, inventory, policies):
    findings = []
    evidence = [item for item in profile['findings'] if item['context'] == 'code_reference']

    def add(rule, severity, problem, document, proof, recommendation):
        findings.append({'id': f'A{len(findings)+1:04}', 'rule': rule, 'severity': severity, 'problem': problem,
            'document': document, 'evidence': proof, 'potential_risk': 'A public statement may not match actual operations.',
            'recommendation': recommendation, 'requires_human_review': True,
            'classification': 'internal_triage_not_anpd', 'status': REVIEW})

    checks = [
        ('ip-denial', r'n[aã]o\s+(?:coletamos|registramos).*?(?:\bip\b|endere[cç]o ip)|do not (?:collect|log).*?\bip\b|no recopilamos.*?\bip\b', {'ip-address'}, 'HIGH'),
        ('tracking-denial', r'n[aã]o (?:usamos|utilizamos).*?(?:analytics|rastreadores|marketing)|no (?:analytics|tracking)|do not use.*?(?:analytics|tracking)', {'google-analytics', 'meta-pixel', 'tiktok-pixel', 'hotjar', 'clarity', 'google-tag-manager', 'google-ads'}, 'HIGH'),
        ('ai-denial', r'n[aã]o (?:usamos|utilizamos).*?(?:intelig[eê]ncia artificial|\bia\b)|do not use (?:ai|artificial intelligence)', {'openai', 'anthropic', 'gemini'}, 'HIGH'),
        ('third-party-denial', r'n[aã]o (?:compartilhamos|enviamos).*?terceiros|no third.parties|do not share.*?third.part', {'openai', 'anthropic', 'gemini', 'stripe', 'sentry', 'firebase', 'supabase'}, 'HIGH'),
    ]
    for name, text in policies.items():
        for rule, pattern, signals, severity in checks:
            match = re.search(pattern, text, re.I)
            proof = [{'file': item['file'], 'line': item['line'], 'signal': item['signal'], 'evidence_id': item['id']} for item in evidence if item['signal'] in signals]
            if match and proof:
                add(rule, severity, 'Potential contradiction between a categorical denial and source indicators.',
                    {'file': name, 'line': text.count('\n', 0, match.start()) + 1}, proof,
                    'Trace the live data flow and scope of the statement; revise the policy or implementation after confirmation.')
        for signal, pattern in [('uploads', r'upload|arquivo|file'), ('openai', r'openai'), ('stripe', r'stripe')]:
            proof = [{'file': item['file'], 'line': item['line'], 'signal': signal} for item in evidence if item['signal'] == signal]
            if proof and not re.search(pattern, text, re.I):
                add('possible-omission', 'MEDIUM', f'Possible omission of {signal}; document type and actual use need review.',
                    {'file': name, 'line': 1}, proof, 'Confirm applicability and explain relevant processing in the appropriate policy.')
        if REVIEW in text or re.search(r'\{\{.+?\}\}', text):
            add('unresolved-fields', 'HIGH', 'Unresolved review fields remain.', {'file': name, 'line': 1}, [], 'Resolve before publication.')
        if not re.search(r'\b(?:Version|Vers[aã]o|Versi[oó]n)\b', text, re.I):
            add('missing-version', 'LOW', 'No recognizable version marker.', {'file': name, 'line': 1}, [], 'Add version and update date.')
        if re.search(r'100%.*segur|compliance guaranteed|conformidade garantida|criptografia de ponta a ponta|end.to.end encrypt|nunca.*treinamento|never.*training|exclusivamente.*brasil|imediata.*exclus[aã]o', text, re.I):
            add('unsupported-promise', 'HIGH', 'A strong technical or legal promise needs independent evidence.', {'file': name, 'line': 1}, [], 'Verify the full architecture, provider terms and retention exceptions; do not infer from a keyword.')
    for operation in inventory.get('operations', []):
        missing = [key for key in ('purpose', 'proposed_legal_basis', 'retention', 'controller') if not operation.get(key)]
        if missing:
            add('incomplete-operation', 'MEDIUM', f"Operation {operation['id']} lacks {', '.join(missing)}.", None,
                [{'evidence_id': value} for value in operation.get('evidence_ids', [])], 'Confirm purpose, roles, basis and retention per operation.')
    return {'schema_version': '1.0', 'status': REVIEW, 'legal_compliance_verified': False,
            'findings': findings, 'limitations': ['Lexical checks can miss paraphrases, context and unsupported laws.', 'No runtime capture, legal-validity certification or production verification.']}


def main():
    parser = argparse.ArgumentParser(description='Flag demonstrable technical inconsistencies and review questions; not a legal opinion.')
    parser.add_argument('--profile', required=True)
    parser.add_argument('--inventory', required=True)
    parser.add_argument('--policies', required=True, help='Local directory containing Markdown policies.')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if Path(args.out).exists():
        raise ValueError('Output already exists.')
    directory = Path(args.policies)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('Policies must be a local directory, not a symlink.')
    policies = {file.name: file.read_text(encoding='utf-8') for file in directory.glob('*.md') if not file.is_symlink() and file.stat().st_size < 512000}
    if not policies:
        raise ValueError('No Markdown policies found.')
    result = audit(load_json(args.profile), load_json(args.inventory), policies)
    write_json(args.out, result)
    print(f"{len(result['findings'])} review findings. No legal compliance certification.")
    return 2 if any(item['severity'] in {'HIGH', 'CRITICAL'} for item in result['findings']) else 0


if __name__ == '__main__':
    raise SystemExit(main_guard(main))
