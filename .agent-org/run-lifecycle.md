# Run Lifecycle

## Purpose

This policy defines runtime initialization for the final Bootstrap roster.

## Run ID

Generate `run_id` after target repository confirmation:

```text
YYYYMMDD-HHMMSS-<shortsha>
```

Use the current target `HEAD` short SHA for `<shortsha>`.

## Runtime Directory

Initialize:

```text
.agent-runs/<run_id>/
  intake/
  carriers/
  results/
  gates/
  worktrees/
  logs/
```

`.agent-runs/` must remain ignored by Git.

## Default Sequence

1. Run CI action writer agents when the objective is CI automation.
2. Run designer agents when implementation design is needed.
3. Run `aufheben-designer` to create one implementation contract.
4. Run `implementer` only from that implementation contract.
5. Run deterministic local tooling when configured.
6. Report changed files, commands run, checks, gaps, and remaining work.

## Gate Profile

Default gate profile:

```text
gate_profile: bootstrap-final-minimal
```

Required mechanical facts:

- git status
- HEAD SHA
- changed files
- forbidden path check

Optional if not configured:

- lint
- typecheck
- tests
- build
- secret scan

Unavailable project-specific checks must be reported as gaps.

## Closeout

Final report must include:

- run_id
- target repo
- branch
- HEAD SHA
- active agents used
- carrier fallbacks
- changed files
- commands run
- checks passed
- checks failed
- gaps
- warnings
