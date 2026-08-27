# ORDEM — tarefa/f1.3-validators

## Agente
opencode

<!-- Bounce: claude sem /login → opencode -->

## Objetivo
Validators determinísticos sobre InvoiceFields / dict (F1.3).

## Copiar de
- src/ledger/schema.py
- ideia: paperflow/ap-verify critics baratos — data + número

## Fazer
1. Criar `src/ledger/validate.py` com:
   - `normalize_vencimento(s) -> str` (aceita DD/MM/AAAA ou AAAA-MM-DD → AAAA-MM-DD)
   - `validate_fields(data: dict | InvoiceFields) -> list[str]` erros (vazio = ok)
   - regras: vencimento formato AAAA-MM-DD; valor finito >= 0; emissor/endereco non-empty strip
2. Criar `src/ledger/__main_validate_hint.py` NÃO — em vez disso módulo rodável:
   `python -m ledger.validate` lê JSON stdin e imprime `{"ok": bool, "errors": [...]}` exit 0 se ok else 2
3. NÃO editar `__main__.py` (Ownership opencode)

## Arquivos permitidos
- src/ledger/validate.py
- src/ledger/schema.py (só import; NÃO mudar campos ouro)

## Não fazer
- Sem __main__.py, sem fixtures, sem LLM, sem UI, sem merge main

## Ownership
- src/ledger/validate.py

## Pronto quando
```bash
pip install -e . -q
echo '{"emissor":"Acme","endereco":"x","valor":10,"vencimento":"2026-09-15"}' | python -m ledger.validate
echo '{"emissor":"","endereco":"x","valor":-1,"vencimento":"15/09/2026"}' | python -m ledger.validate ; test $? -eq 2
```

## Tema
F1.3 deterministic validators
