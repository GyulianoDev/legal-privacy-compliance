# Verificações da entrega 1.0.0

Executadas em **2026-11-05**, Windows, Python **3.14.6**. Os scripts exigem 3.10+, mas outras versões e sistemas não foram executados.

| Verificação | Resultado observado |
| --- | --- |
| `skill-creator/scripts/quick_validate.py` do ambiente | `Skill is valid!` |
| `scripts/validate-skill.py` | Entrada, sintaxe, links, JSON, recursos e cinco hashes aprovados |
| `unittest discover -s tests -v` com jsonschema instalado | 26 testes: 25 aprovados, 1 ignorado, nenhuma falha |
| Dez cenários fictícios | Sinais esperados identificados; nenhum apresentado como produção confirmada |
| Quatro schemas | Definições válidas em Draft 2020-12; perfis/inventários dos dez cenários e brief/metadados validados |
| Auditoria CLI | Contradições de IP, analytics e IA detectadas com arquivo/linha; retorno 2 no cenário propositalmente incorreto |
| Geração CLI | Rascunho criado, pendências preservadas, segunda execução no mesmo destino recusada |
| Exportação HTML/JSON | Conteúdo ativo escapado; estado de rascunho preservado; sobrescrita recusada |
| Instalação local de teste | Cópia autocontida em diretórios de descoberta; cinco PDFs presentes; script da cópia leu o próprio catálogo |
| PDFs originais e cópias | Cinco hashes coincidem; originais preservados; 40, 49, 11, 15 e 52 páginas respectivamente |
| Extração pela CLI portátil | Cookies pp. 28–29; Senado pp. 4–5; Defesa pp. 9–11; gov.br pp. 13–15; poder público pp. 30–31, com saída não vazia |

O teste ignorado tenta criar um symlink real: a conta Windows não tinha o privilégio necessário. A implementação pula symlinks/reparse points, mas esse comportamento não foi comprovado por criação real de link neste ambiente.

Os testes verificam comportamento técnico e invariantes, não correção de parecer jurídico ou aprovação documental. Não houve teste de descoberta/ativação automática ou sessão completa nos aplicativos Claude Code, Codex e Antigravity; os caminhos foram comparados com documentação oficial e a cópia local foi exercitada. Consulte o [protocolo por cliente](../adapters/compatibility.md).

Sem teste em Linux/macOS, exportação PDF/DOCX, integração de rotas públicas, inspeção de produção ou validação de todos os ramos normativos/linguísticos. Os testes não instalaram a skill globalmente nem executaram publicação pelos scripts do pacote. A preparação posterior do repositório mantém os mesmos caminhos e implementação nas branches `ptbr` e `en`, com tradução dos arquivos Markdown e comentários explicativos. PDFs originais, exemplos JSON e metadados de interface são compartilhados.
