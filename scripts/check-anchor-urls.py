#!/usr/bin/env python3
"""Controller-run anchor URL liveness check.

Exit codes:
0 all checked URLs returned HTTP 200.
1 at least one URL returned a hard non-200 response.
2 network unavailable or transport failure prevented a reliable sweep.
3 every non-200 response was a documented bot-block class response; controller consumers treat this as recorded pass semantics, not silent success.
"""
from __future__ import annotations

import argparse
import http.client
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
BROWSER_CLASS_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BOT_BLOCK_HOSTS = {"doi.org", "search.worldcat.org"}
BOT_BLOCK_STATUS = {403, 429}


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme not in {"http", "https"}:
            raise urllib.error.URLError(f"blocked redirect scheme: {parsed.scheme}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class BrowserHTTPConnection(http.client.HTTPConnection):
    _http_vsn = 11
    _http_vsn_str = "HTTP/1.1"


class BrowserHTTPSConnection(http.client.HTTPSConnection):
    _http_vsn = 11
    _http_vsn_str = "HTTP/1.1"


class BrowserHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(BrowserHTTPConnection, req)


class BrowserHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(BrowserHTTPSConnection, req)


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


def build_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": BROWSER_CLASS_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "close",
        },
    )


def build_opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(
        SafeRedirectHandler,
        BrowserHTTPHandler,
        BrowserHTTPSHandler,
    )


def fetch_url(opener: urllib.request.OpenerDirector, url: str, timeout: float) -> tuple[int | None, str, str | None]:
    request = build_request(url)
    try:
        with opener.open(request, timeout=timeout) as response:
            return int(response.status), classify_status(url, int(response.status)), None
    except urllib.error.HTTPError as exc:
        return int(exc.code), classify_status(url, int(exc.code)), None
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        return None, "network_unavailable", exc.__class__.__name__


def run_check(timeout: float) -> tuple[int, dict[str, object]]:
    opener = build_opener()
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
        {
            "name": "doi_bot_block_only",
            "expected_exit": 3,
            "results": [
                {"url": "https://doi.org/10.1145/3491102.3517642", "class": classify_status("https://doi.org/10.1145/3491102.3517642", 403)},
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
    request = build_request("https://example.com/")
    ua_passed = request.get_header("User-agent") == BROWSER_CLASS_UA
    http_passed = (
        BrowserHTTPConnection._http_vsn_str == "HTTP/1.1"
        and BrowserHTTPSConnection._http_vsn_str == "HTTP/1.1"
    )
    failed = failed or not ua_passed or not http_passed
    cases.extend([
        {
            "name": "browser_class_user_agent",
            "expected_exit": 0,
            "actual_exit": 0 if ua_passed else 1,
            "passed": ua_passed,
        },
        {
            "name": "http_1_1_request_profile",
            "expected_exit": 0,
            "actual_exit": 0 if http_passed else 1,
            "passed": http_passed,
        },
    ])
    code = 1 if failed else 0
    return code, {
        "status": "pass" if code == 0 else "fail",
        "exit_code": code,
        "cases": cases,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="GET anchor pointers and report controller-run liveness as JSON.",
        epilog="Exit 0 all 200; 1 hard non-200; 2 network unavailable; 3 only bot-block-class 403/429 from documented hosts; exit 3 is recorded pass semantics for controller liveness.",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds.")
    parser.add_argument("--self-test", action="store_true", help="Run offline classifier fixtures without network.")
    args = parser.parse_args(argv)

    code, payload = run_self_test() if args.self_test else run_check(args.timeout)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
