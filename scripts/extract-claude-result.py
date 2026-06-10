#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def fail(message: str) -> int:
    print(json.dumps({"status": "fail", "error": message}, ensure_ascii=False), file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract role JSON from Claude CLI JSON output.")
    parser.add_argument("--cli-output", required=True, help="Claude --output-format json file.")
    parser.add_argument("--out", required=True, help="Destination for extracted role JSON.")
    args = parser.parse_args()

    cli_output_path = Path(args.cli_output)
    out_path = Path(args.out)

    try:
        envelope = json.loads(cli_output_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return fail(f"cli_output_parse_error: {exc}")

    if not isinstance(envelope, dict):
        return fail("cli_output_must_be_object")

    if envelope.get("type") != "result":
        return fail("cli_output_type_must_be_result")

    if "result" not in envelope:
        return fail("cli_output_missing_result")

    result = envelope["result"]
    if isinstance(result, str):
        try:
            extracted = json.loads(result)
        except Exception as exc:  # noqa: BLE001
            return fail(f"result_field_is_not_json: {exc}")
    elif isinstance(result, dict):
        extracted = result
    else:
        return fail("result_field_must_be_json_object_or_json_string")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(extracted, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "out": str(out_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
