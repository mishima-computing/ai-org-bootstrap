# Artifact Policy

## Runtime Artifacts

Runtime artifacts are stored under:

```text
.agent-runs/<run_id>/
```

This directory is ignored by git.

## Standard Run Layout

```text
.agent-runs/
  <run_id>/
    intake/
    work-packets/
    candidates/
      codex/
      claude/
      antigravity/
    gates/
    audit-bundles/
    audits/
    worktrees/
    logs/
```

## Do Not Commit

Do not commit:

- raw prompts
- raw stdout
- raw stderr
- raw model transcripts
- screenshots
- recordings
- unreviewed candidate outputs
- local worktrees
- raw tool logs
- secrets
- credentials
- production data
- customer data

## May Commit

The following may be committed only when sanitized and intentionally reviewed:

- role specs
- carrier adapters
- schemas
- deterministic scripts
- bootstrap policies
- sanitized summaries
- accepted documentation

## Hashing

When practical, record SHA-256 hashes for:

- candidate patch
- deterministic gate report
- audit bundle
- audit decision

## History

Human-readable sanitized summaries may later be stored under:

```text
.agent-org/history/
```

Do not create history summaries in this task.
