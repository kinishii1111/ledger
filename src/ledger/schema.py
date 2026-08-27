"""Campos ouro Fase 1 — fonte única do contrato."""

from __future__ import annotations

from pydantic import BaseModel, Field


class InvoiceFields(BaseModel):
    emissor: str = Field(..., description="Quem emitiu a fatura")
    endereco: str = Field(..., description="Endereço ou CNPJ do emissor")
    valor: float = Field(..., description="Valor total devido")
    vencimento: str = Field(..., description="Data de vencimento AAAA-MM-DD")
