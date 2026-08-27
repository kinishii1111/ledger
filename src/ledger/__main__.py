from __future__ import annotations

import argparse
import json
import sys

from ledger import __version__
from ledger.schema import InvoiceFields


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ledger",
        description="Document → validated JSON + eval harness (agent-first)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="cmd")

    p_schema = sub.add_parser("schema", help="Print JSON Schema of invoice fields")
    p_schema.add_argument("--example", action="store_true", help="Print example instance")

    # stubs for later fatias — help already documents the roadmap
    sub.add_parser("extract", help="(F1.2+) extract fields from a document")
    sub.add_parser("eval", help="(F1.4+) run eval harness")

    args = parser.parse_args(argv)

    if args.cmd is None:
        parser.print_help()
        return 0

    if args.cmd == "schema":
        if args.example:
            ex = InvoiceFields(
                emissor="Acme Supplies Ltda",
                endereco="12.345.678/0001-90",
                valor=1500.0,
                vencimento="2026-09-15",
            )
            print(ex.model_dump_json(indent=2))
        else:
            print(json.dumps(InvoiceFields.model_json_schema(), indent=2))
        return 0

    if args.cmd in {"extract", "eval"}:
        print(f"{args.cmd}: not implemented yet (see FASES / ORDEM)", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
