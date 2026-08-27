"""Read a document file (.md/.txt) → str."""
from __future__ import annotations

from pathlib import Path

_SUPPORTED = {".md", ".txt"}


def read_document(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"arquivo não encontrado: {path}")
    if p.suffix.lower() not in _SUPPORTED:
        raise ValueError(f"extensão não suportada: {p.suffix} (use .md ou .txt)")
    return p.read_text(encoding="utf-8")