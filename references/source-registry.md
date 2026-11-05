# Fontes e manutenção

Pesquisa de preparação: **2026-11-05**. Este registro não substitui uma consulta atual por projeto. É ponto de partida com estado e limites; não deve ser convertido em fontes verificadas para qualquer produto sem nova análise.

Use o portal Planalto como origem prioritária. Na preparação, algumas páginas devolveram bloqueio de acesso; a legislação consolidada da Câmara foi a alternativa oficial. Catálogo ANPD e página institucional não confirmam por si só o conteúdo integral de um ato ou prazo.

| Fonte | URL oficial | Estado na preparação |
| --- | --- | --- |
| LGPD consolidada | https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html | Texto consultado; conferir alterações a cada uso. |
| Marco Civil atualizado | https://www2.camara.leg.br/legin/fed/lei/2014/lei-12965-23-abril-2014-778630-normaatualizada-pl.pdf | Texto consultado. |
| Decreto 8.771/2016 | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/d8771.htm | Acesso bloqueado; pesquisar alternativa oficial antes de citar dispositivo. |
| CDC consolidado | https://www2.camara.leg.br/legin/fed/lei/1990/lei-8078-11-setembro-1990-365086-normaatualizada-pl.html | Texto consultado. |
| Código Civil consolidado | https://www2.camara.leg.br/legin/fed/lei/2002/lei-10406-10-janeiro-2002-432893-normaatualizada-pl.html | Texto consultado. |
| ECA consolidado | https://www2.camara.leg.br/legin/fed/lei/1990/lei-8069-13-julho-1990-372211-normaatualizada-pl.html | Texto consultado. |
| Decreto 7.962/2013 | https://www2.camara.leg.br/legin/fed/decret/2013/decreto-7962-15-marco-2013-775557-publicacaooriginal-139266-pe.html | Publicação original consultada; pesquisar alterações. |
| Regulamentações ANPD | https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd | Catálogo consultado; verificar inteiro teor de cada ato. |
| Resolução 19/2024 | https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024 | Texto e indicação de retificação consultados. |
| Resolução 2/2022 | https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022 | Texto consultado; conferir alterações. |
| Materiais ANPD | https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes | Localização de guias e edições. |
| ECA Digital ANPD | https://www.gov.br/anpd/pt-br/assuntos/eca-digital | Página atual consultada; atos e orientações devem ser abertos para uso concreto. |

Para cada pesquisa de projeto, criar `legal-sources.json`: array de `{id, title, url, jurisdiction, kind, articles, consulted_at, status, applicability, notes}`. `status` é `verified`, `needs_recheck`, `blocked` ou `offline`. `verified` significa texto relevante e aplicabilidade conferidos naquela análise; não significa conformidade do produto. `consulted_at` usa `YYYY-MM-DD`. `kind` distingue `law`, `regulation`, `guidance`, `proposal` e `practice`. `articles`, `applicability` e `notes` são strings; registre os limites da consulta em `notes`.

Documente falha de acesso e fonte alternativa; não simule consulta. Em modo offline use [PDFs locais](pdf-library.md), suas datas e pendências. Uma norma citada em PDF de 2022 não comprova vigência em 2026.
