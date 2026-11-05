import argparse
from common import main_guard, new_output, write_json
from scan_project import scan, report


def main():
    parser = argparse.ArgumentParser(description='Inspect local source without executing it; output technical indicators, not legal conclusions.')
    parser.add_argument('project')
    parser.add_argument('--out', required=True, help='New local output directory; no overwrites.')
    args = parser.parse_args()
    profile, inventory = scan(args.project)
    out = new_output(args.out)
    write_json(out / 'project-profile.json', profile)
    write_json(out / 'data-inventory.json', inventory)
    (out / 'discovery-report.md').write_text(report(profile), encoding='utf-8')
    print(f"Scanned {profile['files_scanned']} files; {len(profile['findings'])} indicators. Status: {profile['status']}. Output: {out}")


if __name__ == '__main__':
    main_guard(main)
