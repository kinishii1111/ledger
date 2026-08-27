"""Validators determinísticos sobre InvoiceFields / dict (F1.3)."""

from __future__ import annotations

import json
import math
import re
import sys
from datetime import date
from typing import Union

from .schema import InvoiceFields

_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DMY = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")


def normalize_vencimento(s: str) -> str:
    """DD/MM/AAAA ou AAAA-MM-DD -> AAAA-MM-DD."""
    s = s.strip()
    m = _DMY.match(s)
    if m:
        d, mo, y = m.groups()
        return date(int(y), int(mo), int(d)).isoformat()
    if _ISO.match(s):
        y, mo, d = s.split("-")
        return date(int(y), int(mo), int(d)).isoformat()
    raise ValueError(f"vencimento inválido: {s!r}")


def validate_fields(data: Union[dict, InvoiceFields]) -> list[str]:
    """Lista de erros; vazio = ok."""
    errors: list[str] = []
    if isinstance(data, InvoiceFields):
        data = data.model_dump()
    if not isinstance(data, dict):
        return ["entrada deve ser dict ou InvoiceFields"]

    emissor = data.get("emissor")
    if not isinstance(emissor, str) or not emissor.strip():
        errors.append("emissor não pode ser vazio")
    endereco = data.get("endereco")
    if not isinstance(endereco, str) or not endereco.strip():
        errors.append("endereco não pode ser vazio")

    valor = data.get("valor")
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        errors.append("valor deve ser número")
    elif not math.isfinite(valor):
        errors.append("valor deve ser finito")
    elif valor < 0:
        errors.append("valor deve ser >= 0")

    vencimento = data.get("vencimento")
    if not isinstance(vencimento, str):
        errors.append("vencimento deve ser string")
    else:
        try:
            v = normalize_vencimento(vencimento)
            if v != vencimento.strip():
                data["vencimento"] = v
        except ValueError:
            errors.append("vencimento deve ser AAAA-MM-DD ou DD/MM/AAAA")

    return errors


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "errors": [f"JSON inválido: {e}"]}))
        sys.exit(2)
    errors = validate_fields(data)
    ok = not errors
    print(json.dumps({"ok": ok, "errors": errors}))
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()