# AI Quality Bootstrap

This repository is the GitHub source pack for AI Quality Bootstrap.

Main copy-paste entrypoint:

- [bootstrap/codex-bootstrap-v0.1.md](bootstrap/codex-bootstrap-v0.1.md)

Previous repository contents were preserved under `Legacy/`.

## Current Phase

Bootstrap Pack on top of the execution substrate.

## Repository Areas

```text
bootstrap/         Copy-paste bootstrap entrypoints
roles/             Canonical role specs
.agent-org/        Governance and substrate policies
.codex/agents/     Codex carrier adapters
.agents/skills/    Codex skill loaders
.claude/agents/    Claude Code carrier adapters
.claude/skills/    Claude skill loaders
.antigravity/      Provisional Antigravity area and adapters
schemas/           Shared output schemas
scripts/           Deterministic tooling skeletons and validation
smoke/             Future smoke tests
.agent-runs/       Ignored runtime artifacts
Legacy/            Preserved pre-rebuild material and old drafts
```

Key runtime policies:

- `.agent-org/pack-materialization.md`
- `.agent-org/carrier-invocation.md`
- `.agent-org/run-lifecycle.md`

## Carriers

- Codex: supervisor, dispatcher, boring worker, schema output, audit
- Claude Code: critical-surface work, heavy implementation, Mapmaker, independent audit
- Antigravity: provisional visual/browser/UI evidence lane

## Status

No production agent execution has been performed by this repository setup.
