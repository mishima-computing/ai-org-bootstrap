#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRECEDENTS_DIR = ROOT / ".agent-org/knowledge/review/precedents"
STRING_LIMIT = 200
CAPS = {
    "selected_precedent_cards": 8,
    "selection_warnings": 6,
    "knowledge_gaps": 6,
}


def clean_string(value: object) -> str:
    text = " ".join(str(value).strip().split())
    return text[:STRING_LIMIT]


def cap_ordered(values: list[str], name: str, warnings: list[str]) -> list[str]:
    cleaned = list(dict.fromkeys(clean_string(value) for value in values if clean_string(value)))
    limit = CAPS[name]
    if len(cleaned) > limit:
        warnings.append(clean_string(f"{name} truncated from {len(cleaned)} to {limit} items"))
    return cleaned[:limit]


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end_index = lines[1:].index("---") + 1
    except ValueError:
        return {}
    frontmatter: dict[str, str] = {}
    for line in lines[1:end_index]:
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def precedent_cards(cards_dir: Path = PRECEDENTS_DIR) -> list[Path]:
    if not cards_dir.is_dir():
        return []
    return [
        path
        for path in sorted(cards_dir.glob("*.md"))
        if path.name != "README.md"
    ]


def keys_for_card(frontmatter: dict[str, str]) -> list[str]:
    keys: list[str] = []
    for item in frontmatter.get("lens_nn_map", "").split(";"):
        item = item.strip()
        if not item or ":" not in item:
            continue
        lens, nn_class = [part.strip() for part in item.split(":", 1)]
        if lens:
            keys.append(lens)
        if nn_class:
            keys.append(nn_class)
        if lens and nn_class:
            keys.append(f"{lens}:{nn_class}")
    return sorted(dict.fromkeys(keys))


def matching_cards(cards: list[Path], supplied_key: str) -> list[str]:
    selected: list[str] = []
    for card in cards:
        frontmatter = parse_frontmatter(card)
        if supplied_key in keys_for_card(frontmatter):
            selected.append(card.relative_to(ROOT).as_posix())
    return selected


def select(supplied_key: str, cards_dir: Path = PRECEDENTS_DIR) -> dict[str, object]:
    warnings: list[str] = []
    gaps: list[str] = []
    key = clean_string(supplied_key)
    cards = precedent_cards(cards_dir)
    selected = matching_cards(cards, key)
    if not cards:
        gaps.append("No precedent cards were found under .agent-org/knowledge/review/precedents/.")
    elif not selected:
        gaps.append(f"No local precedent card matched supplied review key: {key}. Fall through to web long-tail lookup.")
    return {
        "knowledge_gaps": cap_ordered(gaps, "knowledge_gaps", warnings),
        "selected_precedent_cards": cap_ordered(selected, "selected_precedent_cards", warnings),
        "selection_key": key,
        "selection_warnings": cap_ordered(warnings, "selection_warnings", []),
    }


def run_self_test() -> int:
    errors: list[str] = []
    nn4 = set(select("NN4")["selected_precedent_cards"])
    expected_nn4 = {
        ".agent-org/knowledge/review/precedents/do-not-break-userspace.md",
        ".agent-org/knowledge/review/precedents/regression-burden.md",
    }
    if nn4 != expected_nn4:
        errors.append(f"NN4 selected_precedent_cards expected {sorted(expected_nn4)} got {sorted(nn4)}")

    combined = set(select("other:none")["selected_precedent_cards"])
    expected_combined = {".agent-org/knowledge/review/precedents/tone-step-back.md"}
    if combined != expected_combined:
        errors.append(f"other:none selected_precedent_cards expected {sorted(expected_combined)} got {sorted(combined)}")

    gap_result = select("forgeability:NN2")
    if gap_result["selected_precedent_cards"] or not gap_result["knowledge_gaps"]:
        errors.append("gap report missing for unmatched supplied key")

    payload = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return 0 if not errors else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Select local Linon review precedent cards from a supplied review-time key.")
    parser.add_argument("--key", help="Supplied review-time key: lens, NN class, or lens:NN-class.")
    parser.add_argument("--self-test", action="store_true", help="Run offline deterministic selector self-test.")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if not args.key:
        parser.error("--key is required unless --self-test is used")

    sys.stdout.write(json.dumps(select(args.key), ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
