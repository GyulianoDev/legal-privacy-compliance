# Redação e aplicabilidade

| Documento | Critério para considerar |
| --- | --- |
| Termos | Relação de uso do serviço; dimensionar obrigações e contratação |
| Privacidade | Tratamento de dados pessoais confirmado ou a confirmar |
| Cookies | Cookies/tecnologias semelhantes que mereçam transparência específica |
| IA | Uso real de modelos, automação, RAG, agentes ou decisões |
| Uso aceitável | Contas, conteúdo, APIs, bots ou risco de abuso |
| Exclusão/retenção | Ciclo de vida de dados com procedimentos relevantes |
| DPA | Tratamento em nome de outro controlador em relação contratual |
| Consentimento | Finalidade específica realmente apoiada em consentimento |
| Incidentes | Procedimento interno de resposta; não política pública automática |

Não gere todos os documentos por padrão: `FULL` cobre todos os aplicáveis, com
justificativa para inclusão e exclusão. Landing page estática não ganha assinatura,
cadastro, banner de marketing ou DPA sem evidência. Avalie avisos de colaboradores,
candidatos, RIPD, registro de operações, comunidade e vendedores se pertinentes.

Templates são roteiros condicionais, não contratos para simples troca de nome.
Redija detalhes verificáveis e cite os dispositivos relevantes. Cláusulas devem
explicar finalidade, procedimento e consequências, sem promessas absolutas ou
renúncia de direitos. Base, identidade, contato, retenção ou termos essenciais
desconhecidos permanecem em pendências internas; não lance isso em página pública.

O brief de `generate-documents.py` contém `product`, `version`, `updated_at`,
`language`, `identity`, `pending` e `documents`. Cada documento informa `type`,
`title`, `applicable`, `applicability_reason`, `sections` (`heading`, `body`),
`source_ids`, `evidence_ids`, `pending`. Consulte [exemplo](../examples/reviewed-brief.json).
Esse arquivo é conteúdo preparado pelo agente após análise; preencher JSON não
confirma fatos nem aprova publicação. Os JSONs gerados mantêm `publishable: false`.

Saída interna em pasta nova: documentos Markdown/metadata, inventário revisado,
relatório, informações ausentes e fontes. Mantenha uma relação explícita entre
parágrafo -> operação -> evidência -> dispositivo. Para EN/ES, traduza significado,
definições e exceções; idioma não decide jurisdição. Produza componentes, MDX e
rotas somente mediante pedido de integração; não confunda exportar com publicar.
