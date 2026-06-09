# Worktree Policy

## Purpose

This policy prevents multiple agents from sharing the same writable target and corrupting each other's work.

## Read-only Roles

Read-only roles may run in the main checkout.

Read-only roles include:

- workspace-gatekeeper
- convergence-manager
- work-packet-dispatcher
- critical-surface-manager
- mapmaker-agent
- experiment-designer
- codex-auditor
- claude-independent-auditor
- visual-auditor
- gate-report-builder

## Write-capable Roles

Write-capable roles must run in isolated git worktrees.

Write-capable roles include:

- boring-worker
- auth-security-implementer
- database-implementer
- visual-ux-worker

## Candidate Branch Naming

Use this branch format:

```text
ai/candidate-<role>-<run_id>
```

Use this worktree format:

```text
.agent-runs/<run_id>/worktrees/<role>/
```

## Ownership Rule

One active writer owns one candidate branch or worktree.

Two active writer roles must not share:

- a branch
- a worktree
- a patch application target

## SHA Rule

Before candidate generation, record:

- run_id
- role
- candidate_objective_id
- target branch or worktree
- locked_target_sha

Before audit and adoption, reread HEAD as current_target_sha.

A candidate must not be adopted if current_target_sha does not match candidate_base_sha unless the candidate is regenerated against the new base.

## Adoption Rule

Candidate implementers do not merge or adopt their own work.

Only Supervisor Codex may adopt an accepted candidate after deterministic gates and audit.
