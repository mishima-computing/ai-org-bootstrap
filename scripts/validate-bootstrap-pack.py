#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROLE_HEADINGS = [
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

CODEX_SCHEMA_BY_AGENT = {
    "convergence-manager": "schemas/convergence-decision.schema.json",
    "work-packet-dispatcher": "schemas/work-packet.schema.json",
    "critical-surface-manager": "schemas/critical-surface-decision.schema.json",
    "mapmaker-agent": "schemas/concept-memo.schema.json",
    "experiment-designer": "schemas/experiment-packet.schema.json",
    "boring-worker": "schemas/candidate-output.schema.json",
    "codex-auditor": "schemas/audit-decision.schema.json",
    "gate-report-builder": "schemas/gate-report.schema.json",
}

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

READ_ONLY_CLAUDE_AGENTS = {
    "critical-surface-manager",
    "mapmaker-agent",
    "design-space-searcher",
    "invariant-scout",
    "production-readiness-planner",
    "claude-independent-auditor",
    "visual-auditor",
}

WRITE_CAPABLE_CLAUDE_AGENTS = {
    "auth-security-implementer",
    "database-implementer",
    "visual-ux-worker",
}

REQUIRED_ANTIGRAVITY_AGENTS = [
    "visual-ux-worker",
    "visual-auditor",
    "mapmaker-agent",
]

REQUIRED_POLICY_DOCS = [
    ".agent-org/runtime-registry.yaml",
    ".agent-org/execution-substrate.md",
    ".agent-org/worktree-policy.md",
    ".agent-org/artifact-policy.md",
    ".agent-org/pack-materialization.md",
    ".agent-org/carrier-invocation.md",
    ".agent-org/run-lifecycle.md",
]

REQUIRED_SCRIPTS = [
    "scripts/run-gates.sh",
    "scripts/build-audit-bundle.py",
    "scripts/hash-artifacts.py",
    "scripts/build-mapmaker-input-bundle.py",
    "scripts/validate-bootstrap-pack.py",
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
    "run-manifest.schema.json",
    "mapmaker-input-bundle.schema.json",
]

BOOTSTRAP_SECTIONS = [
    "Purpose",
    "Required Preconditions",
    "Target Repository Confirmation",
    "Bootstrap Pack Loading",
    "Agent Registry",
    "Execution Order",
    "Convergence Rules",
    "Critical Surface Rules",
    "Mapmaker Rules",
    "Candidate Implementation Rules",
    "Deterministic Gate Rules",
    "Audit Rules",
    "Adoption Rules",
    "Artifact Rules",
    "Stop Conditions",
    "Required Final Report",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lower(path: Path) -> str:
    return text(path).lower()


def contains_all(content: str, phrases: list[str]) -> list[str]:
    normalized = content.lower()
    return [phrase for phrase in phrases if phrase.lower() not in normalized]


def check_required_files() -> list[str]:
    required = [
        ROOT / "bootstrap/codex-bootstrap-v0.1.md",
        ROOT / "bootstrap/README.md",
        ROOT / ".codex/config.toml",
        ROOT / ".claude/settings.json",
    ]
    required.extend(ROOT / path for path in REQUIRED_POLICY_DOCS)
    required.extend(ROOT / path for path in REQUIRED_SCRIPTS)
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
    schema_ids: dict[str, str] = {}
    for path in sorted((ROOT / "schemas").glob("*.json")):
        try:
            parsed = json.loads(text(path))
        except Exception as exc:  # noqa: BLE001 - report parse failure
            errors.append(f"{rel(path)}: {exc}")
            continue
        schema_id = parsed.get("$id")
        if schema_id:
            if schema_id in schema_ids:
                errors.append(f"duplicate_schema_id: {schema_id} in {schema_ids[schema_id]} and {rel(path)}")
            schema_ids[schema_id] = rel(path)

    settings = ROOT / ".claude/settings.json"
    try:
        json.loads(text(settings))
    except Exception as exc:  # noqa: BLE001 - report parse failure
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
        except Exception as exc:  # noqa: BLE001 - report parse failure
            errors.append(f"{rel(path)}: {exc}")
    return parsed, errors, warnings


def check_roles() -> list[str]:
    errors: list[str] = []
    for role in REQUIRED_ROLES:
        path = ROOT / "roles" / f"{role}.md"
        if not path.is_file():
            continue
        content = text(path)
        for heading in REQUIRED_ROLE_HEADINGS:
            if heading not in content:
                errors.append(f"{rel(path)} missing heading: {heading}")

    semantic_checks = {
        "roles/bootstrap-supervisor.md": [
            "adoption authority",
            "implementers",
            "auditors",
            "Mapmaker",
            "Antigravity",
            "deterministic gates",
            "accepted audit",
        ],
        "roles/convergence-manager.md": [
            "max decomposition depth = 3",
            "max active work packets = 1",
            "P0/P1/P2",
            "P1/P2 do not block done",
            "preparation-only work cannot repeat",
            "new discoveries default to deferred backlog unless they block P0",
            "schemas/convergence-decision.schema.json",
        ],
        "roles/critical-surface-manager.md": [
            "High risk is not a reason to stop. High risk is a reason to add gates.",
            "L0 static artifact",
            "L5 requires explicit human approval",
            "Vague blockers are invalid",
            "Allowed blocker enum",
            "schemas/critical-surface-decision.schema.json",
        ],
        "roles/mapmaker-agent.md": [
            "Genius is not a vote. Genius is a compression hypothesis.",
            "Must not implement",
            "edit files",
            "expand P0",
            "one bounded experiment",
            "evidence",
            "schemas/concept-memo.schema.json",
        ],
        "roles/auth-security-implementer.md": [
            "isolated worktree",
            "production secrets",
            "deploy",
            "protected branch",
            "adopt",
            "default deny",
            "server-side authorization",
            "negative",
        ],
        "roles/database-implementer.md": [
            "isolated worktree",
            "rollback/down migration",
            "local apply",
            "local rollback",
            "production DB",
            "production migration",
        ],
        "roles/codex-auditor.md": [
            "read-only",
            "Must not edit",
            "fix candidate",
            "adopt",
            "summarize away failed checks",
        ],
        "roles/claude-independent-auditor.md": [
            "read-only",
            "Must not edit",
            "fix candidates",
            "adopt",
            "summarize away failed checks",
        ],
        "roles/visual-ux-worker.md": [
            "Antigravity provisional",
            "auth",
            "database",
            "production",
            "secrets",
            "final audit",
            "adoption",
        ],
        "roles/visual-auditor.md": [
            "Antigravity provisional",
            "auth",
            "database",
            "production",
            "secrets",
            "final audit",
            "adoption",
        ],
    }
    for raw_path, phrases in semantic_checks.items():
        path = ROOT / raw_path
        if not path.is_file():
            continue
        for phrase in contains_all(text(path), phrases):
            errors.append(f"{raw_path} missing semantic phrase: {phrase}")
    return errors


def check_codex_adapters(toml_data: dict[Path, dict]) -> list[str]:
    errors: list[str] = []
    required_keys = {"name", "description", "model_reasoning_effort", "sandbox_mode", "developer_instructions"}
    for name in REQUIRED_CODEX_AGENTS:
        path = ROOT / ".codex/agents" / f"{name}.toml"
        if not path.is_file():
            continue
        parsed = toml_data.get(path)
        raw = text(path)
        if parsed is None:
            for key in required_keys:
                if f"{key} =" not in raw:
                    errors.append(f"{rel(path)} missing TOML key: {key}")
            continue
        missing = required_keys - set(parsed)
        for key in sorted(missing):
            errors.append(f"{rel(path)} missing TOML key: {key}")
        if parsed.get("model_reasoning_effort") != "high":
            errors.append(f"{rel(path)} model_reasoning_effort must be high")
        expected_sandbox = "workspace-write" if name == "boring-worker" else "read-only"
        if parsed.get("sandbox_mode") != expected_sandbox:
            errors.append(f"{rel(path)} sandbox_mode must be {expected_sandbox}")
        instructions = str(parsed.get("developer_instructions", ""))
        role_path = f"roles/{name}.md"
        if role_path not in instructions:
            errors.append(f"{rel(path)} must reference {role_path}")
        if "canonical role spec controls behavior" not in instructions.lower():
            errors.append(f"{rel(path)} must state canonical role spec controls behavior")
        if "adoption authority" not in instructions.lower():
            errors.append(f"{rel(path)} must prohibit adoption authority")
        schema = CODEX_SCHEMA_BY_AGENT.get(name)
        if schema and schema not in instructions:
            errors.append(f"{rel(path)} must reference schema {schema}")
    return errors


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


def check_claude_adapters() -> list[str]:
    errors: list[str] = []
    required_keys = {"name", "description", "tools", "model", "permissionMode"}
    for name in REQUIRED_CLAUDE_AGENTS:
        path = ROOT / ".claude/agents" / f"{name}.md"
        if not path.is_file():
            continue
        frontmatter, body, error = parse_frontmatter(path)
        if error:
            errors.append(f"{rel(path)} {error}")
            continue
        for key in sorted(required_keys - set(frontmatter)):
            errors.append(f"{rel(path)} missing frontmatter key: {key}")
        tools = frontmatter.get("tools", "")
        if name in READ_ONLY_CLAUDE_AGENTS and ("Edit" in tools or "Write" in tools):
            errors.append(f"{rel(path)} read-only tools must not include Edit or Write")
        if f"roles/{name}.md" not in body:
            errors.append(f"{rel(path)} must reference roles/{name}.md")
        if "canonical role spec controls behavior" not in body.lower():
            errors.append(f"{rel(path)} must state canonical role spec controls behavior")
        if name in WRITE_CAPABLE_CLAUDE_AGENTS:
            missing = contains_all(
                body,
                [
                    "admitted files",
                    "isolated worktree",
                    "No production",
                    "No secrets",
                    "No protected branch merge",
                    "No adoption authority",
                ],
            )
            for phrase in missing:
                errors.append(f"{rel(path)} missing write constraint: {phrase}")
    return errors


def check_antigravity_adapters() -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_ANTIGRAVITY_AGENTS:
        path = ROOT / ".antigravity/agents" / f"{name}.md"
        if not path.is_file():
            continue
        content = lower(path)
        checks = {
            "provisional": "provisional",
            "smoke test": ("smoke-test" in content or "smoke test" in content or "smoke-tested" in content),
            "no auth": "auth" in content,
            "no database": "database" in content,
            "no production": "production" in content,
            "no adoption": "adoption" in content,
        }
        for label, result in checks.items():
            if isinstance(result, str):
                result = result in content
            if not result:
                errors.append(f"{rel(path)} missing Antigravity requirement: {label}")
    return errors


def check_skill_loaders() -> list[str]:
    errors: list[str] = []
    paths = [ROOT / ".agents/skills" / name / "SKILL.md" for name in REQUIRED_CODEX_SKILLS]
    paths.extend(ROOT / ".claude/skills" / name / "SKILL.md" for name in REQUIRED_CLAUDE_SKILLS)
    for path in paths:
        if not path.is_file():
            continue
        content = lower(path)
        if "roles/" not in content:
            errors.append(f"{rel(path)} must reference roles/")
        if "not adoption authority" not in content:
            errors.append(f"{rel(path)} must state not adoption authority")
    return errors


def check_policy_docs() -> list[str]:
    errors: list[str] = []
    required_phrases = {
        ".agent-org/pack-materialization.md": [
            "Mode A",
            "Mode B",
            "Mode C",
            "APPROVE BOOTSTRAP PACK MATERIALIZATION",
            "bootstrap_pack_not_materialized",
            "Do not invent or generate",
        ],
        ".agent-org/carrier-invocation.md": [
            "carrier_unavailable",
            "Claude CLI",
            ".agent-runs/<run_id>/carriers/claude/<role>/",
            "Antigravity is provisional",
            "Only Supervisor Codex may adopt",
        ],
        ".agent-org/run-lifecycle.md": [
            "YYYYMMDD-HHMMSS-<shortsha>",
            "run-manifest.json",
            "ai/candidate-<role>-<run_id>",
            "gate_profile: bootstrap-v0.1-minimal",
            "mapmaker/input-bundle.json",
            "Candidate Implementer Selection",
        ],
    }
    for raw_path, phrases in required_phrases.items():
        path = ROOT / raw_path
        if not path.is_file():
            continue
        for phrase in contains_all(text(path), phrases):
            errors.append(f"{raw_path} missing policy phrase: {phrase}")
    return errors


def check_scripts() -> list[str]:
    errors: list[str] = []
    run_gates = ROOT / "scripts/run-gates.sh"
    if run_gates.is_file():
        content = text(run_gates)
        for phrase in [
            "bootstrap-v0.1-minimal",
            "forbidden_path_check",
            "candidate_output_schema_check",
            "optional_not_configured",
            "git rev-parse HEAD",
        ]:
            if phrase not in content:
                errors.append(f"{rel(run_gates)} missing gate phrase: {phrase}")
    mapmaker = ROOT / "scripts/build-mapmaker-input-bundle.py"
    if mapmaker.is_file():
        content = text(mapmaker)
        for phrase in [
            "p0_acceptance",
            "repo_hotspots",
            "complexity_observations",
            "critical_surfaces",
            "non_goals",
        ]:
            if phrase not in content:
                errors.append(f"{rel(mapmaker)} missing Mapmaker bundle field: {phrase}")
    return errors


def check_bootstrap_entrypoint() -> list[str]:
    errors: list[str] = []
    path = ROOT / "bootstrap/codex-bootstrap-v0.1.md"
    if not path.is_file():
        return errors
    content = text(path)
    normalized = content.lower()
    for index, section in enumerate(BOOTSTRAP_SECTIONS, start=1):
        heading = f"## {index}. {section}"
        if heading not in content:
            errors.append(f"{rel(path)} missing section heading: {heading}")
    phrase_groups = {
        "target repo confirmation": ["target repository confirmation", "target repo"],
        "run mode classification": ["Mode A", "Mode B", "Mode C"],
        "pack materialization": ["bootstrap_pack_not_materialized", "APPROVE BOOTSTRAP PACK MATERIALIZATION"],
        "run id format": ["YYYYMMDD-HHMMSS-<shortsha>"],
        "run manifest": ["run-manifest.json"],
        "carrier invocation": ["carrier invocation"],
        "worktree creation": ["ai/candidate-<role>-<run_id>", ".agent-runs/<run_id>/worktrees/<role>/"],
        "gate profile": ["gate_profile: bootstrap-v0.1-minimal"],
        "Mapmaker input bundle": ["mapmaker/input-bundle.json"],
        "candidate implementer selection": ["Select candidate implementer by surface"],
        "max decomposition depth": ["max_decomposition_depth", "max decomposition depth"],
        "P0/P1/P2": ["p0/p1/p2"],
        "high risk is not a stop reason": ["high risk is not a stop reason"],
        "Mapmaker": ["mapmaker"],
        "deterministic gates": ["deterministic gate"],
        "Supervisor Codex adoption": ["supervisor codex adoption", "supervisor codex adopts"],
        "Antigravity provisional": ["antigravity", "provisional"],
    }
    for label, alternatives in phrase_groups.items():
        if not any(alt.lower() in normalized for alt in alternatives):
            errors.append(f"{rel(path)} missing bootstrap phrase: {label}")
    return errors


def main() -> int:
    toml_paths = [ROOT / ".codex/config.toml"] + sorted((ROOT / ".codex/agents").glob("*.toml"))
    toml_data, toml_errors, warnings = load_toml(toml_paths)

    errors: list[str] = []
    errors.extend(f"missing: {item}" for item in check_required_files())
    errors.extend(f"json_parse_error: {item}" for item in parse_json_files())
    errors.extend(f"toml_parse_error: {item}" for item in toml_errors)
    errors.extend(check_roles())
    errors.extend(check_codex_adapters(toml_data))
    errors.extend(check_claude_adapters())
    errors.extend(check_antigravity_adapters())
    errors.extend(check_skill_loaders())
    errors.extend(check_policy_docs())
    errors.extend(check_scripts())
    errors.extend(check_bootstrap_entrypoint())

    payload = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
