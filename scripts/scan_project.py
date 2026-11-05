import hashlib
import io
import json
import os
import re
import tokenize
from pathlib import Path

from common import REVIEW, safe_name, timestamp

SKIP_DIRS = {".git", ".svn", ".hg", "node_modules", ".venv", "venv", "vendor", "dist", "build", ".next", ".tools", ".cache", "coverage", "legal-output", "__pycache__", ".aws", ".ssh", ".codex", ".agents", ".claude"}
SOURCE_SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".py", ".java", ".cs", ".csproj", ".php", ".go", ".rb", ".rs", ".c", ".h", ".swift", ".kt", ".kts", ".dart", ".vue", ".svelte", ".html", ".sql", ".prisma", ".json", ".toml", ".yaml", ".yml", ".xml", ".gradle"}
PROVIDERS = {
    "google-analytics": ("tracking", r"google-analytics|googletagmanager\.com/gtag|\bgtag\s*\("),
    "google-tag-manager": ("tracking", r"googletagmanager\.com/gtm|\bGTM-[A-Z0-9]+"),
    "meta-pixel": ("tracking", r"connect\.facebook\.net|\bfbq\s*\("),
    "tiktok-pixel": ("tracking", r"analytics\.tiktok\.com|\bttq\.(track|page)"),
    "google-ads": ("tracking", r"googleadservices|googlesyndication|\bAW-[0-9]+"),
    "hotjar": ("tracking", r"\bhotjar\b|static\.hotjar\.com"),
    "clarity": ("tracking", r"clarity\.ms|@microsoft/clarity"),
    "sentry": ("monitoring", r"@sentry/|sentry_sdk|sentry\.io"),
    "stripe": ("payment", r"\bstripe\b|stripe\.com"),
    "mercado-pago": ("payment", r"mercadopago|mercado-pago"),
    "paypal": ("payment", r"\bpaypal\b"),
    "openai": ("ai", r"\bopenai\b|api\.openai\.com"),
    "anthropic": ("ai", r"\banthropic\b|api\.anthropic\.com"),
    "gemini": ("ai", r"@google/genai|google\.genai|generativelanguage\.googleapis"),
    "firebase": ("cloud", r"\bfirebase\b|\bfirestore\b|\bFirebase(?:Auth|Firestore|Messaging|Storage)\b"),
    "supabase": ("cloud", r"\bsupabase\b"),
    "onesignal": ("push", r"\bonesignal\b"),
    "aws": ("cloud", r"@aws-sdk/|\bboto3\b|amazonaws\.com"),
    "azure": ("cloud", r"@azure/|azure\.storage|blob\.core\.windows\.net"),
    "google-cloud": ("cloud", r"@google-cloud/|google\.cloud"),
    "cloudflare": ("cloud", r"\bwrangler\b|@cloudflare/|cloudflare\.com"),
    "smtp": ("email", r"\bsmtplib\b|\bnodemailer\b|\bSMTPClient\b"),
    "postgresql": ("database", r"\bpsycopg\b|\bNpgsql\b|\bpostgres(?:ql)?\b"),
    "mysql": ("database", r"\bmysql\b|\bpymysql\b"),
    "mongodb": ("database", r"\bmongodb\b|\bmongoose\b|\bpymongo\b"),
    "redis": ("database", r"\bredis\b|\bioredis\b"),
    "sqlite": ("database", r"\bsqlite3?\b|better-sqlite3"),
}
SIGNALS = {
    "email": ("personal-data", r"\b(?:email|emailAddress|e_mail)\b"),
    "name": ("personal-data", r"\b(?:first_name|last_name|full_name|firstName|lastName|fullName)\b"),
    "phone": ("personal-data", r"\b(?:phone|phoneNumber|telefone)\b"),
    "tax-id": ("personal-data", r"\b(?:cpf|cnpj|taxId)\b"),
    "address": ("personal-data", r"\b(?:streetAddress|postalCode|shipping_address|deliveryAddress)\b"),
    "location": ("personal-data", r"\b(?:geolocation|latitude|longitude|ACCESS_FINE_LOCATION)\b"),
    "ip-address": ("personal-data", r"\b(?:remote_addr|REMOTE_ADDR|remoteAddress)\b|x-forwarded-for"),
    "device-id": ("personal-data", r"\b(?:deviceId|advertisingId|IDFA|ANDROID_ID)\b"),
    "uploads": ("feature", r"\b(?:multer|UploadFile|IFormFile|multipart/form-data)\b"),
    "messages": ("personal-data", r"\b(?:chat_history|conversationHistory|messageContent|promptHistory)\b"),
    "health": ("sensitive-candidate", r"\b(?:medicalRecord|healthData|diagnosis|bloodType)\b"),
    "biometrics": ("sensitive-candidate", r"\b(?:faceEmbedding|fingerprintTemplate|biometricData)\b"),
    "audio": ("personal-data", r"\b(?:MediaRecorder|microphone|audioFile)\b"),
    "children": ("context", r"\b(?:childAccount|parentalConsent|child_profile|kidsApp)\b"),
    "authentication": ("feature", r"\b(?:signInWith(?:EmailAndPassword|Credential|OAuth|Popup|Redirect)?|GoogleSignIn|GoogleAuthProvider|OAuth2|oauth|jwt|bcrypt|argon2|twoFactor|resetPassword|password_hash)\b"),
    "apple-sign-in": ("feature", r"\b(?:AppleAuthentication|ASAuthorizationAppleIDProvider)\b|apple-signin"),
    "cookies": ("storage", r"document\.cookie|Set-Cookie|\bset_cookie\b|res\.cookie\s*\("),
    "local-storage": ("storage", r"\blocalStorage\b"),
    "session-storage": ("storage", r"\bsessionStorage\b"),
    "indexed-db": ("storage", r"\bindexedDB\b"),
    "push": ("feature", r"\b(?:requestPermission|registerForRemoteNotifications|FirebaseMessaging)\b"),
    "multi-tenant": ("context", r"\b(?:tenantId|tenant_id|organizationId)\b"),
    "employees": ("context", r"\b(?:employeeId|employee_id|payroll)\b"),
    "subscriptions": ("feature", r"\b(?:subscriptionId|recurringPrice|subscription_id)\b"),
    "vector-store": ("ai", r"\b(?:embeddings|vectorStore|pgvector|chromadb|pinecone)\b"),
    "international": ("context", r"\b(?:targetCountries|servedCountries|operatingCountries)\b"),
}
FRAMEWORKS = {"react", "next", "vue", "nuxt", "svelte", "express", "django", "flask", "fastapi", "laravel", "spring", "flutter", "expo", "react-native", "aspnetcore"}


def is_link(path):
    if path.is_symlink():
        return True
    info = path.lstat()
    return bool(getattr(info, "st_file_attributes", 0) & 0x400)


def eligible_files(root, limit=5000):
    count = 0
    for folder, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS and not is_link(Path(folder) / name))
        for name in sorted(files):
            file = Path(folder) / name
            if is_link(file) or name.startswith('.env') or any(word in name.lower() for word in ("secret", "credential", "service-account", "service_account")):
                continue
            if file.suffix.lower() not in SOURCE_SUFFIXES and name not in {"requirements.txt", "Gemfile", "go.mod", "composer.json"}:
                continue
            if file.stat().st_size > 512000 or any(part in name for part in ('.min.', '.lock')):
                continue
            if count >= limit:
                return
            count += 1
            yield file


def strip_comments(text, suffix):
    if suffix == '.py':
        try:
            tokens = [token for token in tokenize.generate_tokens(io.StringIO(text).readline) if token.type != tokenize.COMMENT]
            return tokenize.untokenize(tokens)
        except (tokenize.TokenError, IndentationError):
            return text
    if suffix in {'.json', '.html', '.sql', '.toml', '.yaml', '.yml'}:
        if suffix == '.html':
            return re.sub(r'<!--[\s\S]*?-->', lambda m: '\n' * m[0].count('\n'), text)
        return text
    # preserve strings and lines; this only reduces noise, it doesn't prove execution.
    pattern = r'("(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|`(?:\\.|[^`\\])*`)|(/\*[\s\S]*?\*/|//[^\n]*)'
    return re.sub(pattern, lambda m: m[1] if m[1] else '\n' * m[0].count('\n'), text)


def scan(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Project root must be a directory.")
    findings = []
    frameworks = set()
    count = 0
    configs = []
    product = safe_name(root.name)
    for file in eligible_files(root):
        relative = file.relative_to(root).as_posix()
        try:
            text = file.read_text(encoding='utf-8-sig')
        except (UnicodeError, OSError):
            continue
        count += 1
        if file.name == 'package.json':
            try:
                manifest = json.loads(text)
                if file.parent == root and isinstance(manifest.get('name'), str):
                    product = safe_name(manifest['name'])
                dependencies = {**manifest.get('dependencies', {}), **manifest.get('devDependencies', {})}
                frameworks.update(name for name in FRAMEWORKS if name in dependencies)
            except (ValueError, TypeError, AttributeError):
                configs.append({'file': relative, 'valid': False, 'reason': 'Invalid package manifest; values withheld.'})
        elif file.suffix == '.json':
            try:
                json.loads(text)
            except ValueError:
                configs.append({'file': relative, 'valid': False, 'reason': 'Not strict JSON; may require JSONC or a framework parser.'})
        if any(part.lower() in {'tests', 'test', '__tests__', 'fixtures', 'examples', 'mocks'} for part in file.relative_to(root).parts) or re.search(r'\.(test|spec)\.', file.name):
            context = 'test_or_example'
        elif file.suffix in {'.sql', '.prisma'}:
            context = 'schema_only'
        elif file.name in {'package.json', 'requirements.txt', 'pyproject.toml', 'go.mod', 'composer.json', 'Gemfile', 'pom.xml', 'build.gradle', 'build.gradle.kts'} or file.suffix == '.csproj':
            context = 'dependency_declared'
        elif file.suffix in {'.json', '.yaml', '.yml', '.toml', '.xml'}:
            context = 'configuration_reference'
        else:
            context = 'code_reference'
        code = strip_comments(text, file.suffix)
        digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
        for key, (category, pattern) in {**PROVIDERS, **SIGNALS}.items():
            match = re.search(pattern, code, re.I)
            if not match:
                continue
            findings.append({'id': f'E{len(findings)+1:04}', 'signal': key, 'category': category, 'file': relative,
                             'line': code.count('\n', 0, match.start()) + 1, 'context': context,
                             'confidence': 'low' if context in {'dependency_declared', 'test_or_example', 'schema_only'} else 'medium',
                             'production_verified': False, 'file_sha256': digest,
                             'evidence': f'Matched known {category} identifier; source values withheld.'})
        for framework in FRAMEWORKS:
            if re.search(r'\b' + re.escape(framework) + r'\b', code, re.I):
                frameworks.add(framework)
    profile = {'schema_version': '1.0', 'product': product, 'scanned_at': timestamp(), 'files_scanned': count,
               'scope': 'static_source_only', 'frameworks': sorted(frameworks), 'findings': findings,
               'configuration_checks': configs, 'coverage': {'max_files': 5000, 'max_file_bytes': 512000,
               'limit_may_be_reached': count >= 5000, 'excluded': sorted(SKIP_DIRS), 'secrets_and_symlinks_skipped': True},
               'unknowns': ['legal_identity', 'privacy_contact', 'production_use', 'audience', 'jurisdictions', 'retention', 'storage_regions'],
               'status': REVIEW}
    operations = []
    for finding in findings:
        if finding['context'] == 'test_or_example' or finding['category'] not in {'personal-data', 'sensitive-candidate', 'tracking', 'ai', 'payment'}:
            continue
        operations.append({'id': f'OP{len(operations)+1:04}', 'category': finding['signal'], 'fields': [],
            'collection_source': None, 'purpose': None, 'subjects': [], 'controller': None, 'processor': None,
            'proposed_legal_basis': None, 'recipients': [], 'international_transfer': None, 'storage_location': None,
            'retention': None, 'deletion_mechanism': None, 'security_measures': [], 'evidence_ids': [finding['id']],
            'confidence': finding['confidence'], 'status': REVIEW, 'pending': ['Confirm actual operation, purpose, roles, basis and retention.']})
    inventory = {'schema_version': '1.0', 'product': product, 'operations': operations, 'status': REVIEW}
    return profile, inventory


def report(profile):
    lines = [f"# Static discovery: {profile['product']}", '', 'Status: REQUIRES_HUMAN_REVIEW', '',
             'Static indicators only. Production collection and legal applicability are unverified.', '',
             '| Signal | Context | File | Line |', '| --- | --- | --- | --- |']
    lines += [f"| {item['signal']} | {item['context']} | {item['file']} | {item['line']} |" for item in profile['findings']]
    lines += ['', 'Missing: ' + ', '.join(profile['unknowns']), '', 'No raw source lines, credentials or field values are included.']
    return '\n'.join(lines) + '\n'
