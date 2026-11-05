# Fictional Examples

`reviewed-brief.json` demonstrates the input format, not a legally approved case. Identity, legal bases and retention periods remain unresolved. `researched-sources.json` is intentionally empty: tests do not simulate official research that did not happen for a real product.

The ten small projects in `tests/fixtures/` are static test inputs, with snippets that must not be executed as applications. They cover landing pages, analytics, commerce, mobile, SaaS, AI, minors, international operations, dependencies without implementation and contradictory policies.

To try them, run from the skill root:

```sh
python scripts/scan-project.py tests/fixtures/incorrect-policies --out ../demo-scan
python scripts/verify-consistency.py --profile ../demo-scan/project-profile.json --inventory ../demo-scan/data-inventory.json --policies tests/fixtures/incorrect-policies/policies --out ../demo-audit.json
python scripts/generate-documents.py --brief examples/reviewed-brief.json --sources examples/researched-sources.json --out ../demo-drafts
```

The auditor returns **2** for this scenario because it finds high-priority contradictions. Generation creates only a draft privacy policy with unresolved questions; `FULL` does not force nine documents. Use new outputs when repeating these commands.
