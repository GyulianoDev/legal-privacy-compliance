# Legal Privacy Compliance

Skill para analisar projetos e preparar termos, políticas e inventários com evidências técnicas, pesquisa oficial e pendências explícitas. Documentação em português; scripts e nomes de arquivos em inglês.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-SKILL.md-5865F2?style=for-the-badge)
![Local](https://img.shields.io/badge/Execução-Local-17876D?style=for-the-badge)

---

## 📌 Sobre o Projeto

O agente investiga o projeto, consulta os PDFs pertinentes, pesquisa legislação atual e escreve as seções. Os scripts ajudam na descoberta, rastreabilidade, geração de arquivos e auditoria.

---

## ✨ Funcionalidades

- 🔎 Descoberta estática de frameworks, integrações e categorias candidatas de dados em várias linguagens.
- 🧭 Separação de dependências, configuração, código, schemas e testes; nenhuma delas é apresentada automaticamente como uso em produção.
- 📝 Nove roteiros para documentos condicionais, com geração Markdown e metadados JSON a partir de brief escrito pelo agente.
- 🍪 Fluxos específicos de cookies, consentimento, IA, menores, SaaS e transferências.
- 📚 Consulta dos PDFs por página, com hash e proveniência, mesmo após instalar em outro projeto.
- 🧪 Auditoria de contradições, arquivos novos sem sobrescrita e inventários com campos desconhecidos explícitos.

Modos do agente: `FULL` (padrão), `TOS`, `PRIVACY`, `COOKIES`, `AI`, `AUDIT`, `UPDATE`, `CHECK`, `INVENTORY`, `EXPORT`. A CLI de geração aceita `FULL/TOS/PRIVACY/COOKIES/AI`; os demais modos são fluxos do agente com os scripts pertinentes. Idiomas documentais: `pt-BR`, `en`, `es`; tradução não define jurisdição.

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
| --- | --- |
| Agent Skills / Markdown / YAML | Núcleo comum e descoberta pelos clientes |
| Python 3.10+ e biblioteca padrão | Scanner, auditoria, geração, exportação e instalação |
| JSON Schema 2020-12 | Contratos de perfil, inventário, brief e metadados |
| pypdf, opcional | Extração de páginas dos PDFs incluídos |
| unittest / jsonschema | Testes funcionais e validação completa dos schemas |

---

## 🚀 Instalação

Copie este pedido para o seu agente instalar a skill no projeto atual:

```text
Agente, instale esta skill em meu ambiente para usá-la no meu projeto atual: https://github.com/GyulianoDev/legal-privacy-compliance
Use a branch ptbr e a instalação por projeto compatível com este agente.
```

Tenha Python 3.10+ e o agente escolhido. Abra o terminal nesta pasta, a que contém `SKILL.md`. Os comandos usam `python`; em sistemas onde o executável se chama `python3`, use esse nome.

Para obter o pacote pelo GitHub:

```sh
git clone --branch ptbr https://github.com/GyulianoDev/legal-privacy-compliance.git
cd legal-privacy-compliance
```

1. Confira o destino com `--dry-run`.
2. Execute sem `--dry-run` para copiar a pasta inteira, incluindo PDFs.
3. Abra/recarregue a sessão do cliente e confirme a descoberta.

```sh
python scripts/install-skill.py --agent claude --project /path/to/project --dry-run
python scripts/install-skill.py --agent claude --project /path/to/project
python scripts/install-skill.py --agent codex --project /path/to/project
python scripts/install-skill.py --agent antigravity --project /path/to/project
```

Escolha o cliente necessário. Codex e Antigravity compartilham o destino atual `.agents/skills/`; basta uma cópia nesse projeto. O instalador recusa destino existente e não atualiza outra instalação automaticamente. No PowerShell, caminhos com espaços precisam de aspas:

```powershell
python scripts/install-skill.py --agent codex --project "C:\Projects\My App"
```

Instalação global, quando desejada:

```sh
python scripts/install-skill.py --agent claude --scope global
python scripts/install-skill.py --agent codex --scope global
python scripts/install-skill.py --agent antigravity --scope global
```

| Cliente | Projeto | Global |
| --- | --- | --- |
| Claude Code | `.claude/skills/legal-privacy-compliance/` | `~/.claude/skills/legal-privacy-compliance/` |
| Codex | `.agents/skills/legal-privacy-compliance/` | `~/.agents/skills/legal-privacy-compliance/` |
| Antigravity | `.agents/skills/legal-privacy-compliance/` | `~/.gemini/config/skills/legal-privacy-compliance/` |

Caminhos conferidos na documentação oficial em 2026-11-05: [Claude](https://code.claude.com/docs/en/skills), [Codex](https://developers.openai.com/codex/skills/), [Antigravity](https://antigravity.google/docs/skills), [padrão Agent Skills](https://agentskills.io/specification). Diferenças de superfície, diretórios legados e protocolo de validação estão em [compatibilidade](adapters/compatibility.md).

Para extrair PDFs por script:

```sh
python -m pip install "pypdf>=6,<7"
python scripts/read-pdf.py --list
python scripts/read-pdf.py --id cookies --pages 28-36 --out cookie-excerpts.txt
```

Um agente com leitor de PDF pode consultar os arquivos diretamente. Os scripts principais não precisam de rede, chave ou dependência externa.

---

## ▶️ Como Usar

No Claude Code ou Antigravity App/CLI:

```text
/legal-privacy-compliance INVENTORY: analise este projeto e liste apenas fatos, indícios e pendências.
```

No Codex:

```text
$legal-privacy-compliance FULL: prepare os documentos aplicáveis a este projeto.
```

Para descoberta automática, quando habilitada no cliente, peça naturalmente: “Verifique se minha política de privacidade corresponde ao código” ou “Meu SaaS usa IA; analise e prepare os documentos aplicáveis”. A descrição permite seleção por intenção; o cliente decide a ativação. Confira as limitações de integração abaixo.

Execução local dos auxiliares:

```sh
python scripts/scan-project.py /path/to/project --out ../private-scan
python scripts/detect-trackers.py /path/to/project --out ../private-trackers.json
python scripts/generate-documents.py --brief examples/reviewed-brief.json --sources examples/researched-sources.json --out ../private-drafts
python scripts/verify-consistency.py --profile ../private-scan/project-profile.json --inventory ../private-scan/data-inventory.json --policies /path/to/policies --out ../private-audit.json
python scripts/export-documents.py ../private-drafts/privacy-policy.md --format html --out ../privacy-preview.html
```

As saídas precisam ser novas. A auditoria retorna `2` com achados `HIGH/CRITICAL`, `0` nos demais resultados e erro em entrada inválida. Zero não certifica conformidade. O gerador sempre mantém `status: draft` e `publishable: false`; não existe atalho para aprovação automática. O exemplo deixa fontes vazias e pendências visíveis de propósito. O brief fictício está em inglês nas duas branches; o idioma dos documentos segue o campo `language` do brief, não a branch.

Os [workflows](workflows/document-generation.md) explicam o brief, a matriz de aplicabilidade, pesquisa, perguntas, revisão e atualização. O agente também entrega relatório interno, fontes datadas, pendências e changelog fundamentado. Procedimento de incidentes é interno.

HTML e JSON são exportações locais opt-in. O HTML renderiza títulos, parágrafos, listas simples e tabelas sem células multilinha, com conteúdo escapado; não é um renderizador completo de Markdown. PDF, DOCX, MDX, React e telas mobile dependem de ferramentas/implementação e autorização no projeto de destino; não estão disponíveis como exportação automática nesta versão.

---

## 📁 Organização dos Arquivos

```text
legal-privacy-compliance/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── agents/openai.yaml
├── adapters/compatibility.md
├── references/          # pesquisa, critérios e fontes
│   └── pdfs/            # cinco PDFs e catalog.json
├── workflows/           # seis procedimentos
├── templates/           # nove roteiros documentais
├── scripts/             # comandos e módulos compartilhados
├── schemas/             # quatro contratos JSON Schema
├── examples/            # brief fictício e fontes vazias
└── tests/fixtures/      # dez cenários estáticos
```

O repositório mantém `ptbr` como branch padrão e `en` com todos os arquivos Markdown e comentários explicativos em inglês, incluindo instruções, templates, referências, workflows e changelog. Os caminhos, a implementação, os exemplos JSON, os metadados de interface e os PDFs são idênticos nas duas branches. Os PDFs preservam o idioma original. A troca de idioma não cria nomes de arquivo diferentes.

---

## 🧪 Testes

```sh
python scripts/validate-skill.py
python -m unittest discover -s tests -v
```

Para incluir validação completa dos schemas e extração PDF, use um ambiente virtual:

```sh
python -m venv .venv
```

Ative com `.venv\Scripts\Activate.ps1` no PowerShell ou `source .venv/bin/activate` no Linux/macOS; depois:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Os testes cobrem os dez cenários, falsos positivos, segredos não reproduzidos, contextos de teste/schema/dependência, contradições com evidência, pendências, três idiomas, exportação escapada, schemas, não sobrescrita e instalação com a biblioteca. Testes de schema são ignorados se `jsonschema` não estiver instalado; criação de symlink pode ser ignorada em contas Windows sem esse privilégio.

O validador local verifica links, sintaxe Python, JSON e integridade dos PDFs. Para validação completa do frontmatter, também foi usado `quick_validate.py` da skill oficial `skill-creator` do ambiente de criação; esse arquivo não é dependência de execução do pacote.

Resultado desta entrega: **26 testes, 25 aprovados e 1 ignorado** pela falta de privilégio para criar symlink no Windows. Os quatro schemas, hashes e extração de trechos dos cinco PDFs foram conferidos. Veja o [relatório de validação](references/validation-report.md) para o alcance exato dos testes.

---

## ⚠️ Segurança e Limitações

- Análise estática heurística: ausência de achado não comprova ausência de tratamento. Até 5.000 arquivos, 512.000 bytes por arquivo; sem execução do produto nem captura de produção. Parsers de linguagens/configurações não são completos.
- `.env`, arquivos com nomes de credenciais/segredos, links e diretórios gerados são pulados. Isso reduz exposição; não é um detector universal de segredos. Relatórios trazem indicadores, caminhos/linhas e hashes, sem valores nem trechos brutos.
- Bases, finalidades, retenção, papéis e regiões precisam de evidência e revisão. A biblioteca histórica e a pesquisa inicial não substituem atualização oficial por projeto. Referências bloqueadas ficam pendentes.
- Nenhum script publica, faz commit, acessa banco, executa aplicação ou envia código. Guarde relatórios fora de pastas servidas e revise antes de compartilhar.
- O pacote não substitui advogado/encarregado, não garante conformidade e não aprova documentos para publicação.
- Os PDFs de terceiros conservam atribuição e não recebem a licença MIT do código. Conferir permissões antes de redistribuição pública.
- Verificados localmente: scripts Python no Windows, fixtures, schemas, instalação/cópia e integridade da biblioteca. Descoberta e execução completa nos três clientes, macOS/Linux e exportações PDF/DOCX **ainda não foram validadas**. O [protocolo](adapters/compatibility.md) indica como testar.
