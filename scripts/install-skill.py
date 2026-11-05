import argparse
import shutil
from pathlib import Path

from common import SKILL_ROOT, main_guard

PROJECT_PATHS = {'claude': '.claude/skills', 'codex': '.agents/skills', 'antigravity': '.agents/skills'}
GLOBAL_PATHS = {'claude': '.claude/skills', 'codex': '.agents/skills', 'antigravity': '.gemini/config/skills'}


def main():
    parser = argparse.ArgumentParser(description='Copy the complete shared skill, including PDFs, into an official discovery directory. Never overwrites.')
    parser.add_argument('--agent', choices=PROJECT_PATHS, required=True)
    parser.add_argument('--scope', choices=['project', 'global'], default='project')
    parser.add_argument('--project', help='Required for project scope.')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.scope == 'project' and not args.project:
        raise ValueError('Project scope requires --project.')
    base = Path(args.project).resolve() if args.scope == 'project' else Path.home()
    if not base.is_dir():
        raise ValueError('The target project/home must already exist.')
    relative = PROJECT_PATHS[args.agent] if args.scope == 'project' else GLOBAL_PATHS[args.agent]
    target = base / relative / 'legal-privacy-compliance'
    for parent in (target, *target.parents):
        if parent == base.parent:
            break
        if parent.is_symlink() or (parent.exists() and getattr(parent.lstat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('Installation path contains a symbolic link or reparse point.')
    if target.exists() or target.is_symlink():
        raise ValueError(f'Target already exists: {target}. No files were changed.')
    if target.is_relative_to(SKILL_ROOT):
        raise ValueError('Cannot install the skill inside itself.')
    print(f'Install target: {target}')
    if args.dry_run:
        print('Dry run; no changes made.')
        return
    shutil.copytree(SKILL_ROOT, target, symlinks=False, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.cache', '.git', '.venv', '.tools', 'node_modules', 'legal-output'))
    print('Copied shared skill and PDF library. Verify discovery in the selected agent; this is not a runtime integration test.')


if __name__ == '__main__':
    main_guard(main)
