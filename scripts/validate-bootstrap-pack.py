#!/usr/bin/env python3
from __future__ import annotations

import json
import argparse
import re
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

SCHEMA_SAMPLE_INSTANCES = {
    "schemas/ci-action-writer-result.schema.json": {
        "role_id": "functional-ci-action-writer",
        "detected_ecosystem": [],
        "workflows_read": [],
        "workflows_changed": [],
        "commands_added": [],
        "commands_already_present": [],
        "checks_added": [],
        "checks_already_present": [],
        "gaps": [],
        "files_changed": [],
    },
    "schemas/design-proposal.schema.json": {
        "role_id": "aggressive-designer",
        "objective": "example objective",
        "proposal_summary": "example summary",
        "recommended_direction": "example direction",
        "expected_benefits": [],
        "risks": [],
        "assumptions": [],
        "constraints": [],
        "things_to_avoid": [],
        "handoff_notes": "example handoff",
    },
    "schemas/genius-packet.schema.json": {
        "role_id": "genius",
        "objective": "example objective",
        "substrate_inputs": [
            {
                "ref_type": "repo_pointer",
                "locator": "roles/genius.md",
                "summary": "Example local role pointer.",
            }
        ],
        "official_spec_evidence": [
            {
                "ref_type": "official_spec",
                "locator": "https://example.com/spec",
                "summary": "Example named-interface specification evidence.",
            }
        ],
        "repo_evidence": [
            {
                "ref_type": "repo_pointer",
                "locator": "schemas/genius-packet.schema.json",
                "summary": "Example schema pointer.",
            }
        ],
        "kept_hypotheses": [
            {
                "hypothesis_id": "H1",
                "mechanism": "Use pointer-style evidence to keep handoff compact.",
                "score": 0.82,
                "verification_status": "confirmed",
                "repo_evidence_refs": [
                    {
                        "ref_type": "repo_pointer",
                        "locator": "roles/genius.md",
                        "summary": "Example role evidence reference.",
                    }
                ],
                "external_refs": [
                    {
                        "ref_type": "official_spec",
                        "locator": "https://example.com/spec",
                        "summary": "Example external verification reference.",
                    }
                ],
                "expected_benefit": "Example benefit.",
                "risks": [
                    "Example risk."
                ],
                "rejection_conditions": [
                    "Reject if localized evidence is absent."
                ],
                "what_not_to_copy": [
                    "Do not copy unrelated implementation bodies."
                ],
            }
        ],
        "refuted_hypotheses": [],
        "unverified_hypotheses": [],
        "what_not_to_copy": [
            "Do not perform search-first idea gathering."
        ],
        "handoff_to_aufheben": "example handoff",
    },
    "schemas/implementation-contract.schema.json": {
        "role_id": "aufheben-designer",
        "contract_id": "contract-example",
        "objective": "example objective",
        "selected_direction": "example direction",
        "rejected_parts": [
            {
                "source": "aggressive-designer",
                "rejected_part": "example rejected part",
                "reason": "example reason",
            }
        ],
        "implementation_summary": "example summary",
        "acceptance_criteria": [],
        "files_allowed_to_change": [],
        "files_not_allowed_to_change": [],
        "required_checks": [],
        "security_requirements": [],
        "nonfunctional_requirements": [],
        "non_goals": [],
        "risks": [],
        "fallback_plan": "example fallback",
        "handoff_to_implementer": "example handoff",
    },
    "schemas/implementation-result.schema.json": {
        "role_id": "implementer",
        "implementation_contract_id": "contract-example",
        "summary": "example summary",
        "files_changed": [],
        "commands_run": [],
        "command_results": [
            {
                "command": "true",
                "exit_code": 0,
                "result": "pass",
            }
        ],
        "checks_passed": [],
        "checks_failed": [],
        "remaining_failures": [],
        "scope_deviations": [],
        "manual_followup": [],
    },
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


def load_json(path: Path) -> tuple[object | None, str | None]:
    try:
        return json.loads(text(path)), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def matches_json_type(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_schema_instance(schema: dict, instance: object, path: str = "$") -> list[str]:
    errors: list[str] = []

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}")

    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(matches_json_type(instance, item) for item in expected_type):
            errors.append(f"{path}: expected type {expected_type!r}")
            return errors
    elif isinstance(expected_type, str):
        if not matches_json_type(instance, expected_type):
            errors.append(f"{path}: expected type {expected_type}")
            return errors

    if isinstance(instance, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    errors.append(f"{path}: missing required field {key}")

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, subschema in properties.items():
                if key in instance and isinstance(subschema, dict):
                    errors.extend(validate_schema_instance(subschema, instance[key], f"{path}.{key}"))

            if schema.get("additionalProperties") is False:
                for key in instance:
                    if key not in properties:
                        errors.append(f"{path}: additional property {key} is not allowed")

    if isinstance(instance, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                errors.extend(validate_schema_instance(item_schema, item, f"{path}[{index}]"))

    pattern = schema.get("pattern")
    if isinstance(pattern, str) and isinstance(instance, str):
        if not re.search(pattern, instance):
            errors.append(f"{path}: string does not match pattern {pattern!r}")

    return errors


def check_schema_samples() -> list[str]:
    errors: list[str] = []
    for rel_schema, sample in SCHEMA_SAMPLE_INSTANCES.items():
        schema_path = ROOT / rel_schema
        loaded, error = load_json(schema_path)
        if error or not isinstance(loaded, dict):
            errors.append(f"{rel_schema}: cannot load schema for required-field validation")
            continue

        sample_errors = validate_schema_instance(loaded, sample)
        for item in sample_errors:
            errors.append(f"{rel_schema}: sample invalid: {item}")

        required = loaded.get("required", [])
        if isinstance(required, list) and required:
            missing_sample = dict(sample)
            missing_sample.pop(required[0], None)
            missing_errors = validate_schema_instance(loaded, missing_sample)
            if not missing_errors:
                errors.append(f"{rel_schema}: required field validation did not fail for {required[0]}")
    return errors


def resolve_cli_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def validate_instance_cli(schema_arg: str, instance_arg: str) -> int:
    schema_path = resolve_cli_path(schema_arg)
    instance_path = resolve_cli_path(instance_arg)

    errors: list[str] = []
    schema, schema_error = load_json(schema_path)
    instance, instance_error = load_json(instance_path)

    if schema_error or not isinstance(schema, dict):
        errors.append(f"{schema_arg}: schema_parse_error: {schema_error or 'schema must be object'}")
    if instance_error:
        errors.append(f"{instance_arg}: json_parse_error: {instance_error}")

    if not errors and isinstance(schema, dict):
        errors.extend(validate_schema_instance(schema, instance))

    payload = {
        "status": "pass" if not errors else "fail",
        "schema": schema_arg,
        "instance": instance_arg,
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


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
        ROOT / "scripts/extract-claude-result.py",
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
        if agent in read_only_agents and any(tool in tools for tool in ["Bash", "Edit", "Write"]):
            errors.append(f"{rel(path)} read-only agent must not include Bash, Edit, or Write")
        if agent == "security-ci-action-writer" and frontmatter.get("model") != "fable":
            errors.append(f"{rel(path)} model must be fable")
        elif agent != "security-ci-action-writer" and frontmatter.get("model") != "inherit":
            errors.append(f"{rel(path)} model must be inherit")
        if frontmatter.get("model") == "default":
            errors.append(f"{rel(path)} model must not be default")
        if agent == "genius":
            for tool in ["WebSearch", "WebFetch"]:
                if tool not in tools:
                    errors.append(f"{rel(path)} missing external research tool: {tool}")
            if "verification_status" not in body:
                errors.append(f"{rel(path)} must define verification_status behavior")
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


def check_pack_policies(toml_data: dict[Path, dict]) -> list[str]:
    errors: list[str] = []

    codex_config = toml_data.get(ROOT / ".codex/config.toml", {})
    if "skills" in codex_config:
        errors.append(".codex/config.toml must not use bare [skills] enabled config")

    carrier = text(ROOT / ".agent-org/carrier-invocation.md")
    for phrase in [
        "codex exec",
        "developer_instructions",
        "--agent \"<agent>\"",
        "cli-output.json",
        "result.json",
        "scripts/extract-claude-result.py",
        "claude_api_unreachable",
        "claude_auth_unavailable",
        "Claude carrier requires network access",
        "structured_output",
        "carrier_output_invalid",
        "Retry with concise JSON only",
        "--allowedTools",
        "--json-schema",
    ]:
        if phrase not in carrier:
            errors.append(f".agent-org/carrier-invocation.md missing phrase: {phrase}")
    forbidden_prompt_flag = "--append-system" + "-prompt"
    if forbidden_prompt_flag in carrier:
        errors.append(f".agent-org/carrier-invocation.md must not invoke Claude adapters through {forbidden_prompt_flag}")

    contract_schema = text(ROOT / "schemas/implementation-contract.schema.json")
    if "contract_id" not in contract_schema:
        errors.append("schemas/implementation-contract.schema.json must include contract_id")

    implementer_role = text(ROOT / "roles/implementer.md")
    if "contract_id" not in implementer_role or "implementation_contract_id" not in implementer_role:
        errors.append("roles/implementer.md must map contract_id to implementation_contract_id")

    bootstrap = text(ROOT / "bootstrap/codex-bootstrap.md")
    for phrase in [
        "Claude CLI is available, authenticated, network-capable",
        "carrier_unavailable",
        "do not retry by guessing a different invocation",
    ]:
        if phrase not in bootstrap:
            errors.append(f"bootstrap/codex-bootstrap.md missing Claude precondition phrase: {phrase}")

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
        "delegate the workflow change to the relevant CI action writer",
        "CI constraints must come from",
        "Codex main may add exactly `.agent-runs/`",
        ".github/workflows/**",
        "schemas/implementation-contract.schema.json",
        "schemas/implementation-result.schema.json",
    ]:
        if phrase not in content:
            errors.append(f"{rel(path)} missing phrase: {phrase}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the AI Quality Bootstrap pack.")
    parser.add_argument("--schema", help="Schema file for validating one JSON instance.")
    parser.add_argument("--instance", help="JSON instance file to validate against --schema.")
    args = parser.parse_args(argv)

    if args.schema or args.instance:
        if not args.schema or not args.instance:
            print(json.dumps({
                "status": "fail",
                "errors": ["--schema and --instance must be provided together"],
            }, indent=2))
            return 1
        return validate_instance_cli(args.schema, args.instance)

    toml_paths = [ROOT / ".codex/config.toml"] + sorted((ROOT / ".codex/agents").glob("*.toml"))
    toml_data, toml_errors, warnings = load_toml(toml_paths)

    errors: list[str] = []
    errors.extend(f"missing: {item}" for item in check_required_files())
    errors.extend(f"json_parse_error: {item}" for item in parse_json_files())
    errors.extend(f"schema_conformance_error: {item}" for item in check_schema_samples())
    errors.extend(f"toml_parse_error: {item}" for item in toml_errors)
    errors.extend(check_active_directories())
    errors.extend(check_roles())
    errors.extend(check_codex_adapters(toml_data))
    errors.extend(check_claude_adapters())
    errors.extend(check_registry())
    errors.extend(check_pack_policies(toml_data))
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
