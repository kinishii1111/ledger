"""Extract InvoiceFields from raw text via regex/heuristics. No LLM. Best-effort."""
from __future__ import annotations

import re
from datetime import datetime

from ledger.schema import InvoiceFields

_CNPJ_RE = re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{14}")
_VALOR_RE = re.compile(r"(?:R\s?\$)\s*([\d.]+,\d{2})")
_VENC_RE = re.compile(
    r"venc(?:imento)?\s*[:\-]?\s*(\d{1,2})/(\d{1,2})/(\d{2,4})",
    re.IGNORECASE,
)
_VENC_ISO_RE = re.compile(r"venc(?:imento)?\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)

_MESES = {
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
}


def _to_float(br: str) -> float:
    return float(br.replace(".", "").replace(",", "."))


def _parse_date(day: str, month: str, year: str) -> str:
    y = int(year)
    if y < 100:
        y += 2000 if y < 70 else 1900
    return datetime(y, int(month), int(day)).strftime("%Y-%m-%d")


def extract_rules(text: str) -> InvoiceFields:
    text = " ".join(text.split())

    cnpj = _CNPJ_RE.search(text)
    endereco = cnpj.group(0) if cnpj else ""

    valor = 0.0
    m_val = _VALOR_RE.search(text)
    if m_val:
        valor = _to_float(m_val.group(1))

    vencimento = ""
    m_iso = _VENC_ISO_RE.search(text)
    if m_iso:
        vencimento = m_iso.group(1)
    else:
        m_venc = _VENC_RE.search(text)
        if m_venc:
            vencimento = _parse_date(*m_venc.groups())

    emissor = ""
    m_fat = re.search(r"fatura\s+(.+?)(?:\s+cnpj\b|\s+total:|\s+venc)", text, re.IGNORECASE)
    if m_fat:
        emissor = m_fat.group(1).strip()
    if not emissor:
        head = text.split("CNPJ")[0].split("Total:")[0]
        emissor = head[:60].strip() or "desconhecido"

    return InvoiceFields(
        emissor=emissor,
        endereco=endereco,
        valor=valor,
        vencimento=vencimento,
    )