import argparse
import html
import json
import re
from pathlib import Path

from common import main_guard


def to_html(title, text, language='pt-BR'):
    blocks = []
    table = []
    items = []

    def flush():
        if table:
            header, *rows = table
            blocks.append('<table><thead><tr>' + ''.join(f'<th>{html.escape(cell)}</th>' for cell in header) + '</tr></thead><tbody>')
            for row in rows:
                blocks.append('<tr>' + ''.join(f'<td>{html.escape(cell)}</td>' for cell in row) + '</tr>')
            blocks.append('</tbody></table>')
            table.clear()
        if items:
            blocks.append('<ul>' + ''.join(f'<li>{html.escape(item)}</li>' for item in items) + '</ul>')
            items.clear()

    for line in text.splitlines():
        escaped = html.escape(line)
        if line.startswith('|') and line.rstrip().endswith('|'):
            if not re.fullmatch(r'[|:\s-]+', line):
                table.append([cell.strip() for cell in line.strip().strip('|').split('|')])
            continue
        if line.startswith('- '):
            if table:
                flush()
            items.append(line[2:])
            continue
        flush()
        if line.startswith('# '):
            blocks.append(f'<h1>{escaped[2:]}</h1>')
        elif line.startswith('## '):
            blocks.append(f'<h2>{escaped[3:]}</h2>')
        elif line.strip():
            blocks.append(f'<p>{escaped}</p>')
    flush()
    return '<!doctype html><html lang="' + html.escape(language) + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>' + html.escape(title) + '</title><style>body{font:16px/1.7 system-ui;max-width:960px;margin:50px auto;padding:0 28px;color:#e5edf5;background:#101926}h1{color:#70d6c6}h2{margin-top:36px}p{white-space:pre-wrap;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;margin:28px 0}th,td{text-align:left;padding:12px;border-bottom:1px solid #344252}th{color:#70d6c6;background:#192637}</style></head><body><main>' + '\n'.join(blocks) + '</main></body></html>'


def main():
    parser = argparse.ArgumentParser(description='Export a local Markdown artifact as escaped HTML or JSON; never publishes or executes embedded HTML.')
    parser.add_argument('input')
    parser.add_argument('--format', choices=['html', 'json'], required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--language', choices=['pt-BR', 'en', 'es'], default='pt-BR')
    args = parser.parse_args()
    target = Path(args.out)
    if target.exists():
        raise ValueError('Output already exists.')
    source = Path(args.input)
    text = source.read_text(encoding='utf-8')
    result = to_html(source.stem, text, args.language) if args.format == 'html' else json.dumps({'source': source.name, 'content': text, 'publication_approved': False}, ensure_ascii=False, indent=2)
    target.write_text(result, encoding='utf-8')
    print(f'Exported locally: {target}. Review status has not changed.')


if __name__ == '__main__':
    main_guard(main)
