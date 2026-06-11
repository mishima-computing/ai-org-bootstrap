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

Codex main is responsible for confirming the ignore rule during approved pack materialization. It may add exactly `.agent-runs/` to the target root `.gitignore` if absent.

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

## Carrier Execution Timeout

Default carrier execution timeout is 30 minutes of wall-clock time per carrier process.

On expiry, the controller kills the carrier process and records `carrier_timeout` in `carrier-status.json`. Silent hangs are detectable only by timeout; the default may be raised per invocation when the controller expects a legitimately longer run.

## Resume

If a carrier dies or hangs after writing workspace changes but before reporting, preserve the dead attempt's artifacts unmodified and re-invoke the same role with the original file scope and contract.

The resume prompt must be verify-and-report only:

```text
Resume the same role from the existing workspace state. Do not redesign. Verify existing work against the original contract. Run required_checks. Emit the required report.
```

The resumed role must not receive wider file scope than its original contract.

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
- controller may distill adopted-cycle facts into `.agent-org/knowledge/cards/` per `.agent-org/knowledge/README.md`
