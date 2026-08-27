"""F1.4 — eval harness offline (replay). Sem LLM. Golden = fixtures/*/expected.json."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ledger.parse import read_document
from ledger.rules import extract_rules
from ledger.schema import InvoiceFields

_FIELDS = ["emissor", "endereco", "valor", "vencimento"]
_VALOR_TOL = 0.01


def _load_pred(fixture_dir: Path, doc_path: Path) -> dict[str, Any]:
    cache_path = fixture_dir.parent.parent / "cache" / f"{fixture_dir.name}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    fields: InvoiceFields = extract_rules(read_document(str(doc_path)))
    return fields.model_dump()


def _field_match(field: str, expected: Any, pred: Any) -> bool:
    if field == "valor":
        try:
            return abs(float(pred) - float(expected)) <= _VALOR_TOL
        except (TypeError, ValueError):
            return False
    return str(pred).strip() == str(expected).strip()


def run_eval(fixtures_dir: str = "fixtures") -> dict[str, Any]:
    base = Path(fixtures_dir)
    cases = []
    field_hits = {f: 0 for f in _FIELDS}
    total_fields = 0

    for case_dir in sorted(base.iterdir()):
        expected_path = case_dir / "expected.json"
        doc_path = case_dir / "doc.md"
        if not expected_path.exists() or not doc_path.exists():
            continue
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        pred = _load_pred(case_dir, doc_path)

        mismatches = []
        for f in _FIELDS:
            ok = _field_match(f, expected.get(f), pred.get(f))
            total_fields += 1
            if ok:
                field_hits[f] += 1
            else:
                mismatches.append({"field": f, "expected": expected.get(f), "pred": pred.get(f)})

        cases.append(
            {
                "id": case_dir.name,
                "pred": pred,
                "expected": expected,
                "mismatches": mismatches,
                "ok": not mismatches,
            }
        )

    n_cases = len(cases)
    overall_accuracy = (
        sum(c["ok"] for c in cases) / n_cases if n_cases else 0.0
    )
    per_field_accuracy = {
        f: (field_hits[f] / n_cases if n_cases else 0.0) for f in _FIELDS
    }

    return {
        "cases": cases,
        "n_cases": n_cases,
        "overall_accuracy": overall_accuracy,
        "per_field_accuracy": per_field_accuracy,
    }


def render_report_md(result: dict[str, Any]) -> str:
    lines = ["# Eval Replay Report", ""]
    lines.append(f"Casos: {result['n_cases']}  ")
    lines.append(f"Accuracy geral: {result['overall_accuracy']:.2%}")
    lines.append("")
    lines.append("## Accuracy por campo")
    lines.append("")
    lines.append("| campo | accuracy |")
    lines.append("|---|---|")
    for f in _FIELDS:
        lines.append(f"| {f} | {result['per_field_accuracy'][f]:.2%} |")
    lines.append("")
    lines.append("## Mismatches")
    lines.append("")
    any_mismatch = False
    for case in result["cases"]:
        if not case["mismatches"]:
            continue
        any_mismatch = True
        lines.append(f"### {case['id']}")
        lines.append("")
        lines.append("| campo | esperado | previsto |")
        lines.append("|---|---|---|")
        for m in case["mismatches"]:
            lines.append(f"| {m['field']} | {m['expected']} | {m['pred']} |")
        lines.append("")
    if not any_mismatch:
        lines.append("Nenhum.")
        lines.append("")
    return "\n".join(lines)


def main(fixtures_dir: str = "fixtures", reports_dir: str = "reports") -> int:
    result = run_eval(fixtures_dir)
    out_dir = Path(reports_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "eval-replay.md").write_text(render_report_md(result), encoding="utf-8")
    (out_dir / "eval-replay.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        f"eval --replay: {result['n_cases']} casos, "
        f"accuracy geral {result['overall_accuracy']:.2%}"
    )
    for f in _FIELDS:
        print(f"  {f}: {result['per_field_accuracy'][f]:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
