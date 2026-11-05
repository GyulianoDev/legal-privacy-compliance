# Project discovery

Perform static reading before asking questions. Locate `AGENTS.md`, manifests,
models, routes, screens, integrations, infrastructure and existing policies. Do
not run project builds, installers, migrations or scripts to discover behavior.

The scanner accepts common languages and manifests, limits size/count, withholds
raw lines and ignores `.env*`, sensitive filenames, links and dependencies. These
filters do not guarantee that filenames or metadata contain no secrets: review
reports before sharing. Do not print configuration to search for tokens; use
variable names and services' public contracts.

For each integration, trace dependency -> configuration -> import -> call ->
environment and operational confirmation. A dependency does not prove use;
comments, fixtures, schemas and future screens do not prove collection. Describe
static-analysis limitations, unsupported languages and excluded/truncated files.

Investigate product, audience, jurisdictions, languages, channels, authentication,
uploads, charges, advertising, storage, logs, backups, deletion and third parties.
A legal entity's CNPJ is not automatically personal data; individual entrepreneurs,
MEI registrations and links to natural persons require context. An IP address
available to a server does not mean persistence; inspect app, proxy and hosting logs.

Output: profile and evidence identified by file, line, context, hash and confidence.
Before citing a line, confirm its position in the original file; scanner
preprocessing is no substitute for contextual reading.
