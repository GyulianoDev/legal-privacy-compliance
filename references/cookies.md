# Cookies, armazenamento e preferências

Use código/configuração e, quando autorizado, observação de rede em ambiente de teste com dados fictícios. Dependência não comprova disparo; disparo sem cookie pode transmitir dados pessoais. `localStorage` usado só para tema não implica consentimento por si só.

Inventarie nome/chave ou padrão, tecnologia, fornecedor, domínio, dados transmitidos, finalidade, categoria, primeira/terceira parte, duração verificada, momento de ativação, condição de consentimento e evidência. Separe o que foi visto do que depende de painel do fornecedor. Não deduza duração pelo nome.

Quando a operação depender de consentimento, a especificação deve incluir:

- Aceitar, rejeitar não essenciais e personalizar em linguagem clara, com facilidade equivalente; sem caixas previamente marcadas para opção dependente de consentimento.
- Bloqueio antes da escolha, inclusive tags, pixels, SDKs e chamadas servidor/cliente pertinentes.
- Categorias explicadas, política acessível e alteração/revogação posterior.
- Persistência e registro mínimo das escolhas, versões e duração justificada, sem transformar o registro num rastreador adicional.
- Testes de primeira visita, rejeição, aceite parcial, revogação e nova sessão. Verificar se carregamento via GTM contorna a preferência.

Política escrita não implementa bloqueio. Entregue `consent-banner-spec.md` quando aplicável e liste divergências técnicas para implementação autorizada. Não acrescente banner nem altere o aplicativo durante a geração documental.

O PDF local é edição histórica de 2022. Há redação problemática na p. 24 sobre legítimo interesse pelo poder público; não use essa frase como fundamento. Consulte versão/errata oficial e o [catálogo analisado](pdf-library.md).
