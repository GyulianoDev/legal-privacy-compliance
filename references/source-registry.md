# Sources and maintenance

Preparation research: **2026-11-05**. This registry does not replace current research for each project. It is a starting point with status/limits; do not convert it into verified sources for any product without fresh analysis.

Prioritize the official Planalto portal. During preparation, some pages blocked access; consolidated legislation from the Chamber of Deputies was the official alternative. The ANPD catalog and institutional pages alone do not confirm an act's full text or deadlines.

| Source | Official URL | Preparation status |
| --- | --- | --- |
| Consolidated LGPD | https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html | Text consulted; check amendments on each use. |
| Updated Internet Civil Framework | https://www2.camara.leg.br/legin/fed/lei/2014/lei-12965-23-abril-2014-778630-normaatualizada-pl.pdf | Text consulted. |
| Decree 8.771/2016 | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/d8771.htm | Access blocked; find an official alternative before citing provisions. |
| Consolidated Consumer Protection Code | https://www2.camara.leg.br/legin/fed/lei/1990/lei-8078-11-setembro-1990-365086-normaatualizada-pl.html | Text consulted. |
| Consolidated Civil Code | https://www2.camara.leg.br/legin/fed/lei/2002/lei-10406-10-janeiro-2002-432893-normaatualizada-pl.html | Text consulted. |
| Consolidated Child and Adolescent Statute | https://www2.camara.leg.br/legin/fed/lei/1990/lei-8069-13-julho-1990-372211-normaatualizada-pl.html | Text consulted. |
| Decree 7.962/2013 | https://www2.camara.leg.br/legin/fed/decret/2013/decreto-7962-15-marco-2013-775557-publicacaooriginal-139266-pe.html | Original publication consulted; check amendments. |
| ANPD regulations | https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd | Catalog consulted; verify each complete act. |
| Resolution 19/2024 | https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024 | Text and correction notice consulted. |
| Resolution 2/2022 | https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022 | Text consulted; check amendments. |
| ANPD materials | https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes | Location of guides and editions. |
| ANPD Digital ECA | https://www.gov.br/anpd/pt-br/assuntos/eca-digital | Current page consulted; open relevant acts/guidance for concrete use. |

For each project's research, create `legal-sources.json`: an array of `{id, title, url, jurisdiction, kind, articles, consulted_at, status, applicability, notes}`. `status` is `verified`, `needs_recheck`, `blocked` or `offline`. `verified` means relevant text and applicability were checked in that analysis; it does not establish product compliance. `consulted_at` uses `YYYY-MM-DD`. `kind` distinguishes `law`, `regulation`, `guidance`, `proposal` and `practice`. `articles`, `applicability` and `notes` are strings; record consultation limits in `notes`.

Document access failures and alternative sources; do not simulate research. Offline, use [local PDFs](pdf-library.md), their dates and unresolved questions. A rule cited in a 2022 PDF does not establish effective status in 2026.
