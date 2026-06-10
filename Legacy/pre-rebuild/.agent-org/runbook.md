# AI Agent Organization Runbook

## Run identity

Use `YYYYMMDD-HHMMSS` local time format for `run_id`.

## Workspace classification

Before writes, classify the workspace as `new_project`, `existing_repo_clean`, `dirty_existing_repo`, or `ambiguous_workspace`, plus any `cloud_synced_workspace` risk flag.

Use raw path and realpath-equivalent cloud-sync checks when available.

## Bootstrap flow

- `new_project`: create or use a fresh local-only root, initialize Git if needed, add `.agent-runs/` to `.gitignore`, create governance files, verify, then create one local commit on the default branch unless a run branch is requested.
- `existing_repo_clean`: create `ai/bootstrap-<run_id>`, update only approved governance files, verify, then commit locally.
- `dirty_existing_repo`: stop before branch creation or writes.
- `ambiguous_workspace`: stop unless files resolve the ambiguity safely.

Branch names: `ai/run-<run_id>`, `ai/bootstrap-<run_id>`, and `ai/candidate-<agent>-<run_id>`.

## Approval phrases

| Action | Required approval |
|---|---|
| Write in a cloud-synced workspace | `APPROVE CLOUD-SYNC WORKSPACE <run_id>` |
| Merge into a protected branch | `APPROVE MERGE <run_id> <target_branch>` |
| Let Antigravity produce a candidate UI patch | `APPROVE ANTIGRAVITY CANDIDATE UI PATCH <run_id>` |
| Push, deploy, or publish | Separate explicit human approval |

## Ask Gate

Ask at most three questions, do not ask what files can answer, proceed with low-risk assumptions, and stop on unresolved high-risk ambiguity.

## Context Cartographer

Gather read-only repository context, approved scope, current branch, remotes, status, relevant files, and risk flags before assigning implementation work.

## Candidate Implementer

Candidate Implementer outputs patch-only work with `candidate_objective_id`, `candidate_id`, attempt number, base SHA, changed files, rationale, checks, assumptions, known risks, and unresolved questions.

## Claude candidate patch flow

Claude may be used only with explicit approval. Store raw output and invocation material under ignored `.agent-runs/`. Convert candidate output into a deterministic audit bundle before any adoption.

## Target ownership

Record `target_lock_owner_run_id`, `target_branch_or_worktree`, `locked_target_sha`, and `candidate_base_sha`.

One active run owns a writable candidate target for each objective.

Reread `current_target_sha` before gates, audit bundle generation, and adoption.

## Attempt accounting

Use a cross-agent attempt ceiling per `run_id` and `candidate_objective_id`. The default is three attempts.

Switching agents does not reset the count. Parse, scope, base, or Auditor failures consume attempts when they produce a new candidate.

## Auditor finding lineage

Track previous finding IDs. Mark repeated findings as `yes`, `no`, or `partial`, and record material progress as `yes`, `no`, `partial`, or `not_applicable`.

## Deterministic audit bundle

Generate the bundle mechanically from the human task, candidate output, invocation manifest, prior findings, and gate outputs.

Do not omit unfavorable assumptions, risks, unresolved questions, or failed checks. Represent missing fields explicitly.

## SHA revalidation

Verify `candidate_base_sha` and reread `current_target_sha`.

Adopt only when the current target still matches the accepted candidate base, unless a regenerated candidate was reviewed against the new base.

## Antigravity Visual Review

Antigravity is a visual review pod by default.

It is review-only and artifact-first unless explicit candidate UI patch approval is present.

## Local Tooling verification

Run deterministic checks such as status, ignored-file proof, whitespace checks, scope checks, sanitation scan, tests, lint, typecheck, or build when relevant.

Local Tooling produces evidence, not release decisions.

## Codex Auditor

Auditor is independent and read-only.

It reviews scope, forbidden files, policy, base SHA, target ownership, checks, sanitation, and bundle completeness. It returns `accepted`, `rejected`, or `needs_revision`.

## Release Manager and final readiness

Final readiness separates local commit, merge, push, deploy, and publish.

Human Owner approval is required for merge, push, deploy, publish, production data, credentials, and protected-branch exceptions.

## Local commit conditions

Commit locally only when workspace mode allows writing, branch conditions are satisfied, changed files are in approved scope, `.agent-runs/` is ignored and untracked, forbidden paths are absent, whitespace checks pass, and sanitation gate passes.

## Merge conditions

Merge only with explicit Human Owner approval for the run and target branch.

Merge approval does not imply push, deploy, or publish.

## Final sanitized summary

Write final summaries under `.agent-org/history/`.

Do not include secrets, credentials, raw prompts, raw stderr, raw screenshots, recordings, production personal data, customer data, or unnecessary local absolute paths.
