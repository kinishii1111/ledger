# AGENTS — Ledger

Orquestrador: **Cursor** (Rick com Kin). Lacaios: **caveman** (`LACAIO.md`).

## Lei deste repo

1. **Copiar → engenharia reversa → melhorar.** Antes de inventar: clonar/ler OSS em `../scratch/` ou `labs/`, extrair o atalho, só então escrever no núcleo. Ver `ORQUESTRACAO.md` § OSS.
2. **Útil pra agente**, não UI humana. CLI / MCP / report.
3. **Eval > demo.** Sem score reproduzível não está pronto.
4. **Gate Kin:** cada fase valida em **1 caso do contexto real** (não só sintético). Ver `../FASES.md` Gate Kin.
5. **Máquina fraca:** L0/L1 local; L2 API flash + cache. Sem Ollama grande / Docker.
6. **Async:** 1 agente = 1 branch `tarefa/*` = 1 worktree. ORDEM.md. Sem auto-merge.

## Agentes

| id | Onde roda | Uso |
|----|-----------|-----|
| `opencode` | local (worktree) | default barato |
| `agy` | local | research/rascunho; cota Google |
| `claude` | local | se auth ok |
| `grok` | local | último |
| `jules` | **nuvem Google** (GitHub) | fatia longa / quando a caixa está cheia; **zero RAM local** |

Prioridade local: opencode → agy → claude → grok.  
Jules: paralelo **remoto** — Ownership disjunto; gate no PR/sessão como qualquer lacaio.

Skills sede: `kin-opencode-tarefa`, `kin-lacaios`, `kin-norte`.
