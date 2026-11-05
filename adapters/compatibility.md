# Compatibilidade e descoberta

Documentação oficial consultada em **2026-11-05**. O núcleo compartilhado é um único diretório `legal-privacy-compliance` com `SKILL.md`; não há três cópias divergentes nem necessidade de wrapper proprietário para executar os scripts. Apenas `agents/openai.yaml` acrescenta metadados opcionais do Codex.

| Agente | Projeto | Global do usuário | Ativação manual |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/legal-privacy-compliance/` | `~/.claude/skills/legal-privacy-compliance/` | `/legal-privacy-compliance` |
| Codex | `.agents/skills/legal-privacy-compliance/` | `~/.agents/skills/legal-privacy-compliance/` | `$legal-privacy-compliance`; seletor `/skills` conforme cliente |
| Google Antigravity | `.agents/skills/legal-privacy-compliance/` | `~/.gemini/config/skills/legal-privacy-compliance/` | App/CLI: `/legal-privacy-compliance`; IDE: conferir Customizations |

O Antigravity também documenta caminhos legados como `.agent/skills` no projeto e `~/.gemini/antigravity/skills` no IDE. O instalador usa os caminhos compartilhados atuais; não instala duplicatas em diretórios legados. Claude e Codex não recebem automaticamente todos os diretórios específicos do outro agente.

Nos três produtos, descoberta por descrição permite ativação por intenção quando habilitada no cliente; não é garantia de acionamento em toda mensagem. Reinicie/recarregue a sessão ou use o mecanismo de atualização do cliente após instalar. No CLI Antigravity, conferir `/skills reload` na versão instalada. A sintaxe e disponibilidade de seletores podem variar por superfície/versão.

## Verificação prática de aceitação em cada cliente

1. Instalar numa pasta de teste pelo comando do README, com a biblioteca completa.
2. Abrir uma sessão nova na raiz desse projeto e confirmar descoberta do nome/descrição.
3. Invocar manualmente `INVENTORY` em um projeto fictício; conferir acesso aos scripts e `read-pdf.py --list` pelo caminho instalado.
4. Em outra sessão, pedir naturalmente uma auditoria de política sem citar o nome; observar se o cliente seleciona a skill.
5. Verificar que não executa app, lê `.env`, publica ou inventa identidade; conferir relatórios e pendências.
6. Registrar cliente, versão, sistema, invocação, permissões, resultado e falhas. Descoberta correta não prova qualidade jurídica.

**Estado desta entrega:** formato, scripts e instalação local testados; nenhuma sessão completa de Claude Code, Codex instalado ou Antigravity foi iniciada como teste de descoberta/execução. macOS/Linux e renderização PDF/DOCX também não foram executados. Não confundir documentação oficial e cópia de pastas com esses testes.

Fontes primárias: [Agent Skills](https://agentskills.io/specification), [Claude Code Skills](https://code.claude.com/docs/en/skills), [Codex Skills](https://developers.openai.com/codex/skills/), [Google Antigravity Skills](https://antigravity.google/docs/skills).
