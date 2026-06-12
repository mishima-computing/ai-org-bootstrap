#!/usr/bin/env python3
"""Controller-run anchor URL liveness check.

Exit codes:
0 all checked URLs returned HTTP 200.
1 at least one URL returned a hard non-200 response.
2 network unavailable or transport failure prevented a reliable sweep.
3 every non-200 response was a documented bot-block class response.
"""
from __future__ import annotations

import argparse
import json
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANCHORS_DIR = ROOT / ".agent-org/knowledge/ui/anchors"
POINTER_PREFIX = "Pointer: "
BOT_BLOCK_HOSTS = {"search.worldcat.org"}
BOT_BLOCK_STATUS = {403, 429}


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme not in {"http", "https"}:
            raise urllib.error.URLError(f"blocked redirect scheme: {parsed.scheme}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def discover_pointers(anchors_dir: Path) -> list[dict[str, object]]:
    pointers: list[dict[str, object]] = []
    for path in sorted(anchors_dir.glob("*.md")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith(POINTER_PREFIX):
                continue
            raw_url = stripped[len(POINTER_PREFIX):].split("|", 1)[0].strip()
            parsed = urllib.parse.urlparse(raw_url)
            if parsed.scheme not in {"http", "https"}:
                continue
            pointers.append({
                "path": rel(path),
                "line": line_number,
                "url": raw_url,
                "host": parsed.netloc.lower(),
            })
    return pointers


def classify_status(url: str, status: int) -> str:
    host = urllib.parse.urlparse(url).netloc.lower()
    if status == 200:
        return "ok"
    if status in BOT_BLOCK_STATUS and host in BOT_BLOCK_HOSTS:
        return "bot_block"
    return "hard_non_200"


def exit_code(results: list[dict[str, object]]) -> int:
    classes = {str(item["class"]) for item in results}
    if "hard_non_200" in classes:
        return 1
    if "network_unavailable" in classes:
        return 2
    if "bot_block" in classes:
        return 3
    return 0


def status_for_exit(code: int) -> str:
    return {
        0: "pass",
        1: "hard_non_200",
        2: "network_unavailable",
        3: "bot_block",
    }[code]


def fetch_url(opener: urllib.request.OpenerDirector, url: str, timeout: float) -> tuple[int | None, str, str | None]:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "ai-org-bootstrap-anchor-liveness/1.0"},
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            return int(response.status), classify_status(url, int(response.status)), None
    except urllib.error.HTTPError as exc:
        return int(exc.code), classify_status(url, int(exc.code)), None
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        return None, "network_unavailable", exc.__class__.__name__


def run_check(timeout: float) -> tuple[int, dict[str, object]]:
    opener = urllib.request.build_opener(SafeRedirectHandler)
    results: list[dict[str, object]] = []
    for pointer in discover_pointers(ANCHORS_DIR):
        status, result_class, error = fetch_url(opener, str(pointer["url"]), timeout)
        item = dict(pointer)
        item.update({
            "status": status,
            "class": result_class,
        })
        if error:
            item["error"] = error
        results.append(item)

    code = exit_code(results)
    return code, {
        "status": status_for_exit(code),
        "exit_code": code,
        "checked_count": len(results),
        "results": results,
    }


def run_self_test() -> tuple[int, dict[str, object]]:
    fixtures = [
        {
            "name": "all_200",
            "expected_exit": 0,
            "results": [{"url": "https://example.com/a", "class": "ok"}],
        },
        {
            "name": "hard_non_200",
            "expected_exit": 1,
            "results": [{"url": "https://example.com/missing", "class": "hard_non_200"}],
        },
        {
            "name": "network_unavailable",
            "expected_exit": 2,
            "results": [{"url": "https://example.com/down", "class": "network_unavailable"}],
        },
        {
            "name": "bot_block_only",
            "expected_exit": 3,
            "results": [
                {"url": "https://example.com/ok", "class": "ok"},
                {"url": "https://search.worldcat.org/isbn/9780961392147", "class": "bot_block"},
            ],
        },
    ]
    cases: list[dict[str, object]] = []
    failed = False
    for fixture in fixtures:
        actual = exit_code(fixture["results"])
        passed = actual == fixture["expected_exit"]
        failed = failed or not passed
        cases.append({
            "name": fixture["name"],
            "expected_exit": fixture["expected_exit"],
            "actual_exit": actual,
            "passed": passed,
        })
    code = 1 if failed else 0
    return code, {
        "status": "pass" if code == 0 else "fail",
        "exit_code": code,
        "cases": cases,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="GET anchor pointers and report controller-run liveness as JSON.",
        epilog="Exit 0 all 200; 1 hard non-200; 2 network unavailable; 3 only bot-block-class 403/429 from documented hosts.",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds.")
    parser.add_argument("--self-test", action="store_true", help="Run offline classifier fixtures without network.")
    args = parser.parse_args(argv)

    code, payload = run_self_test() if args.self_test else run_check(args.timeout)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
