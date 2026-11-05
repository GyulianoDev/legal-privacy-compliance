# Drafting and applicability

| Document | Criterion for consideration |
| --- | --- |
| Terms | Service use relationship; scope obligations and contracting |
| Privacy | Confirmed or potential personal-data processing |
| Cookies | Cookies/similar technologies needing specific transparency |
| AI | Actual use of models, automation, RAG, agents or decisions |
| Acceptable use | Accounts, content, APIs, bots or abuse risk |
| Deletion/retention | Data lifecycle with relevant procedures |
| DPA | Processing on another controller's behalf within a contract |
| Consent | Specific purpose actually relying on consent |
| Incidents | Internal response procedure, not an automatic public policy |

Do not generate all documents by default: `FULL` covers all applicable ones, with
reasons for inclusion and exclusion. A static landing page does not gain
subscriptions, registration, a marketing banner or a DPA without evidence.
Consider employee/applicant notices, impact assessments (RIPD), processing records,
community policies and seller terms when relevant.

Templates are conditional outlines, not contracts needing only a name replacement.
Write verifiable details and cite relevant provisions. Clauses should explain
purpose, procedure and consequences without absolute promises or waiving rights.
Unknown bases, identity, contacts, retention or essential terms remain internal
review questions; do not deploy these drafts to a public page.

The `generate-documents.py` brief contains `product`, `version`, `updated_at`,
`language`, `identity`, `pending` and `documents`. Each document supplies `type`,
`title`, `applicable`, `applicability_reason`, `sections` (`heading`, `body`),
`source_ids`, `evidence_ids`, `pending`. See the [example](../examples/reviewed-brief.json).
The agent prepares this content after analysis; completing JSON does not confirm
facts or approve publication. Generated JSON files keep `publishable: false`.

Internal output in a new folder: Markdown documents/metadata, reviewed inventory,
report, missing information and sources. Maintain explicit links between
paragraph -> operation -> evidence -> provision. For EN/ES, translate meaning,
definitions and exceptions; language does not determine jurisdiction. Produce
components, MDX and routes only on an integration request; exporting is not publishing.
