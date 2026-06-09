# Bootstrap Entrypoints

`codex-bootstrap-v0.1.md` is the copy-paste Codex entrypoint.

Target repositories should not regenerate role specs or skill loaders. This repository is the source pack for AI Quality Bootstrap.

The entrypoint supports source-pack repos, target repos with vendored packs, and target repos that still need explicit pack materialization.

Canonical roles live under `roles/`.

Carrier adapters live under:

- `.codex/agents/`
- `.claude/agents/`
- `.antigravity/agents/` as provisional adapters

Runtime artifacts created by target runs belong under `.agent-runs/` and must remain ignored.

Previous repository content is preserved under `Legacy/`.
