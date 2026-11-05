# Legal research

Start with the [registry](../references/source-registry.md). For each material
conclusion, open the relevant official text and check provision, jurisdiction,
effective status, amendments and regulations. A blocked Planalto page does not
make a law inaccessible: consult the Chamber of Deputies, Senate, ANPD or Official
Gazette and record the substitute. Do not confuse original publication with
consolidated text, or a draft with an effective rule.

Create `legal-sources.json` as an array: `id`, `title`, `url`, `jurisdiction`, `kind`
(`law`, `regulation`, `guidance`, `proposal`, `practice`), `articles`, `consulted_at`,
`status` (`verified`, `needs_recheck`, `blocked`, `offline`), `applicability` and `notes`.
Use strings for `articles`, `applicability` and `notes`; `consulted_at` is `YYYY-MM-DD`.
The agent confirms sources during the session; an older date does not automatically
become today's date. Link sources and technical evidence to the supported section.

Read local PDFs by edition and physical page, checking printed numbering. Historical
PDFs support context and comparisons; they do not replace current legal research.
Public-agency examples are not authority for a private SaaS's practices. Do not
copy identities, contacts, sector-specific policies or venue clauses.

Without network access: deliver discovery and drafts, mark `OFFLINE_REFERENCE_ONLY`,
cite local editions and list exactly what needs updating. Do not invent provisions,
case law or effective status. For AI, do not claim no regulation exists merely
because initial research did not find a specific law.
