# Legal Privacy Compliance

A skill for analyzing projects and preparing terms, policies and inventories with technical evidence, official research and explicit review questions. Supporting documentation is in Portuguese; scripts and filenames are in English.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-SKILL.md-5865F2?style=for-the-badge)
![Local](https://img.shields.io/badge/Execution-Local-17876D?style=for-the-badge)

---

## 📌 About the Project

The agent investigates the project, consults relevant PDFs, researches current legislation and writes the sections. Scripts support discovery, traceability, file generation and auditing. Regular expressions do not select legal bases or validate legal provisions.

The package includes the **five supplied PDFs**, with English filenames, hashes, editions and limits on their use. The gov.br and Ministry of Defense examples are institutional references, not ready-to-use SaaS terms. See the [library analysis](references/pdf-library.md).

---

## ✨ Features

- 🔎 Static discovery of frameworks, integrations and candidate data categories across several languages.
- 🧭 Distinguishes dependencies, configuration, code, schemas and tests; none is automatically presented as production use.
- 📝 Nine outlines for conditional documents, with Markdown and JSON metadata generation from an agent-authored brief.
- 🍪 Specific workflows for cookies, consent, AI, minors, SaaS and transfers.
- 📚 PDF lookup by page, with hashes and provenance, including after installation in another project.
- 🧪 Contradiction auditing, new outputs without overwriting and inventories with explicit unknown fields.

Agent modes: `FULL` (default), `TOS`, `PRIVACY`, `COOKIES`, `AI`, `AUDIT`, `UPDATE`, `CHECK`, `INVENTORY`, `EXPORT`. The generation CLI accepts `FULL/TOS/PRIVACY/COOKIES/AI`; the remaining modes are agent workflows using the relevant scripts. Document languages: `pt-BR`, `en`, `es`; translation does not determine jurisdiction.

---

## 🛠️ Technologies

| Technology | Purpose |
| --- | --- |
| Agent Skills / Markdown / YAML | Shared core and client discovery |
| Python 3.10+ and standard library | Scanner, auditing, generation, export and installation |
| JSON Schema 2020-12 | Contracts for profiles, inventories, briefs and metadata |
| pypdf, optional | Page extraction from the included PDFs |
| unittest / jsonschema | Functional tests and full schema validation |

---

## 🚀 Installation

You need Python 3.10+ and your chosen agent. Open a terminal in this folder, which contains `SKILL.md`. Commands use `python`; use `python3` on systems where that is the executable name.

To get the package from GitHub:

```sh
git clone --branch ptbr https://github.com/GyulianoDev/legal-privacy-compliance.git
cd legal-privacy-compliance
```

1. Check the destination with `--dry-run`.
2. Run without `--dry-run` to copy the entire folder, including PDFs.
3. Open/reload the client session and confirm discovery.

```sh
python scripts/install-skill.py --agent claude --project /path/to/project --dry-run
python scripts/install-skill.py --agent claude --project /path/to/project
python scripts/install-skill.py --agent codex --project /path/to/project
python scripts/install-skill.py --agent antigravity --project /path/to/project
```

Choose the client you need. Codex and Antigravity share the current `.agents/skills/` destination; one copy in that project is enough. The installer refuses existing destinations and does not update another installation automatically. In PowerShell, quote paths containing spaces:

```powershell
python scripts/install-skill.py --agent codex --project "C:\Projects\My App"
```

For global installation, when wanted:

```sh
python scripts/install-skill.py --agent claude --scope global
python scripts/install-skill.py --agent codex --scope global
python scripts/install-skill.py --agent antigravity --scope global
```

| Client | Project | Global |
| --- | --- | --- |
| Claude Code | `.claude/skills/legal-privacy-compliance/` | `~/.claude/skills/legal-privacy-compliance/` |
| Codex | `.agents/skills/legal-privacy-compliance/` | `~/.agents/skills/legal-privacy-compliance/` |
| Antigravity | `.agents/skills/legal-privacy-compliance/` | `~/.gemini/config/skills/legal-privacy-compliance/` |

Paths checked against official documentation on 2026-11-05: [Claude](https://code.claude.com/docs/en/skills), [Codex](https://developers.openai.com/codex/skills/), [Antigravity](https://antigravity.google/docs/skills), [Agent Skills standard](https://agentskills.io/specification). Surface differences, legacy directories and the validation protocol are documented in [compatibility](adapters/compatibility.md).

To extract PDF text with a script:

```sh
python -m pip install "pypdf>=6,<7"
python scripts/read-pdf.py --list
python scripts/read-pdf.py --id cookies --pages 28-36 --out cookie-excerpts.txt
```

An agent with a PDF reader can consult the files directly. The main scripts do not require a network connection, keys or external dependencies.

---

## ▶️ How to Use

In Claude Code or Antigravity App/CLI:

```text
/legal-privacy-compliance INVENTORY: analyze this project and list only facts, indicators and review questions.
```

In Codex:

```text
$legal-privacy-compliance FULL: prepare the applicable documents for this project.
```

For automatic discovery, when enabled in the client, ask naturally: “Check whether my privacy policy matches the code” or “My SaaS uses AI; analyze it and prepare applicable documents.” The description enables selection by intent; the client decides whether to activate the skill. Check the integration limitations below.

Running the local helpers:

```sh
python scripts/scan-project.py /path/to/project --out ../private-scan
python scripts/detect-trackers.py /path/to/project --out ../private-trackers.json
python scripts/generate-documents.py --brief examples/reviewed-brief.json --sources examples/researched-sources.json --out ../private-drafts
python scripts/verify-consistency.py --profile ../private-scan/project-profile.json --inventory ../private-scan/data-inventory.json --policies /path/to/policies --out ../private-audit.json
python scripts/export-documents.py ../private-drafts/privacy-policy.md --format html --out ../privacy-preview.html
```

Outputs must be new. The auditor returns `2` for `HIGH/CRITICAL` findings, `0` for other results and an error for invalid input. Zero does not certify compliance. The generator always keeps `status: draft` and `publishable: false`; there is no automatic approval shortcut. The example intentionally leaves sources empty and review questions visible.

The [workflows](workflows/document-generation.md) explain the brief, applicability matrix, research, questions, review and updates. The agent also delivers an internal report, dated sources, unresolved questions and a justified changelog. The incident procedure is internal.

HTML and JSON are local, opt-in exports. HTML renders headings, paragraphs, simple lists and tables without multiline cells, escaping content; it is not a complete Markdown renderer. PDF, DOCX, MDX, React and mobile screens require tools/implementation and authorization in the destination project; they are not available as automatic exports in this version.

---

## 📁 File Organization

```text
legal-privacy-compliance/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── agents/openai.yaml
├── adapters/compatibility.md
├── references/          # research, criteria and sources
│   └── pdfs/            # five PDFs and catalog.json
├── workflows/           # six procedures
├── templates/           # nine document outlines
├── scripts/             # commands and shared modules
├── schemas/             # four JSON Schema contracts
├── examples/            # fictional brief and empty sources
└── tests/fixtures/      # ten static scenarios
```

The repository keeps `ptbr` as its default branch and `en` for English READMEs and explanatory comments. Paths, implementation and PDFs are identical across both branches. The instructions and references were requested in Portuguese for this skill and remain shared. Switching languages does not create different filenames.

---

## 🧪 Tests

```sh
python scripts/validate-skill.py
python -m unittest discover -s tests -v
```

To include full schema validation and PDF extraction, use a virtual environment:

```sh
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` on Linux/macOS; then:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Tests cover the ten scenarios, false positives, withheld secrets, test/schema/dependency contexts, evidence-backed contradictions, unresolved questions, three languages, escaped exports, schemas, overwrite prevention and installation with the library. Schema tests are skipped when `jsonschema` is not installed; symlink creation may be skipped under Windows accounts without that privilege.

The local validator checks links, Python syntax, JSON and PDF integrity. For full frontmatter validation, the environment's official `skill-creator` skill's `quick_validate.py` was also used; that file is not a runtime dependency of this package.

Delivery result: **26 tests, 25 passed and 1 skipped** because of missing Windows symlink creation privileges. The four schemas, hashes and excerpt extraction from all five PDFs were checked. See the [validation report](references/validation-report.md) for the exact scope of testing.

---

## ⚠️ Security and Limitations

- Heuristic static analysis: no finding does not prove no processing. Up to 5,000 files and 512,000 bytes per file; no product execution or production capture. Language/configuration parsers are not complete.
- `.env`, files named for credentials/secrets, links and generated directories are skipped. This reduces exposure; it is not a universal secret detector. Reports contain indicators, paths/lines and hashes, without values or raw excerpts.
- Bases, purposes, retention, roles and regions need evidence and review. The historical library and initial research do not replace current official research for each project. Blocked sources remain unresolved.
- No script publishes, commits, accesses databases, executes applications or sends code. Keep reports outside served directories and review before sharing.
- The package does not replace a lawyer/data protection officer, guarantee compliance or approve documents for publication.
- Third-party PDFs retain attribution and do not receive the code's MIT license. Check permissions before public redistribution.
- Locally checked: Python scripts on Windows, fixtures, schemas, installation/copying and library integrity. Discovery and full execution in the three clients, macOS/Linux and PDF/DOCX exports **have not yet been validated**. The [protocol](adapters/compatibility.md) explains how to test them.

Useful next improvements: real discovery tests per client, configuration-specific parsers when a project needs them and export connectors with verified rendering. Expand only in response to an observed need.
