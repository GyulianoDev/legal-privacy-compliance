import argparse
import ast
import hashlib
import re
from pathlib import Path

from common import SKILL_ROOT, load_json, main_guard


def validate(root):
    errors = []
    entry = root / 'SKILL.md'
    if not entry.is_file():
        return ['SKILL.md is missing.']
    text = entry.read_text(encoding='utf-8')
    match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
    if not match:
        errors.append('Missing YAML frontmatter boundary.')
    else:
        fields = dict(re.findall(r'^(name|description):\s*(.+)$', match[1], re.M))
        if fields.get('name') != root.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', fields.get('name', '')):
            errors.append('Skill name must match its directory and use lowercase kebab-case.')
        if not 1 <= len(fields.get('description', '')) <= 1024:
            errors.append('Description must contain 1-1024 characters.')
    if len(text.splitlines()) > 500:
        errors.append('Entry point is too large; move conditional guidance to references.')
    for file in root.rglob('*'):
        if file.is_symlink() or getattr(file.lstat(), 'st_file_attributes', 0) & 0x400:
            errors.append(f'Unexpected link: {file.relative_to(root)}')
            continue
        if not file.is_file():
            continue
        relative = file.relative_to(root).as_posix()
        if file.suffix == '.py':
            try:
                ast.parse(file.read_text(encoding='utf-8'), filename=relative)
            except SyntaxError as error:
                errors.append(f'{relative}: {error}')
        if file.suffix == '.json':
            try:
                load_json(file)
            except ValueError as error:
                errors.append(f'{relative}: {error}')
        if file.suffix == '.md':
            for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', file.read_text(encoding='utf-8')):
                if target.startswith(('http:', 'https:', '#', 'mailto:')):
                    continue
                path = (file.parent / target.split('#')[0]).resolve()
                if not path.is_relative_to(root.resolve()) or not path.exists():
                    errors.append(f'{relative}: missing or external local link {target}')
    try:
        catalog = load_json(root / 'references/pdfs/catalog.json')
        if len(catalog) != 5 or len({item['id'] for item in catalog}) != len(catalog):
            errors.append('Expected five uniquely identified reference PDFs.')
        for item in catalog:
            file = root / 'references/pdfs' / item['file']
            if file.parent.resolve() != (root / 'references/pdfs').resolve():
                errors.append('Catalog path escapes the library.')
            elif hashlib.sha256(file.read_bytes()).hexdigest() != item['sha256']:
                errors.append(f"PDF checksum mismatch: {item['id']}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f'Invalid PDF library: {error}')
    for name in ('project-profile', 'data-inventory', 'legal-document', 'generation-brief'):
        if not (root / 'schemas' / f'{name}.schema.json').is_file():
            errors.append(f'Missing schema: {name}')
    return errors


def main():
    parser = argparse.ArgumentParser(description='Check package resources, Python syntax, JSON, local links, frontmatter shape and PDF integrity. Not a legal or agent-runtime validator.')
    parser.add_argument('skill', nargs='?', default=str(SKILL_ROOT))
    args = parser.parse_args()
    errors = validate(Path(args.skill).resolve())
    if errors:
        for error in errors:
            print(f'FAIL: {error}')
        return 1
    print('Package checks passed: entry point, resources, syntax, JSON and five PDF hashes.')
    print('Use the Agent Skills validator for full YAML/spec validation and test discovery in each agent separately.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main_guard(main))
