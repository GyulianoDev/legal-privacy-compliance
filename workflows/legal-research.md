# Pesquisa normativa

Comece pelo [registro](../references/source-registry.md). Para cada conclusão
material, abra o texto oficial pertinente e confira dispositivo, jurisdição,
vigência, alterações e ato regulamentar. Planalto bloqueado não implica lei
inacessível: consulte Câmara, Senado, ANPD ou Diário Oficial e registre a substituição.
Não confunda publicação original com texto consolidado nem minuta com regra vigente.

Crie `legal-sources.json` como array: `id`, `title`, `url`, `jurisdiction`, `kind`
(`law`, `regulation`, `guidance`, `proposal`, `practice`), `articles`, `consulted_at`,
`status` (`verified`, `needs_recheck`, `blocked`, `offline`), `applicability` e `notes`.
Use strings em `articles`, `applicability` e `notes`; `consulted_at` é `YYYY-MM-DD`.
A confirmação
é feita pelo agente na sessão; datas anteriores não viram data atual automaticamente.
Vincule fonte e evidência técnica à seção fundamentada.

Leia o PDF local pela edição e página física, conferindo paginação impressa. Um
PDF histórico ajuda a contextualizar e comparar; não substitui atualização da lei.
Modelos de órgãos públicos não são autoridade para práticas de um SaaS privado.
Não copie identificações, contatos, políticas setoriais ou cláusulas de foro.

Sem rede: entregue descoberta e rascunho, marque `OFFLINE_REFERENCE_ONLY`, cite
edições locais e liste exatamente o que depende de atualização. Não invente artigo,
jurisprudência ou vigência. Para IA, não afirme inexistência de regulação apenas
porque a pesquisa inicial não encontrou uma lei específica.
