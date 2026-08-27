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

    p_extract = sub.add_parser("extract", help="Extract fields from a document")
    p_extract.add_argument("path", help="path to .md/.txt document")
    p_extract.add_argument(
        "--rules",
        action="store_true",
        help="use offline regex/rules extractor (default when no other backend)",
    )

    p_eval = sub.add_parser("eval", help="run eval harness")
    p_eval.add_argument(
        "--replay",
        action="store_true",
        help="offline replay against fixtures/*/expected.json (no LLM)",
    )

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

    if args.cmd == "extract":
        from ledger.parse import read_document
        from ledger.rules import extract_rules

        try:
            text = read_document(args.path)
            fields = extract_rules(text)
        except (OSError, ValueError) as e:
            print(f"extract: {e}", file=sys.stderr)
            return 2
        print(fields.model_dump_json(indent=2))
        return 0

    if args.cmd == "eval":
        if not args.replay:
            print("eval: use --replay (only mode implemented)", file=sys.stderr)
            return 2
        from ledger.eval_run import main as eval_main

        try:
            return eval_main()
        except (OSError, ValueError) as e:
            print(f"eval: {e}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
