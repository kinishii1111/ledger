# Ledger

Document → JSON validado + **harness de eval**. Feito pra **agente** (CLI/MCP), não pra humano clicar.

Portfolio BrandCo · fases em `../FASES.md` (estudo) / commits `tarefa/*`.

## Agora (F1.0)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
ledger --help
ledger schema --example
```

## Norte

- Copiar OSS → engenharia reversa → núcleo mínimo (`AGENTS.md`, `ORQUESTRACAO.md`)
- L0/L1 offline; L2 API flash + cache (máquina fraca)
- Lacaios async + **Jules** (nuvem) — ver `ORQUESTRACAO.md`
- **LLM multi-provider (F1.5):** OpenRouter `:free` / Gemini / Groq — ver [`docs/LLM-PROVIDERS.md`](docs/LLM-PROVIDERS.md)

## Status

WIP Fase 1. Score E2E ainda não — não inventar número no README até `eval --replay` existir.
