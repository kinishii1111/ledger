# ORDEM — tarefa/f1.1-fixtures

## Agente
agy

## Objetivo
3 fixtures sintéticas invoice + golden JSON (F1.1).

## Copiar de
- shape: pasta `fixtures/<id>/doc.md` + `expected.json` (ver fixtures/README.md)
- campos: src/ledger/schema.py (InvoiceFields)
- refs OSS (só shape mental): vinimabreu/doc-eval corpus sintético — NÃO clonar neste commit

## Fazer
- Criar exatamente:
  - fixtures/inv-01/doc.md + expected.json
  - fixtures/inv-02/doc.md + expected.json
  - fixtures/inv-03/doc.md + expected.json
- doc.md = texto de fatura legível (pt ou en), com emissor, endereço/CNPJ, valor, vencimento
- Plantar 1 armadilha: inv-02 com data de **emissão** e **vencimento** distintas (texto deixa claro)
- expected.json = InvoiceFields válido (vencimento AAAA-MM-DD, valor number)
- Atualizar fixtures/README.md com a lista dos 3 ids (curto)

## Arquivos permitidos
- fixtures/inv-01/**
- fixtures/inv-02/**
- fixtures/inv-03/**
- fixtures/README.md

## Não fazer
- NÃO tocar src/
- Sem PDF, sem LLM, sem UI, sem merge main, sem testes pytest

## Ownership
- Só fixtures/**

## Pronto quando
```bash
test -f fixtures/inv-01/expected.json
test -f fixtures/inv-02/expected.json
test -f fixtures/inv-03/expected.json
python -c "from pathlib import Path; import json; from ledger.schema import InvoiceFields
for p in Path('fixtures').glob('inv-*/expected.json'):
  InvoiceFields.model_validate(json.loads(p.read_text()))
  assert (p.parent/'doc.md').is_file()
print('ok', 3)"
```

## Tema
F1.1 golden set sintético
