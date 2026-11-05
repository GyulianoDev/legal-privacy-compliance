# Exemplos fictícios

`reviewed-brief.json` demonstra o formato de entrada, não um caso juridicamente aprovado. Identidade, bases e prazos permanecem pendentes. `researched-sources.json` está intencionalmente vazio: os testes não simulam uma pesquisa oficial que não ocorreu para um produto real.

Os dez projetos pequenos em `tests/fixtures/` são entradas estáticas de teste, com trechos que não devem ser executados como aplicações. Eles cobrem landing, analytics, comércio, mobile, SaaS, IA, menores, internacional, dependências sem implementação e política contraditória.

Para experimentar, execute na raiz da skill:

```sh
python scripts/scan-project.py tests/fixtures/incorrect-policies --out ../demo-scan
python scripts/verify-consistency.py --profile ../demo-scan/project-profile.json --inventory ../demo-scan/data-inventory.json --policies tests/fixtures/incorrect-policies/policies --out ../demo-audit.json
python scripts/generate-documents.py --brief examples/reviewed-brief.json --sources examples/researched-sources.json --out ../demo-drafts
```

A auditoria desse cenário retorna **2** porque encontra contradições de alta prioridade. A geração cria apenas política de privacidade em rascunho, com pendências; o modo `FULL` não força nove documentos. Use saídas novas ao repetir.
