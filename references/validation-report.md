# Delivery 1.0.0 checks

Executed on **2026-11-05**, Windows, Python **3.14.6**. Scripts require 3.10+, but other versions and operating systems were not exercised.

| Check | Observed result |
| --- | --- |
| Environment's `skill-creator/scripts/quick_validate.py` | `Skill is valid!` |
| `scripts/validate-skill.py` | Entry point, syntax, links, JSON, resources and five hashes passed |
| `unittest discover -s tests -v` with jsonschema installed | 26 tests: 25 passed, 1 skipped, no failures |
| Ten fictional scenarios | Expected indicators identified; none presented as confirmed production use |
| Four schemas | Valid Draft 2020-12 definitions; profiles/inventories from all ten scenarios and brief/metadata validated |
| Audit CLI | IP, analytics and AI contradictions found with file/line evidence; return 2 for the deliberately incorrect scenario |
| Generation CLI | Draft created, unresolved questions preserved, second execution at the same destination refused |
| HTML/JSON export | Active content escaped; draft state preserved; overwriting refused |
| Local installation test | Self-contained copy in discovery directories; five PDFs present; installed script read its own catalog |
| Original and bundled PDFs | Five matching hashes; originals preserved; 40, 49, 11, 15 and 52 pages respectively |
| Portable CLI extraction | Cookies pp. 28–29; Senate pp. 4–5; Defense pp. 9–11; gov.br pp. 13–15; public sector pp. 30–31, with nonempty output |

The skipped test attempts real symlink creation: the Windows account lacked the required privilege. The implementation skips symlinks/reparse points, but real-link creation did not verify that behavior in this environment.

Tests verify technical behavior and invariants, not a legal opinion's correctness or document approval. No discovery/automatic-activation test or complete session was run in Claude Code, Codex or Antigravity applications; paths were compared with official documentation and local copying was exercised. See the [per-client protocol](../adapters/compatibility.md).

No Linux/macOS, PDF/DOCX export, public-route integration, production inspection or complete legal/linguistic coverage testing. Tests did not install the skill globally or publish through package scripts. Subsequent repository preparation preserves paths and implementation across `ptbr` and `en`, translating Markdown files and explanatory comments. Original PDFs, JSON examples and interface metadata are shared.
