# ORDEM — tarefa/f1.4-eval-replay

Closes #1

## Agente
claude

## Objetivo
Field-level eval + report MD. `ledger eval --replay` (offline, sem LLM).

## Copiar de
- shape mental: doceval field report (NÃO clonar repo inteiro neste commit)
- schema: src/ledger/schema.py
- extract rules: src/ledger/rules.py + parse.py
- validate: src/ledger/validate.py
- fixtures: fixtures/inv-*/expected.json + doc.md

## Fazer
1. Criar `src/ledger/eval_run.py`:
   - carregar golden `fixtures/*/expected.json`
   - pred: se existir `cache/<id>.json` usa; senão roda `extract_rules(read_document(doc.md))`
   - score por campo (emissor, endereco, valor, vencimento): exact match após strip; valor com tolerância abs 0.01; vencimento já ISO
   - retornar estrutura + accuracy overall e per-field
2. Escrever `reports/eval-replay.md` (e opcional `.json`) com tabela por campo + mismatches
3. Wire `__main__.py`: `ledger eval --replay` → print resumo + grava report; exit 0 sempre que rodou (score baixo não é crash); exit 2 só erro de IO/schema
4. Criar `reports/.gitkeep` se pasta vazia no git — report gerado pode ir no commit se fixtures forem estáveis

## Arquivos permitidos
- src/ledger/eval_run.py
- src/ledger/__main__.py
- reports/**
- NÃO fixtures/ (só ler)
- NÃO validate.py / rules.py / parse.py / schema.py (só import)

## Não fazer
- Sem LLM, sem --live, sem UI, sem pytest suite, sem merge main, sem CI yaml

## Ownership
- src/ledger/eval_run.py
- src/ledger/__main__.py (só subcomando eval)
- reports/

## Pronto quando
```bash
pip install -e . -q
ledger eval --replay
test -f reports/eval-replay.md
grep -q emissor reports/eval-replay.md
```

## Tema
F1.4 eval harness offline — Closes #1
