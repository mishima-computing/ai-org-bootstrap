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

Before invoking Claude Code, create:

```text
.agent-runs/<run_id>/carriers/claude/<agent>/
  input.md
  output.json
  stderr.log
  carrier-status.json
```

`input.md` must include the objective, selected role spec path, adapter path, schema path, allowed files, forbidden files, and expected output path.

Required preflight:

1. `command -v claude`
2. verify `.claude/agents/<agent>.md` exists
3. verify `roles/<agent>.md` exists
4. verify the required output schema exists

If the CLI is unavailable, write `carrier-status.json` with `status: carrier_unavailable`, record `claude_cli_unavailable`, and use an allowed fallback or stop. Do not guess another Claude invocation.

### Read-only Claude Roles

Read-only Claude roles are `aggressive-designer`, `genius`, and `aufheben-designer`.

Invocation template:

```sh
claude --print \
  --permission-mode plan \
  --append-system-prompt "$(cat .claude/agents/<agent>.md)" \
  --output-format json \
  < ".agent-runs/<run_id>/carriers/claude/<agent>/input.md" \
  > ".agent-runs/<run_id>/carriers/claude/<agent>/output.json" \
  2> ".agent-runs/<run_id>/carriers/claude/<agent>/stderr.log"
```

Read-only adapters must not include Bash, Edit, or Write tools.

### Write-capable Claude Roles

Write-capable Claude roles are `security-ci-action-writer` and secondary `implementer`.

Invocation template:

```sh
claude --print \
  --permission-mode acceptEdits \
  --append-system-prompt "$(cat .claude/agents/<agent>.md)" \
  --output-format json \
  < ".agent-runs/<run_id>/carriers/claude/<agent>/input.md" \
  > ".agent-runs/<run_id>/carriers/claude/<agent>/output.json" \
  2> ".agent-runs/<run_id>/carriers/claude/<agent>/stderr.log"
```

Write-capable Claude roles may write only the scope allowed by their role and input contract.

### Genius Invocation

`genius` requires external research. Its adapter must include web/search/fetch capability when available.

If web/search/fetch tools are unavailable, `genius` must produce a schema-shaped output whose handoff states `external_research_unavailable`. It must not fabricate sources.

### Output Capture

Claude output is valid only after:

1. `output.json` exists
2. `output.json` parses as JSON
3. `output.json` conforms to the role schema
4. `carrier-status.json` records the CLI command, exit status, adapter path, role path, schema path, and fallback status

If the local Claude CLI does not support the invocation template, stop with `claude_invocation_contract_unsupported`.

## Fallback Rule

When a preferred carrier is unavailable:

1. Record `carrier_unavailable`.
2. Use the secondary carrier only if the runtime registry allows it.
3. Preserve the same canonical role spec.
4. Record the fallback in runtime notes.

## Authority Rule

Carrier output is candidate evidence or a structured result. It is not adoption.
