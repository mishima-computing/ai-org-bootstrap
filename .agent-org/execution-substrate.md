# Execution Substrate

This repository uses a multi-carrier AI quality bootstrap.

The execution substrate defines where agent configuration, skills, schemas, runtime artifacts, and deterministic gates live. It does not define individual role behavior. Role behavior will be added later as independent role specifications and carrier adapters.

## Carriers

### Codex

Codex is the default supervisor, dispatcher, schema-output, boring-worker, and auditor carrier.

Codex project configuration lives under:

```text
.codex/
.codex/agents/
.agents/skills/
```

Codex role adapters will be stored as TOML files under `.codex/agents/`.

Codex skills will be stored under `.agents/skills/`.

### Claude Code

Claude Code is the default carrier for heavy implementation, critical-surface management, Mapmaker work, invariant scouting, and independent audit.

Claude project configuration lives under:

```text
.claude/
.claude/agents/
.claude/skills/
```

Claude role adapters will be stored as Markdown files with YAML frontmatter under `.claude/agents/`.

Claude skills will be stored under `.claude/skills/`.

### Antigravity

Antigravity is provisional.

It may be used later for visual review, browser evidence, UI exploration, screenshots, recordings, and parallel visual work.

Antigravity configuration lives under:

```text
.antigravity/
.antigravity/agents/
.antigravity/skills/
```

Until its local CLI contract is verified, Antigravity must not be used for:

- authentication
- authorization
- database work
- migrations
- production operations
- secrets
- deployment
- final adoption authority
- final audit authority

## Execution Isolation

Read-only roles may run in the main checkout.

Write-capable roles must run in isolated git worktrees.

No two active writer roles may share the same writable branch or worktree.

Candidate outputs are not adopted directly. They must pass deterministic gates and independent audit before Supervisor Codex may apply or adopt them.

## Runtime Artifacts

Runtime artifacts belong under:

```text
.agent-runs/<run_id>/
```

`.agent-runs/` is ignored by git.

Raw prompts, stdout, stderr, screenshots, recordings, candidate scratchpads, and unreviewed outputs must not be committed.

## Adoption Authority

Only Supervisor Codex may adopt an accepted candidate patch.

Implementers, Mapmaker roles, visual agents, and auditors do not have adoption authority.
