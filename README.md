# AI Quality Bootstrap

This repository is the GitHub source pack for AI Quality Bootstrap.

Main copy-paste entrypoint:

- [bootstrap/codex-bootstrap.md](bootstrap/codex-bootstrap.md)

Previous repository contents and draft role material are preserved under `Legacy/`.

## Current Roster

```text
1. functional-ci-action-writer
2. security-ci-action-writer
3. nonfunctional-ci-action-writer
4. aggressive-designer
5. conservative-designer
6. genius
7. aufheben-designer
8. implementer
```

## Repository Areas

```text
bootstrap/         Copy-paste bootstrap entrypoint
roles/             Canonical role specs for the final roster
.agent-org/        Governance and substrate policies
.codex/agents/     Codex carrier adapters
.claude/agents/    Claude Code carrier adapters
.antigravity/      Reserved provisional carrier area
schemas/           Shared output schemas
scripts/           Deterministic tooling
smoke/             Future smoke tests
.agent-runs/       Ignored runtime artifacts
Legacy/            Preserved pre-rebuild material and drafts
```

## Runtime Model

- Agents: the eight final agents listed above.
- Protocol: `codex-main-controller`.
- Subsystems: `local-tooling`, `gate-reporting`, and `artifact-hashing`.

Codex main may coordinate execution, but it is not listed as an agent.
Deterministic tooling may exist, but it is not listed as an agent.
