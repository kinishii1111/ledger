# ORQUESTRACAO — Ledger (async)

## Padrão

```
Cursor: branch tarefa/<id> + ORDEM.md + commit (+ push se remote)
  → lacaio local (watch-lacaios) OU Jules na nuvem
  → commit/PR prefixado
  → REVIEW GATE (Cursor) → merge|bounce
```

- Serial miúdo: skill `kin-opencode-tarefa`
- Paralelo ≤2 locais: `kin-lacaios` + Ownership disjunto
- Remoto GitHub: este repo (`kinishii1111/ledger`) — Jules **exige** remote
- Interno sem push: `--local` (lei `ORQUESTRACAO-LOCAL.md`) — Jules não entra

```bash
export PATH="/home/kin/.nvm/versions/node/v22.23.1/bin:/home/kin/.local/bin:$PATH"
# locais
watch-lacaios.sh --repo "$(pwd)" --agent all --worktree
# ou
kin-sessao --repo "$(pwd)"
```

## Regra OSS (obrigatória)

**Não nascer do zero se existir atalho open source.**

1. Pesquisar / usar lista em `../../entrada/oss-pesquisa-ledger.md`
2. Clonar em `labs/` ou `../../scratch/` (não na `main` do produto)
3. Rodar 1 comando do OSS; anotar o que roubar (shape de eval, schema, CLI)
4. Na ORDEM: seção **## Copiar de** com path/URL + o que reusar
5. Núcleo `src/ledger/`: só o mínimo adaptado (MIT/Apache — respeitar licença; não dump cego)

Lema: **copiar → preguiça → melhorar → ser esperto.**

Refs Fase 1: `dave8172/doceval`, `vinimabreu/doc-eval`, `DylanMerigaud/ai-invoice-parser`, `awslabs/stickler`.

## Jules (Google) — como encaixa

Jules = **lacaio remoto em VM Google**. Não compete por RAM com OpenCode/Agy nesta máquina (~8 GiB). Ideal pra fatias F1.4+ (scorer, report, multi-file) enquanto locais fazem F1.0–F1.2.

### Pré-requisitos (Kin, one-shot)

1. Conta Google + acesso Jules ([jules.google.com](https://jules.google.com)) — costuma pedir plano AI Pro/Ultra
2. Conectar o repo **kinishii1111/ledger** na UI Jules
3. CLI: `npm i -g @google/jules` → `jules login`
4. (Opcional Actions) secret `JULES_API_KEY` no GitHub

### Fluxo com nosso padrão

| Passo | Quem |
|-------|------|
| ORDEM com Ownership + Pronto quando | Cursor |
| `jules remote new --repo kinishii1111/ledger --session "…"` (colar objetivo da ORDEM) | Cursor / Kin |
| Jules abre sessão/PR na nuvem | Jules |
| Gate: diff Ownership, Pronto quando, merge ou bounce | Cursor |
| Prefixo commit/PR: anotar `jules:` no título se o Jules não prefixar | gate |

```bash
# listar repos conectados
jules remote list --repo

# disparar fatia (exemplo)
jules remote new --repo kinishii1111/ledger --session \
  "Read ORDEM on branch if any. Implement F1.4 field scorer + markdown report. Only touch paths listed. No UI. MIT-friendly; mirror doceval report shape."

# depois: puxar resultado
jules remote pull --session <id>
```

### Regras Jules

- **Mesma ORDEM mental** que lacaio local: arquivos permitidos, Pronto quando comportamental, sem merge na `main` sem gate.
- **Não** paralelo Jules + lacaio local nos **mesmos** paths.
- Não meter Jules no `watch-lacaios` ainda (não é binário local). Spawn **manual** ou Action depois.
- Não gastar Jules em smoke L0 (validators) — isso é local/instantâneo.

### Actions (depois, opcional)

`google-labs-code/jules-invoke` + label `jules` em issue/PR — só quando o fluxo manual estiver estável.

## Placa / higiene

- Eficiência: `Documents/.cursor/lei/LACAIOS-EFFICIENCIA.md`
- Pós-onda local: `scripts/limpar-lacaios.sh`
- Estado job sede: `sede fechar` se houver job; senão CHECKPOINT neste repo
