import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from scan_project import scan


def module(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), SCRIPTS / f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


audit = module('verify-consistency').audit
generate = module('generate-documents')
export = module('export-documents')


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)

    def cli(self, script, *args):
        env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run([sys.executable, '-X', 'utf8', str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True, encoding='utf-8', env=env)

    def fixture(self, name):
        return scan(ROOT / 'tests/fixtures' / name)

    def test_ten_product_scenarios(self):
        expected = {
            'landing': set(), 'analytics': {'google-analytics', 'local-storage'},
            'commerce': {'stripe', 'email', 'address', 'subscriptions'}, 'mobile': {'firebase', 'push', 'authentication'},
            'saas': {'multi-tenant', 'employees'}, 'ai': {'openai', 'uploads', 'messages', 'vector-store'},
            'minors': {'children'}, 'international': {'international'},
            'incomplete': {'openai', 'stripe', 'email'}, 'incorrect-policies': {'ip-address', 'openai', 'google-analytics'},
        }
        for name, signals in expected.items():
            with self.subTest(name=name):
                profile, inventory = self.fixture(name)
                actual = {item['signal'] for item in profile['findings']}
                if name == 'landing':
                    self.assertFalse(actual)
                else:
                    self.assertTrue(signals <= actual, signals - actual)
                self.assertTrue(all(not item['production_verified'] for item in profile['findings']))
                self.assertTrue(all(item['proposed_legal_basis'] is None for item in inventory['operations']))

    def test_unimplemented_dependencies_are_not_active_operations(self):
        profile, inventory = self.fixture('incomplete')
        self.assertFalse(any(item['context'] == 'code_reference' for item in profile['findings']))
        self.assertFalse(any(item['confidence'] == 'high' for item in profile['findings']))
        findings = audit(profile, inventory, {'privacy.md': 'Version: 1.0\nWe do not use AI. We do not share with third parties.'})
        self.assertFalse(any(item['severity'] == 'HIGH' for item in findings['findings']))

    def test_test_data_is_not_added_to_inventory(self):
        (self.work / 'tests').mkdir()
        (self.work / 'tests/test_data.py').write_text('email = "demo@example.invalid"', encoding='utf-8')
        profile, inventory = scan(self.work)
        self.assertEqual(profile['findings'][0]['context'], 'test_or_example')
        self.assertEqual(inventory['operations'], [])

    def test_comments_do_not_activate_integrations(self):
        (self.work / 'app.js').write_text('// openai\n/* gtag("config") */\nconst url = "https://example.invalid";', encoding='utf-8')
        (self.work / 'app.py').write_text('# stripe\nvalue = "https://example.invalid"\n', encoding='utf-8')
        self.assertEqual(scan(self.work)[0]['findings'], [])

    def test_secret_files_and_source_values_are_withheld(self):
        canary = 'PRIVATE_CANARY_NOT_A_REAL_CREDENTIAL'
        (self.work / '.env').write_text(f'OPENAI_KEY={canary}', encoding='utf-8')
        (self.work / 'credentials.json').write_text(json.dumps({'openai': canary}), encoding='utf-8')
        (self.work / 'app.py').write_text(f'email = "{canary}"\n', encoding='utf-8')
        profile, inventory = scan(self.work)
        serialized = json.dumps([profile, inventory])
        self.assertNotIn(canary, serialized)
        self.assertEqual(profile['files_scanned'], 1)
        self.assertEqual(profile['findings'][0]['line'], 1)

    def test_generated_directories_are_excluded(self):
        (self.work / 'node_modules').mkdir()
        (self.work / 'node_modules/vendor.js').write_text('openai; stripe; gtag();', encoding='utf-8')
        self.assertEqual(scan(self.work)[0]['files_scanned'], 0)

    def test_oversized_files_are_excluded(self):
        (self.work / 'large.js').write_text('openai;' + ' ' * 512001, encoding='utf-8')
        self.assertEqual(scan(self.work)[0]['files_scanned'], 0)

    def test_symlink_sources_are_not_followed(self):
        source = self.work / 'outside.js'
        source.write_text('openai;', encoding='utf-8')
        project = self.work / 'project'
        project.mkdir()
        try:
            (project / 'link.js').symlink_to(source)
        except OSError:
            self.skipTest('Symlink creation is unavailable under this Windows account.')
        self.assertEqual(scan(project)[0]['files_scanned'], 0)

    def test_invalid_configuration_does_not_echo_content(self):
        (self.work / 'package.json').write_text('{PRIVATE_CANARY', encoding='utf-8')
        profile, _ = scan(self.work)
        self.assertFalse(profile['configuration_checks'][0]['valid'])
        self.assertNotIn('PRIVATE_CANARY', json.dumps(profile))

    def test_local_storage_is_not_automatically_consent_based(self):
        (self.work / 'app.js').write_text('localStorage.setItem("theme", "dark");', encoding='utf-8')
        result = self.cli('detect-trackers.py', self.work, '--out', self.work / 'trackers.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads((self.work / 'trackers.json').read_text(encoding='utf-8'))
        self.assertIn('local-storage', json.dumps(value))
        self.assertNotIn('"consent_required": true', json.dumps(value))

    def test_policy_contradictions_have_evidence_and_internal_classification(self):
        profile, inventory = self.fixture('incorrect-policies')
        policy = (ROOT / 'tests/fixtures/incorrect-policies/policies/privacy-policy.md').read_text(encoding='utf-8')
        report = audit(profile, inventory, {'privacy-policy.md': policy})
        contradictions = [item for item in report['findings'] if item['rule'].endswith('denial')]
        self.assertEqual({item['rule'] for item in contradictions}, {'ip-denial', 'ai-denial', 'tracking-denial'})
        self.assertTrue(all(item['evidence'] and item['document']['line'] > 0 for item in contradictions))
        self.assertTrue(all(item['classification'] == 'internal_triage_not_anpd' for item in contradictions))
        self.assertFalse(report['legal_compliance_verified'])

    def test_noncontradictory_policy_does_not_produce_denial(self):
        profile, inventory = self.fixture('analytics')
        report = audit(profile, inventory, {'privacy.md': 'Version: 1.0\nAnalytics indicators need confirmation.'})
        self.assertFalse(any(item['rule'].endswith('denial') for item in report['findings']))

    def test_cli_audit_returns_two_for_high_severity(self):
        source = ROOT / 'tests/fixtures/incorrect-policies'
        discovery = self.work / 'scan'
        self.assertEqual(self.cli('scan-project.py', source, '--out', discovery).returncode, 0)
        result = self.cli('verify-consistency.py', '--profile', discovery / 'project-profile.json', '--inventory', discovery / 'data-inventory.json', '--policies', source / 'policies', '--out', self.work / 'audit.json')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue((self.work / 'audit.json').is_file())

    def test_generated_drafts_remain_blocked_with_missing_identity_and_sources(self):
        brief = json.loads((ROOT / 'examples/reviewed-brief.json').read_text(encoding='utf-8'))
        text, metadata = generate.render_document(brief, brief['documents'][0], {})
        self.assertFalse(metadata['publishable'])
        self.assertEqual(metadata['status'], 'draft')
        self.assertIn('REQUIRES_HUMAN_REVIEW', text)
        self.assertTrue(any('identity.legal_name' in item for item in metadata['pending']))

    def test_unverified_or_incomplete_source_stays_pending(self):
        brief = json.loads((ROOT / 'examples/reviewed-brief.json').read_text(encoding='utf-8'))
        document = dict(brief['documents'][0], source_ids=['fake'])
        _, metadata = generate.render_document(brief, document, {'fake': {'status': 'verified', 'url': 'https://example.invalid'}})
        self.assertTrue(any('invalid consultation date' in item for item in metadata['pending']))
        self.assertTrue(any('incomplete source context' in item for item in metadata['pending']))

    def test_generation_cli_and_no_overwrite(self):
        args = ['--brief', ROOT / 'examples/reviewed-brief.json', '--sources', ROOT / 'examples/researched-sources.json', '--out', self.work / 'drafts']
        result = self.cli('generate-documents.py', *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.work / 'drafts/privacy-policy.md').exists())
        self.assertNotEqual(self.cli('generate-documents.py', *args).returncode, 0)

    def test_generation_requires_explicit_applicability(self):
        brief = json.loads((ROOT / 'examples/reviewed-brief.json').read_text(encoding='utf-8'))
        brief['documents'][0]['applicable'] = False
        path = self.work / 'brief.json'
        path.write_text(json.dumps(brief), encoding='utf-8')
        result = self.cli('generate-documents.py', '--brief', path, '--sources', ROOT / 'examples/researched-sources.json', '--out', self.work / 'drafts')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.work / 'drafts').exists())

    def test_unknown_document_type_cannot_escape_output(self):
        brief = json.loads((ROOT / 'examples/reviewed-brief.json').read_text(encoding='utf-8'))
        brief['documents'][0]['type'] = '../outside'
        path = self.work / 'brief.json'
        path.write_text(json.dumps(brief), encoding='utf-8')
        result = self.cli('generate-documents.py', '--brief', path, '--sources', ROOT / 'examples/researched-sources.json', '--out', self.work / 'drafts')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.work / 'drafts').exists())

    def test_all_supported_languages_preserve_review_state(self):
        brief = json.loads((ROOT / 'examples/reviewed-brief.json').read_text(encoding='utf-8'))
        for language in ('pt-BR', 'en', 'es'):
            with self.subTest(language=language):
                text, metadata = generate.render_document(dict(brief, language=language), brief['documents'][0], {})
                self.assertEqual(metadata['language'], language)
                self.assertIn('REQUIRES_HUMAN_REVIEW', text)
                self.assertFalse(metadata['publishable'])

    def test_html_export_escapes_active_content(self):
        content = export.to_html('Demo', '# Draft\n<script>alert(1)</script>', 'en')
        self.assertNotIn('<script>', content)
        self.assertIn('&lt;script&gt;', content)
        self.assertIn('lang="en"', content)

    def test_export_renders_report_table_and_escapes_cells(self):
        content = export.to_html('Report', '| Signal | Evidence |\n| --- | --- |\n| openai | <script>bad</script> |')
        self.assertIn('<th>Signal</th>', content)
        self.assertIn('<td>openai</td>', content)
        self.assertNotIn('<script>', content)
        self.assertNotIn('<td>---</td>', content)

    def test_export_preserves_draft_and_refuses_overwrite(self):
        source = self.work / 'draft.md'
        source.write_text('# Draft\nREQUIRES_HUMAN_REVIEW', encoding='utf-8')
        target = self.work / 'draft.json'
        result = self.cli('export-documents.py', source, '--format', 'json', '--out', target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(target.read_text(encoding='utf-8'))['publication_approved'])
        self.assertNotEqual(self.cli('export-documents.py', source, '--format', 'json', '--out', target).returncode, 0)

    def test_project_installer_carries_library_and_refuses_existing_target(self):
        result = self.cli('install-skill.py', '--agent', 'codex', '--project', self.work)
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = self.work / '.agents/skills/legal-privacy-compliance'
        self.assertEqual(len(list((installed / 'references/pdfs').glob('*.pdf'))), 5)
        validation = self.cli('validate-skill.py', installed)
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
        self.assertNotEqual(self.cli('install-skill.py', '--agent', 'codex', '--project', self.work).returncode, 0)

    def test_installer_dry_run_does_not_create_files(self):
        result = self.cli('install-skill.py', '--agent', 'claude', '--project', self.work, '--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.work / '.claude').exists())

    def test_installed_copy_reads_its_own_catalog(self):
        result = self.cli('install-skill.py', '--agent', 'antigravity', '--project', self.work)
        self.assertEqual(result.returncode, 0, result.stderr)
        script = self.work / '.agents/skills/legal-privacy-compliance/scripts/read-pdf.py'
        result = subprocess.run([sys.executable, '-X', 'utf8', str(script), '--list'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 5)

    def test_schemas_accept_outputs_and_reject_publication_claim(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest('Install requirements-dev.txt for schema validation.')
        schemas = {}
        for file in (ROOT / 'schemas').glob('*.json'):
            value = json.loads(file.read_text(encoding='utf-8'))
            jsonschema.Draft202012Validator.check_schema(value)
            schemas[file.name] = jsonschema.Draft202012Validator(value, format_checker=jsonschema.FormatChecker())
        for fixture in (ROOT / 'tests/fixtures').iterdir():
            if fixture.is_dir():
                profile, inventory = scan(fixture)
                schemas['project-profile.schema.json'].validate(profile)
                schemas['data-inventory.schema.json'].validate(inventory)
        brief = json.loads((ROOT / 'examples/reviewed-brief.json').read_text(encoding='utf-8'))
        schemas['generation-brief.schema.json'].validate(brief)
        _, metadata = generate.render_document(brief, brief['documents'][0], {})
        schemas['legal-document.schema.json'].validate(metadata)
        with self.assertRaises(jsonschema.ValidationError):
            schemas['legal-document.schema.json'].validate(dict(metadata, publishable=True))


if __name__ == '__main__':
    unittest.main()
