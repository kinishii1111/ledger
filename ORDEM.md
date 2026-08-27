# ORDEM — tarefa/f1.2-rules-extract

## Agente
opencode

## Objetivo
Extract sem LLM: parse texto + regras → InvoiceFields (F1.2).

## Copiar de
- schema: src/ledger/schema.py
- CLI stubs: src/ledger/__main__.py
- ideia OSS: regex/rules extractors (pdf-extract rules) — menor diff

## Fazer
1. Criar `src/ledger/parse.py` — ler path `.md`/`.txt` → str
2. Criar `src/ledger/rules.py` — `extract_rules(text: str) -> InvoiceFields` (regex/heurística; best-effort)
3. Em `__main__.py`: `ledger extract PATH` e `ledger extract --rules PATH` chama parse+rules; imprime JSON; exit 0 se valida schema, 2 se falha
4. NÃO criar fixtures (outra branch)

## Arquivos permitidos
- src/ledger/parse.py
- src/ledger/rules.py
- src/ledger/__main__.py
- src/ledger/__init__.py  (só se precisar export)

## Não fazer
- Sem LLM/API, sem fixtures/, sem validate.py, sem UI, sem pytest suite, sem merge main

## Ownership
- src/ledger/parse.py
- src/ledger/rules.py
- src/ledger/__main__.py (só comando extract)

## Pronto quando
```bash
pip install -e . -q
# se fixtures ainda não na branch, usar stdin/file temporário:
printf '%s\n' 'Fatura Acme Ltda CNPJ 12.345.678/0001-90 Total: R$ 1500,00 Vencimento: 15/09/2026' > /tmp/inv.md
ledger extract --rules /tmp/inv.md | python -c "import sys,json; from ledger.schema import InvoiceFields; InvoiceFields.model_validate(json.load(sys.stdin)); print('ok')"
```

## Tema
F1.2 rules extract offline
