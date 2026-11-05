# Descoberta do projeto

Faça leitura estática antes de perguntas. Localize `AGENTS.md`, manifests, modelos,
rotas, telas, integrações, infraestrutura e políticas existentes. Não execute builds,
instaladores, migrações ou scripts do projeto para descobrir seu comportamento.

O scanner aceita linguagens comuns e manifests, limita tamanho/quantidade, omite
linhas brutas e ignora `.env*`, arquivos com nomes sensíveis, links e dependências.
Esses filtros não garantem ausência de segredos em nomes de arquivo ou metadados:
revise o relatório antes de compartilhar. Não imprima configurações para procurar
tokens; use nomes de variáveis e contratos públicos dos serviços.

Para cada integração, percorra dependência -> configuração -> import -> chamada ->
ambiente e confirmação operacional. Dependência não comprova uso; comentário,
fixture, schema e tela futura não comprovam coleta. Descreva limitações de análise
estática, linguagens não compreendidas e arquivos excluídos ou truncados.

Investigue produto, público, jurisdições, idiomas, canais, autenticação, uploads,
cobranças, publicidade, armazenamento, logs, backups, exclusão e terceiros. CNPJ de
pessoa jurídica não é automaticamente dado pessoal; MEI, empresário e vínculos a
pessoa natural exigem contexto. Endereço IP acessível ao servidor não significa
que ele esteja persistido; verifique logs de aplicação, proxy e hospedagem.

Saída: perfil e evidências identificadas por arquivo, linha, contexto, hash e
confiança. Antes de citar linha, confirme sua posição no arquivo original; o
pré-processamento do scanner não substitui leitura contextual.
