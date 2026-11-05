# Compatibility and discovery

Official documentation consulted on **2026-11-05**. The shared core is a single `legal-privacy-compliance` directory with `SKILL.md`; there are no three divergent copies or proprietary wrappers needed to run scripts. Only `agents/openai.yaml` adds optional Codex metadata.

| Agent | Project | User global | Manual activation |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/legal-privacy-compliance/` | `~/.claude/skills/legal-privacy-compliance/` | `/legal-privacy-compliance` |
| Codex | `.agents/skills/legal-privacy-compliance/` | `~/.agents/skills/legal-privacy-compliance/` | `$legal-privacy-compliance`; `/skills` selector depending on client |
| Google Antigravity | `.agents/skills/legal-privacy-compliance/` | `~/.gemini/config/skills/legal-privacy-compliance/` | App/CLI: `/legal-privacy-compliance`; IDE: check Customizations |

Antigravity also documents legacy paths such as project `.agent/skills` and IDE `~/.gemini/antigravity/skills`. The installer uses current shared paths; it does not install duplicates in legacy directories. Claude and Codex do not automatically inherit each other's client-specific directories.

In all three products, description-based discovery supports activation by intent when enabled in the client; it does not guarantee activation for every message. Restart/reload the session or use the client's refresh mechanism after installation. For Antigravity CLI, check `/skills reload` in the installed version. Selector syntax and availability may vary by surface/version.

## Practical acceptance check for each client

1. Install in a test folder using the README command, with the complete library.
2. Start a new session in that project root and confirm discovery of the name/description.
3. Manually invoke `INVENTORY` on a fictional project; check access to scripts and `read-pdf.py --list` using the installed path.
4. In another session, naturally request a policy audit without naming the skill; observe whether the client selects it.
5. Check that it does not execute the app, read `.env`, publish or invent identity; inspect reports and unresolved questions.
6. Record client, version, OS, invocation, permissions, results and failures. Correct discovery does not prove legal quality.

**Delivery status:** format, scripts and local installation tested; no complete session of Claude Code, installed Codex or Antigravity was started as a discovery/execution test. macOS/Linux and PDF/DOCX rendering were not exercised either. Do not confuse official documentation and folder copying with these tests.

Primary sources: [Agent Skills](https://agentskills.io/specification), [Claude Code Skills](https://code.claude.com/docs/en/skills), [Codex Skills](https://developers.openai.com/codex/skills/), [Google Antigravity Skills](https://antigravity.google/docs/skills).
