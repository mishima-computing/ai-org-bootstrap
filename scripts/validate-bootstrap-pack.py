#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FINAL_AGENTS = [
    "functional-ci-action-writer",
    "security-ci-action-writer",
    "nonfunctional-ci-action-writer",
    "aggressive-designer",
    "conservative-designer",
    "genius",
    "aufheben-designer",
    "implementer",
]

CODEX_ADAPTERS = [
    "functional-ci-action-writer",
    "nonfunctional-ci-action-writer",
    "conservative-designer",
    "implementer",
]

CLAUDE_ADAPTERS = [
    "security-ci-action-writer",
    "aggressive-designer",
    "genius",
    "aufheben-designer",
    "implementer",
]

REQUIRED_SCHEMAS = [
    "ci-action-writer-result.schema.json",
    "design-proposal.schema.json",
    "genius-packet.schema.json",
    "implementation-contract.schema.json",
    "implementation-result.schema.json",
]

ROLE_HEADINGS = [
    "# Role:",
    "## Purpose",
    "## Primary Carrier",
    "## Secondary Carrier",
    "## Authority",
    "## Forbidden Actions",
    "## Inputs",
    "## Required Output",
    "## Stop Conditions",
    "## Evidence Requirements",
    "## Interaction With Other Roles",
    "## Anti-patterns",
    "## Notes For Carrier Adapters",
]

SCHEMA_BY_AGENT = {
    "functional-ci-action-writer": "schemas/ci-action-writer-result.schema.json",
    "security-ci-action-writer": "schemas/ci-action-writer-result.schema.json",
    "nonfunctional-ci-action-writer": "schemas/ci-action-writer-result.schema.json",
    "aggressive-designer": "schemas/design-proposal.schema.json",
    "conservative-designer": "schemas/design-proposal.schema.json",
    "genius": "schemas/genius-packet.schema.json",
    "aufheben-designer": "schemas/implementation-contract.schema.json",
    "implementer": "schemas/implementation-result.schema.json",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def contains_all(content: str, phrases: list[str]) -> list[str]:
    lowered = content.lower()
    return [phrase for phrase in phrases if phrase.lower() not in lowered]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str, str | None]:
    lines = text(path).splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text(path), "missing opening frontmatter fence"
    try:
        end_index = lines[1:].index("---") + 1
    except ValueError:
        return {}, text(path), "missing closing frontmatter fence"
    frontmatter: dict[str, str] = {}
    for line in lines[1:end_index]:
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
    body = "\n".join(lines[end_index + 1 :])
    return frontmatter, body, None


def parse_json_files() -> list[str]:
    errors: list[str] = []
    schema_ids: dict[str, str] = {}
    for path in sorted((ROOT / "schemas").glob("*.json")):
        try:
            parsed = json.loads(text(path))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel(path)}: {exc}")
            continue
        schema_id = parsed.get("$id")
        if schema_id:
            if schema_id in schema_ids:
                errors.append(f"duplicate_schema_id: {schema_id} in {schema_ids[schema_id]} and {rel(path)}")
            schema_ids[schema_id] = rel(path)
    settings = ROOT / ".claude/settings.json"
    if settings.is_file():
        try:
            json.loads(text(settings))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel(settings)}: {exc}")
    return errors


def load_toml(paths: list[Path]) -> tuple[dict[Path, dict], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    parsed: dict[Path, dict] = {}
    try:
        import tomllib
    except ModuleNotFoundError:
        warnings.append("tomllib unavailable; skipped TOML parse")
        return parsed, errors, warnings
    for path in paths:
        try:
            parsed[path] = tomllib.loads(text(path))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel(path)}: {exc}")
    return parsed, errors, warnings


def check_required_files() -> list[str]:
    required = [
        ROOT / "bootstrap/codex-bootstrap.md",
        ROOT / "bootstrap/README.md",
        ROOT / ".agent-org/runtime-registry.yaml",
        ROOT / ".agent-org/execution-substrate.md",
        ROOT / ".agent-org/worktree-policy.md",
        ROOT / ".agent-org/artifact-policy.md",
        ROOT / ".agent-org/pack-materialization.md",
        ROOT / ".agent-org/carrier-invocation.md",
        ROOT / ".agent-org/run-lifecycle.md",
        ROOT / ".codex/config.toml",
        ROOT / ".claude/settings.json",
        ROOT / "scripts/run-gates.sh",
        ROOT / "scripts/hash-artifacts.py",
        ROOT / "scripts/validate-bootstrap-pack.py",
    ]
    required.extend(ROOT / "roles" / f"{agent}.md" for agent in FINAL_AGENTS)
    required.extend(ROOT / ".codex/agents" / f"{agent}.toml" for agent in CODEX_ADAPTERS)
    required.extend(ROOT / ".claude/agents" / f"{agent}.md" for agent in CLAUDE_ADAPTERS)
    required.extend(ROOT / "schemas" / name for name in REQUIRED_SCHEMAS)
    return [rel(path) for path in required if not path.is_file()]


def check_active_directories() -> list[str]:
    errors: list[str] = []
    role_files = sorted(path.stem for path in (ROOT / "roles").glob("*.md"))
    if role_files != sorted(FINAL_AGENTS):
        errors.append(f"roles directory must contain only final agents: {role_files}")
    codex_files = sorted(path.stem for path in (ROOT / ".codex/agents").glob("*.toml"))
    if codex_files != sorted(CODEX_ADAPTERS):
        errors.append(f".codex/agents must contain only expected adapters: {codex_files}")
    claude_files = sorted(path.stem for path in (ROOT / ".claude/agents").glob("*.md"))
    if claude_files != sorted(CLAUDE_ADAPTERS):
        errors.append(f".claude/agents must contain only expected adapters: {claude_files}")
    antigravity_files = sorted(path.name for path in (ROOT / ".antigravity/agents").glob("*.md"))
    if antigravity_files:
        errors.append(f".antigravity/agents must not contain active adapters: {antigravity_files}")
    return errors


def check_roles() -> list[str]:
    errors: list[str] = []
    for agent in FINAL_AGENTS:
        path = ROOT / "roles" / f"{agent}.md"
        if not path.is_file():
            continue
        content = text(path)
        for heading in ROLE_HEADINGS:
            if heading not in content:
                errors.append(f"{rel(path)} missing heading: {heading}")
        schema = SCHEMA_BY_AGENT[agent]
        if schema not in content:
            errors.append(f"{rel(path)} must reference {schema}")
        if "adoption" not in content.lower():
            errors.append(f"{rel(path)} must prohibit adoption claims")
    workflow_agents = [
        "functional-ci-action-writer",
        "security-ci-action-writer",
        "nonfunctional-ci-action-writer",
    ]
    for agent in workflow_agents:
        content = text(ROOT / "roles" / f"{agent}.md")
        for phrase in [".github/workflows/**", "Do not invent commands", "package manifests", "branch protection"]:
            if phrase.lower() not in content.lower():
                errors.append(f"roles/{agent}.md missing CI writer phrase: {phrase}")
    for agent in ["aggressive-designer", "conservative-designer", "genius"]:
        content = text(ROOT / "roles" / f"{agent}.md")
        for phrase in ["Outputs only to `aufheben-designer`", "directly instruct `implementer`"]:
            if phrase.lower() not in content.lower():
                errors.append(f"roles/{agent}.md missing designer boundary: {phrase}")
    return errors


def check_codex_adapters(toml_data: dict[Path, dict]) -> list[str]:
    errors: list[str] = []
    required_keys = {"name", "description", "model_reasoning_effort", "sandbox_mode", "developer_instructions"}
    for agent in CODEX_ADAPTERS:
        path = ROOT / ".codex/agents" / f"{agent}.toml"
        parsed = toml_data.get(path)
        if parsed is None:
            errors.append(f"{rel(path)} was not parsed")
            continue
        for key in sorted(required_keys - set(parsed)):
            errors.append(f"{rel(path)} missing TOML key: {key}")
        if parsed.get("model_reasoning_effort") != "high":
            errors.append(f"{rel(path)} model_reasoning_effort must be high")
        expected_sandbox = "workspace-write" if agent in {
            "functional-ci-action-writer",
            "nonfunctional-ci-action-writer",
            "implementer",
        } else "read-only"
        if parsed.get("sandbox_mode") != expected_sandbox:
            errors.append(f"{rel(path)} sandbox_mode must be {expected_sandbox}")
        instructions = str(parsed.get("developer_instructions", ""))
        if f"roles/{agent}.md" not in instructions:
            errors.append(f"{rel(path)} must reference roles/{agent}.md")
        if SCHEMA_BY_AGENT[agent] not in instructions:
            errors.append(f"{rel(path)} must reference {SCHEMA_BY_AGENT[agent]}")
        if "No adoption authority" not in instructions:
            errors.append(f"{rel(path)} must state no adoption authority")
    return errors


def check_claude_adapters() -> list[str]:
    errors: list[str] = []
    required_keys = {"name", "description", "tools", "model", "permissionMode"}
    for agent in CLAUDE_ADAPTERS:
        path = ROOT / ".claude/agents" / f"{agent}.md"
        frontmatter, body, error = parse_frontmatter(path)
        if error:
            errors.append(f"{rel(path)} {error}")
            continue
        for key in sorted(required_keys - set(frontmatter)):
            errors.append(f"{rel(path)} missing frontmatter key: {key}")
        if f"roles/{agent}.md" not in body:
            errors.append(f"{rel(path)} must reference roles/{agent}.md")
        if SCHEMA_BY_AGENT[agent] not in body:
            errors.append(f"{rel(path)} must reference {SCHEMA_BY_AGENT[agent]}")
        if "No adoption authority" not in body:
            errors.append(f"{rel(path)} must state no adoption authority")
        tools = frontmatter.get("tools", "")
        read_only_agents = {"aggressive-designer", "genius", "aufheben-designer"}
        if agent in read_only_agents and ("Edit" in tools or "Write" in tools):
            errors.append(f"{rel(path)} read-only agent must not include Edit or Write")
        if agent == "security-ci-action-writer" and frontmatter.get("model") != "fable":
            errors.append(f"{rel(path)} model must be fable")
    return errors


def check_registry() -> list[str]:
    errors: list[str] = []
    path = ROOT / ".agent-org/runtime-registry.yaml"
    content = text(path)
    for agent in FINAL_AGENTS:
        if f"  {agent}:" not in content:
            errors.append(f"{rel(path)} missing agent: {agent}")
    for phrase in ["protocol:", "codex-main-controller", "subsystems:", "local-tooling", "gate-reporting", "artifact-hashing"]:
        if phrase not in content:
            errors.append(f"{rel(path)} missing registry phrase: {phrase}")
    return errors


def check_bootstrap() -> list[str]:
    errors: list[str] = []
    path = ROOT / "bootstrap/codex-bootstrap.md"
    content = text(path)
    for agent in FINAL_AGENTS:
        if agent not in content:
            errors.append(f"{rel(path)} missing agent: {agent}")
    for phrase in [
        "Codex main is the execution controller",
        ".github/workflows/**",
        "schemas/implementation-contract.schema.json",
        "schemas/implementation-result.schema.json",
    ]:
        if phrase not in content:
            errors.append(f"{rel(path)} missing phrase: {phrase}")
    return errors


def main() -> int:
    toml_paths = [ROOT / ".codex/config.toml"] + sorted((ROOT / ".codex/agents").glob("*.toml"))
    toml_data, toml_errors, warnings = load_toml(toml_paths)

    errors: list[str] = []
    errors.extend(f"missing: {item}" for item in check_required_files())
    errors.extend(f"json_parse_error: {item}" for item in parse_json_files())
    errors.extend(f"toml_parse_error: {item}" for item in toml_errors)
    errors.extend(check_active_directories())
    errors.extend(check_roles())
    errors.extend(check_codex_adapters(toml_data))
    errors.extend(check_claude_adapters())
    errors.extend(check_registry())
    errors.extend(check_bootstrap())

    payload = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
