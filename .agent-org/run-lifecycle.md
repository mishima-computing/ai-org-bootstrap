# Run Lifecycle

## Purpose

This policy defines runtime initialization, worktree creation, minimal gate profile, Mapmaker input bundling, and candidate implementer selection.

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
  work-packets/
  candidates/
  carriers/
  gates/
  audit-bundles/
  audits/
  worktrees/
  mapmaker/
  logs/
  run-manifest.json
```

`.agent-runs/` must remain ignored by Git.

## Run Manifest

`run-manifest.json` records:

- run_id
- target_repo_root
- branch
- locked_target_sha
- current_target_sha
- pack_mode
- pack_materialization_strategy
- carriers_used
- fallbacks_used
- active_worktree_owners
- gate_profile
- adoption_decision

## Worktree Creation Procedure

Before invoking any write-capable role:

1. Read current `HEAD` as `locked_target_sha`.
2. Create candidate branch `ai/candidate-<role>-<run_id>`.
3. Create worktree `.agent-runs/<run_id>/worktrees/<role>/`.
4. Record target ownership in `run-manifest.json`.
5. Run the implementer only inside that worktree.
6. Reread `HEAD` as `current_target_sha` before audit and adoption.

Do not run write-capable roles in the main checkout.

## Gate Profile v0.1

Default gate profile:

```text
gate_profile: bootstrap-v0.1-minimal
```

Required mechanical gates:

- git status
- HEAD SHA
- changed files
- forbidden path check
- candidate output schema check when candidate output exists

Optional if not configured:

- lint
- typecheck
- tests
- build
- secret scan

Mechanical gate failure stops adoption.

Project-specific checks that are not configured must downgrade confidence and require explicit reporting, but they do not automatically block all local progress.

## Mapmaker Input Bundle

Before invoking Mapmaker, create:

```text
.agent-runs/<run_id>/mapmaker/input-bundle.json
```

Minimum fields:

```json
{
  "objective": "",
  "p0_acceptance": [],
  "work_packets": [],
  "pain_points": [],
  "repo_hotspots": [],
  "complexity_observations": [],
  "critical_surfaces": [],
  "constraints": [],
  "non_goals": []
}
```

Mapmaker must not run on vibes alone. If the bundle is empty, defer Mapmaker or gather more read-only evidence.

## Candidate Implementer Selection

Default carrier selection:

- low or medium ordinary work: Codex `boring-worker`
- auth or security work: Claude `auth-security-implementer`
- database or migration work: Claude `database-implementer`
- visual, UI, or browser work: Antigravity `visual-ux-worker` only after smoke test; otherwise Claude `visual-ux-worker`
- production handoff: `production-readiness-planner`, not a deployer

If the preferred carrier is unavailable, use the runtime registry secondary carrier when present and record the fallback.

## Closeout

Final report must include:

- run_id
- pack mode
- materialization strategy
- carriers used
- worktrees created
- gate profile
- not-configured checks
- adoption decision
- deferred backlog
