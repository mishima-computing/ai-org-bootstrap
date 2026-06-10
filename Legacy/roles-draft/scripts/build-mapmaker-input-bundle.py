#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def bundle(objective: str) -> dict:
    return {
        "objective": objective,
        "p0_acceptance": [],
        "work_packets": [],
        "pain_points": [],
        "repo_hotspots": [],
        "complexity_observations": [],
        "critical_surfaces": [],
        "constraints": [],
        "non_goals": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Mapmaker input bundle skeleton.")
    parser.add_argument("--objective", default="", help="Objective text for the bundle.")
    parser.add_argument("--output", help="Optional output path.")
    args = parser.parse_args()

    payload = bundle(args.objective)
    rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
