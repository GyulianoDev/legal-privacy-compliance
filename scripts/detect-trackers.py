import argparse
from common import main_guard, write_json
from scan_project import scan


def main():
    parser = argparse.ArgumentParser(description='List tracking and browser storage indicators; does not claim consent is legally required.')
    parser.add_argument('project')
    parser.add_argument('--out', required=True, help='New JSON file.')
    args = parser.parse_args()
    from pathlib import Path
    if Path(args.out).exists():
        raise ValueError('Output already exists.')
    profile, _ = scan(args.project)
    findings = [item for item in profile['findings'] if item['category'] in {'tracking', 'storage'}]
    write_json(args.out, {'schema_version': '1.0', 'findings': findings, 'runtime_verified': False,
                         'consent_required': None, 'status': 'REQUIRES_HUMAN_REVIEW'})
    print(f'{len(findings)} storage/tracking indicators. Runtime and consent basis require review.')


if __name__ == '__main__':
    main_guard(main)
