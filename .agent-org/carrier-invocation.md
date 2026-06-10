# Carrier Invocation

## Purpose

This policy defines carrier-specific invocation without turning carriers into agents.

Canonical agent behavior lives in `roles/*.md`. Carrier adapters translate that behavior for Codex or Claude Code.

## Codex Invocation

Use `.codex/agents/*.toml` when available.

Codex read-only agents must use read-only tool access.

Codex write-capable agents must use workspace-write access only for the scope allowed by their role and input contract.

Codex output should be captured under:

```text
.agent-runs/<run_id>/carriers/codex/<agent>/
```

## Claude Code Invocation

Before invoking Claude Code:

1. Check whether the Claude CLI is available.
2. If unavailable, return `carrier_unavailable` and use an allowed fallback or stop.
3. Load the matching `.claude/agents/<agent>.md` adapter.
4. Load the canonical `roles/<agent>.md` spec.

Read-only Claude agents must not receive write permission.

Write-capable Claude agents must receive only the scope allowed by their role and input contract.

Claude output should be captured under:

```text
.agent-runs/<run_id>/carriers/claude/<agent>/
```

## Fallback Rule

When a preferred carrier is unavailable:

1. Record `carrier_unavailable`.
2. Use the secondary carrier only if the runtime registry allows it.
3. Preserve the same canonical role spec.
4. Record the fallback in runtime notes.

## Authority Rule

Carrier output is candidate evidence or a structured result. It is not adoption.
