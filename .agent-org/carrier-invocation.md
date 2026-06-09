# Carrier Invocation

## Purpose

This policy defines how Supervisor Codex invokes carrier-specific roles without granting those carriers adoption authority.

Canonical role behavior lives in `roles/*.md`. Carrier adapters translate that behavior for each carrier.

## Codex Invocation

Use `.codex/agents/*.toml` when available.

Codex read-only roles must use read-only tool access. Codex write-capable roles must use workspace-write access only inside an admitted work packet and an isolated worktree when writing.

Codex role output must be captured under:

```text
.agent-runs/<run_id>/carriers/codex/<role>/
```

## Claude Code Invocation

Before invoking Claude Code:

1. Check whether the Claude CLI is available.
2. If unavailable, return `carrier_unavailable` and use an approved fallback carrier or stop.
3. Load the matching `.claude/agents/<role>.md` adapter.
4. Load the canonical `roles/<role>.md` spec.

Read-only Claude roles must not receive write permission.

Write-capable Claude roles must run only inside:

```text
.agent-runs/<run_id>/worktrees/<role>/
```

Capture Claude stdout, stderr, invocation prompt, and parsed output under:

```text
.agent-runs/<run_id>/carriers/claude/<role>/
```

Claude output must be schema-shaped JSON or a structured Markdown block that can be converted into the required schema.

## Antigravity Invocation

Antigravity is provisional.

Do not invoke Antigravity until a smoke test confirms the local CLI behavior and output contract.

If Antigravity is requested before smoke testing, return `carrier_unavailable` or use an approved fallback carrier.

Antigravity may provide candidate visual evidence only. It has no final audit authority and no adoption authority.

Capture Antigravity evidence under:

```text
.agent-runs/<run_id>/carriers/antigravity/<role>/
```

## Fallback Rule

When a preferred carrier is unavailable:

1. Record `carrier_unavailable`.
2. Use the secondary carrier only if the runtime registry allows it.
3. Preserve the same canonical role spec.
4. Record the fallback in `run-manifest.json`.

## Adoption Rule

Carrier output is candidate evidence only.

Only Supervisor Codex may adopt a candidate after deterministic gates and accepted audit.
