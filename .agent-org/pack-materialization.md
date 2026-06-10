# Pack Materialization

## Purpose

This policy resolves the difference between the GitHub source pack and a target repository where a human pastes `bootstrap/codex-bootstrap.md`.

The bootstrap pack must not be invented, regenerated, or partially guessed inside target repositories.

## Run Modes

### Mode A: source-pack repo

Use when the current Git repository is `mishima-computing/ai-org-bootstrap`.

The pack files are already local. Validate the pack in place before using it as source material.

### Mode B: target repo with vendored pack

Use when the current Git repository is the human target repository and the required pack files are already present locally.

Validate the local pack files before routing agents.

### Mode C: target repo without vendored pack

Use when the current Git repository is the human target repository and required pack files are missing.

Do not generate missing role specs, schemas, policies, or adapters.

## Materialization Rule

If pack files are missing:

1. Do not invent or generate missing pack files.
2. Check whether `gh`, `git`, or network fetch is available.
3. If explicit materialization approval is present and tooling is available, vendor the source pack from GitHub into the target repository.
4. During approved materialization, Codex main may add exactly `.agent-runs/` to the target root `.gitignore` if it is absent.
5. If approval or tooling is missing, print exact manual sync commands and stop with `bootstrap_pack_not_materialized`.

Explicit materialization approval phrase:

```text
APPROVE BOOTSTRAP PACK MATERIALIZATION <source_repo> <target_repo>
```

## Stop Conditions

Stop with `bootstrap_pack_not_materialized` when:

- pack files are missing
- explicit materialization approval is absent
- required tooling is unavailable
- the target repo is ambiguous
- materialization would overwrite existing target content
