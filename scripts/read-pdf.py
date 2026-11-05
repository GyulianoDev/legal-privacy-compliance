import argparse
import hashlib
import json
from pathlib import Path

from common import SKILL_ROOT, load_json, main_guard


def main():
    parser = argparse.ArgumentParser(description='Read selected pages from a bundled reference PDF, with edition and hash provenance.')
    parser.add_argument('--id', help='Catalog identifier; omit with --list.')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--pages', default='1', help='One-based physical PDF pages, such as 1,4-7.')
    parser.add_argument('--out', help='New local text file; otherwise print selected pages.')
    args = parser.parse_args()
    catalog = load_json(SKILL_ROOT / 'references/pdfs/catalog.json')
    if args.list:
        print(json.dumps(catalog, ensure_ascii=False, indent=2))
        return
    entry = next((item for item in catalog if item['id'] == args.id), None)
    if not entry:
        raise ValueError('Choose a valid --id using --list.')
    file = SKILL_ROOT / 'references/pdfs' / entry['file']
    if hashlib.sha256(file.read_bytes()).hexdigest() != entry['sha256']:
        raise ValueError('PDF checksum mismatch; update provenance before using this file.')
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ValueError('PDF extraction requires pypdf: python -m pip install pypdf. A PDF-capable agent may read the bundled file directly instead.') from None
    reader = PdfReader(file)
    selected = set()
    for part in args.pages.split(','):
        bounds = part.split('-')
        if len(bounds) > 2:
            raise ValueError('Invalid page range.')
        start = int(bounds[0])
        end = int(bounds[-1])
        if start < 1 or end < start or end > len(reader.pages):
            raise ValueError('Page range exceeds the PDF.')
        selected.update(range(start, end + 1))
    text = f"{entry['title']}\nEdition: {entry['edition']}\nSHA-256: {entry['sha256']}\nRole: {entry['role']}\n\n"
    for number in sorted(selected):
        extracted = reader.pages[number - 1].extract_text() or ''
        text += f'## PDF page {number}\n{extracted}\n\n'
        if not extracted.strip():
            text += 'REQUIRES_HUMAN_REVIEW: empty extraction; use visual inspection or authorized OCR.\n'
    if args.out:
        target = Path(args.out)
        if target.exists():
            raise ValueError('Output already exists.')
        target.write_text(text, encoding='utf-8')
        print(f'Extracted {len(selected)} pages to {target}. Local references need currency checks.')
    else:
        print(text)


if __name__ == '__main__':
    main_guard(main)
