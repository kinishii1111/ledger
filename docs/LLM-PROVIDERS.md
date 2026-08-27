# LLM providers (F1.5+) — backlog Kin

Registrado para organizar depois. **Ainda não implementado.** Entra na fatia F1.5 (`extract --live` + cache).

## Decisão

Cliente fino **OpenAI-compatible**. Trocar vendor = env, não reescrever extrator.

```text
LEDGER_LLM_BASE=https://openrouter.ai/api/v1   # ou Gemini/Groq base
LEDGER_LLM_KEY=...                             # secret local / Actions
LEDGER_LLM_MODEL=...:free                      # ver lista viva do provider
```

Fluxo alvo:

```text
ledger extract --live PATH
  → HTTP chat.completions
  → JSON → validate
  → grava cache/
ledger eval --replay   # sem rede
```

## Opções ~custo zero

| Provedor | Uso | Limite típico |
|----------|-----|----------------|
| **Gemini free** (default preferido — cota já usada via Agy) | key Google | cota diária Google |
| **OpenRouter** modelos `:free` | 1 key, muitos modelos | ~20 req/min; ~50/dia sem crédito (sobe c/ histórico de crédito) |
| **Groq** free tier | OpenAI-compat, rápido | cota diária |
| Ollama local | zero API | **evitar** nesta máquina fraca |

OpenRouter: criar key em https://openrouter.ai/keys · modelos free = sufixo `:free` · lista rotaciona.

## CI / DevOps

- L0/L1: **sem** LLM (já no Actions).
- L2 live: só `workflow_dispatch` (ou cron raro) + secret `LEDGER_LLM_KEY` / `OPENROUTER_API_KEY` / `GEMINI_API_KEY`.
- Nunca live em todo push (cota + flaky).
- Segredo **nunca** no git — `.env` local + GitHub Actions secrets.

## Forma no código (quando for a hora)

Esboço (não existe ainda):

```
src/ledger/llm.py          # client OpenAI-compat (base/key/model)
src/ledger/extract_llm.py  # prompt → InvoiceFields
.env.example               # LEDGER_LLM_* documentado
cache/                     # gitignored; chave (doc_id, prompt_hash, model)
```

## Relação com fases

| Fatia | LLM? |
|-------|------|
| F1.0–F1.4 | Não (rules + validate + scorer offline) |
| **F1.5** | Sim — plug deste doc |
| F1.6+ | Usa o mesmo client |

## Refs OSS (shape)

- Extrator + eval: ai-invoice-parser, doceval  
- Não reinventar scorer nested: awslabs/stickler (se precisar)
