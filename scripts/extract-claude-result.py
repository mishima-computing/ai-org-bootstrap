#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> int:
    print(json.dumps({"status": "fail", "error": message}, ensure_ascii=False), file=sys.stderr)
    return 1


def parse_json_object(value: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        parsed = json.loads(value)
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)
    if not isinstance(parsed, dict):
        return None, "parsed_result_must_be_object"
    return parsed, None


def salvage_json_object(value: str) -> tuple[dict[str, Any] | None, str | None]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(value):
        if char != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(value[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed, None
    return None, "no_json_object_found"


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

    if envelope.get("is_error") is True:
        return fail(f"carrier_error: {envelope.get('result', 'unknown_error')}")

    if "result" not in envelope:
        return fail("cli_output_missing_result")

    result = envelope["result"]
    extraction_mode = "result"
    if isinstance(result, str):
        extracted, parse_error = parse_json_object(result)
        if extracted is None:
            extracted, salvage_error = salvage_json_object(result)
            if extracted is not None:
                extraction_mode = "result_salvaged"
            elif isinstance(envelope.get("structured_output"), dict):
                extracted = envelope["structured_output"]
                extraction_mode = "structured_output_fallback"
            else:
                return fail(f"result_field_is_not_json: {parse_error}; salvage_error: {salvage_error}")
    elif isinstance(result, dict):
        extracted = result
    else:
        structured_output = envelope.get("structured_output")
        if isinstance(structured_output, dict):
            extracted = structured_output
            extraction_mode = "structured_output_fallback"
        else:
            return fail("result_field_must_be_json_object_or_json_string")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(extracted, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "out": str(out_path), "extraction_mode": extraction_mode}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
