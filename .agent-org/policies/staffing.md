# Staffing Policy / Staffingポリシー

## Roles / ロール

- Human Owner: controls high-risk decisions, merge, push, deploy, publish, production data access, credentials, and legal/privacy/brand decisions.
- Supervisor Codex: routes tasks, applies accepted patches, maintains governance, runs verification, creates allowed local commits, and never deploys.
- Codex Auditor: independent read-only reviewer for scope, policy, diff, evidence, and high-risk changes. The Auditor cannot be the implementer.
- Candidate Implementer: produces patches only in an isolated branch or worktree. No commit, merge, push, deploy, protected-branch write, secrets, or forbidden scope.
- Claude: optional candidate implementer, reviewer, or spec critic only when explicitly approved. Patch-only outputs must be reviewed by Codex Auditor.
- Antigravity Visual Pod: UI/UX/graphic/browser verification specialist. Default review-only and artifact-first. Candidate UI patch requires explicit approval. No terminal, backend, auth, DB, dependency, commit, merge, push, deploy, secret, or production-data access by default.
- Gemini: future optional multimodal or cross-model reviewer only when explicitly approved. No bootstrap execution.
- Local Tooling Pod: generates deterministic evidence and does not make release or audit decisions.
- Local AI: not introduced by bootstrap. If introduced later, scratch-only unless separately governed.

## Authority model / 権限モデル

**日本語:** Supervisor は routing、accepted patch adoption、local commit を担当できますが、release authority は持ちません。Human Owner が merge、push、deploy、publish、credentials、production data、legal/privacy/brand を決めます。Candidate Implementer は patch-only で、Codex Auditor は独立 read-only です。

**English:** Supervisor may route work, adopt accepted patches, and create allowed local commits, but has no release authority. The Human Owner decides merge, push, deploy, publish, credentials, production data, and legal/privacy/brand matters. Candidate Implementer is patch-only, and Codex Auditor is independent and read-only.

Candidate patch governance is defined in `.agent-org/runbook.md`.
