# AI Quality Bootstrap

A copy-paste **agent pipeline** for building software under quality control. A
controller (Codex main) routes an objective through eight specialized agents —
three designers propose, one synthesizer resolves them into a single contract,
an implementer builds against that contract, and CI writers wire checks — with
schema-validated handoffs and human adoption at the end.

Main copy-paste entrypoint: **[bootstrap/codex-bootstrap.md](bootstrap/codex-bootstrap.md)**

Field-proven: this pack built [agent-bridge-01](https://github.com/mishima-computing/agent-bridge-01)
(a TS/Next.js SaaS) across ~15 adopted cycles, and improves *itself* through the
same pipeline (Mode A self-hosting).

## The roster

| Agent | Role |
| --- | --- |
| `aggressive-designer` | bold design proposal |
| `conservative-designer` | safe, minimal design proposal |
| `genius` | evidence-gated outside insight (v2: substrate-first, verify-to-kill) |
| `aufheben-designer` | synthesizes the three into **one** implementation contract |
| `implementer` | builds strictly within the contract's allowed scope |
| `functional` / `security` / `nonfunctional`-`ci-action-writer` | wire existing checks into GitHub Actions |

Codex main is the **controller** (protocol, not an agent). Deterministic tooling
(gate reporting, schema validation, artifact hashing) is a **subsystem**.

## Flow

```
objective
  ├─▶ aggressive ─┐
  ├─▶ conservative ┼─▶ aufheben ──▶ verdict
  └─▶ genius ──────┘                  ├─ proceed  ─▶ contract ─▶ implementer ─▶ gates ─▶ human adoption
                                      ├─ redo     ─▶ (controller re-runs designers, max 2)
                                      └─ escalate ─▶ controller / human
```

Each handoff is a JSON document validated against a schema in `schemas/`. The
**aufheben verdict** (proceed / redo / escalate) lets the synthesizer send work
back instead of failing silently — a structural substitute for the inhibition an
always-acting agent lacks.

## Carriers

Canonical behavior lives in `roles/*.md`; carrier adapters translate it per tool:

- **Codex** — `.codex/agents/*.toml`, run via `codex exec --output-schema`
- **Claude Code** — `.claude/agents/*.md`, run via `claude --print --json-schema`
- **Antigravity** — reserved

See [`.agent-org/carrier-invocation.md`](.agent-org/carrier-invocation.md) for the
exact invocation templates (stdin-safe, timeout, interrupted-run resume) and
[`scripts/extract-claude-result.py`](scripts/extract-claude-result.py) for output
extraction (closure repair, largest-object salvage, codex raw-text mode).

## Repository areas

```text
bootstrap/         Copy-paste bootstrap entrypoint
roles/             Canonical role specs (source of truth for behavior)
schemas/           Handoff schemas (design proposal, genius packet, contract,
                   aufheben verdict, implementation result, CI result)
.agent-org/        Policies: carrier invocation, run lifecycle, worktree,
                   pack materialization, knowledge substrate; evaluation docs
.agent-org/knowledge/  Per-target repo map + durable fact cards (genius substrate)
.codex/ .claude/   Carrier adapters and config
scripts/           Deterministic tooling: validator, extractor, gates, hashing
.antigravity/      Reserved carrier area
Legacy/            Preserved pre-rebuild material
.agent-runs/       Ignored runtime artifacts
```

## Self-test

```sh
python3 scripts/validate-bootstrap-pack.py        # validate the whole pack
python3 scripts/extract-claude-result.py --self-test
```

CI (`.github/workflows/`) runs both on every push and PR, plus CodeQL and gitleaks.

## Design notes

- **`genius` v2** is evidence-gated: consume a compact substrate first, hypothesize
  *without* retrieval, then use the web only to confirm/refute kept hypotheses
  (search-to-kill, not search-to-find). See the measured A/B baseline in
  [`docs/evaluation/`](docs/evaluation/).
- **Adoption is human**: agents produce candidate evidence and contracts; merge
  (or contract approval) is the human decision. No agent claims adoption.
