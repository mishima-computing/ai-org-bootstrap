#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROLES = [
    "bootstrap-supervisor",
    "workspace-gatekeeper",
    "convergence-manager",
    "work-packet-dispatcher",
    "critical-surface-manager",
    "mapmaker-agent",
    "design-space-searcher",
    "invariant-scout",
    "experiment-designer",
    "boring-worker",
    "auth-security-implementer",
    "database-implementer",
    "production-readiness-planner",
    "codex-auditor",
    "claude-independent-auditor",
    "visual-ux-worker",
    "visual-auditor",
    "local-tooling-pod",
    "gate-report-builder",
]

REQUIRED_CODEX_AGENTS = [
    "workspace-gatekeeper",
    "convergence-manager",
    "work-packet-dispatcher",
    "critical-surface-manager",
    "mapmaker-agent",
    "experiment-designer",
    "boring-worker",
    "codex-auditor",
    "gate-report-builder",
    "production-readiness-planner",
]

REQUIRED_CLAUDE_AGENTS = [
    "critical-surface-manager",
    "mapmaker-agent",
    "design-space-searcher",
    "invariant-scout",
    "auth-security-implementer",
    "database-implementer",
    "production-readiness-planner",
    "claude-independent-auditor",
    "visual-ux-worker",
    "visual-auditor",
]

REQUIRED_ANTIGRAVITY_AGENTS = [
    "visual-ux-worker",
    "visual-auditor",
    "mapmaker-agent",
]

REQUIRED_CODEX_SKILLS = [
    "convergence",
    "critical-surface",
    "mapmaker",
    "work-packet",
    "audit",
]

REQUIRED_CLAUDE_SKILLS = [
    "critical-surface",
    "mapmaker",
    "heavy-implementation",
    "audit",
]

REQUIRED_SCHEMAS = [
    "work-packet.schema.json",
    "convergence-decision.schema.json",
    "candidate-output.schema.json",
    "audit-decision.schema.json",
    "critical-surface-decision.schema.json",
    "concept-memo.schema.json",
    "experiment-packet.schema.json",
    "gate-report.schema.json",
    "audit-bundle.schema.json",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def check_required_files() -> list[str]:
    required = [
        ROOT / "bootstrap/codex-bootstrap-v0.1.md",
        ROOT / "bootstrap/README.md",
        ROOT / ".codex/config.toml",
        ROOT / ".claude/settings.json",
    ]
    required.extend(ROOT / "roles" / f"{name}.md" for name in REQUIRED_ROLES)
    required.extend(ROOT / ".codex/agents" / f"{name}.toml" for name in REQUIRED_CODEX_AGENTS)
    required.extend(ROOT / ".claude/agents" / f"{name}.md" for name in REQUIRED_CLAUDE_AGENTS)
    required.extend(ROOT / ".antigravity/agents" / f"{name}.md" for name in REQUIRED_ANTIGRAVITY_AGENTS)
    required.extend(ROOT / ".agents/skills" / name / "SKILL.md" for name in REQUIRED_CODEX_SKILLS)
    required.extend(ROOT / ".claude/skills" / name / "SKILL.md" for name in REQUIRED_CLAUDE_SKILLS)
    required.extend(ROOT / "schemas" / name for name in REQUIRED_SCHEMAS)

    return [rel(path) for path in required if not path.is_file()]


def parse_json_files() -> list[str]:
    errors: list[str] = []
    json_paths = list((ROOT / "schemas").glob("*.json")) + [ROOT / ".claude/settings.json"]
    for path in sorted(json_paths):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report parse failure
            errors.append(f"{rel(path)}: {exc}")
    return errors


def parse_toml_files() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        import tomllib
    except ModuleNotFoundError:
        return errors, ["tomllib unavailable; skipped TOML parse"]

    toml_paths = [ROOT / ".codex/config.toml"] + sorted((ROOT / ".codex/agents").glob("*.toml"))
    for path in toml_paths:
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report parse failure
            errors.append(f"{rel(path)}: {exc}")
    return errors, warnings


def main() -> int:
    missing = check_required_files()
    json_errors = parse_json_files()
    toml_errors, warnings = parse_toml_files()
    errors = []
    errors.extend(f"missing: {item}" for item in missing)
    errors.extend(f"json_parse_error: {item}" for item in json_errors)
    errors.extend(f"toml_parse_error: {item}" for item in toml_errors)

    payload = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "required_counts": {
            "roles": len(REQUIRED_ROLES),
            "codex_agents": len(REQUIRED_CODEX_AGENTS),
            "claude_agents": len(REQUIRED_CLAUDE_AGENTS),
            "antigravity_agents": len(REQUIRED_ANTIGRAVITY_AGENTS),
            "codex_skills": len(REQUIRED_CODEX_SKILLS),
            "claude_skills": len(REQUIRED_CLAUDE_SKILLS),
            "schemas": len(REQUIRED_SCHEMAS),
        },
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
