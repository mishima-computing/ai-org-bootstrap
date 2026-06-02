# Artifact Retention Policy / Artifact保持ポリシー

**日本語:** `.agent-runs/` は raw local runtime material です。既定で ignored and untracked にし、commit しません。

**English:** `.agent-runs/` is raw local runtime material. It is ignored and untracked by default and must not be committed.

## Raw material / Raw material

Raw material includes prompts, invocation manifests, stdout/stderr, model and tool metadata, tool versions, parameters, parsed patch extraction notes, candidate base SHA records, screenshots, recordings, DOM snapshots, browser traces, visual comparison images, and candidate artifacts.

## Committed history / Commitされる履歴

**日本語:** commit する履歴は `.agent-org/history/` の sanitized summaries のみです。secrets、credentials、raw prompts、raw stderr、local absolute paths、personal data、customer data、raw screenshots、recordings を含めません。

**English:** Committed history is limited to sanitized summaries under `.agent-org/history/`. It must exclude secrets, credentials, raw prompts, raw stderr, local absolute paths, personal data, customer data, raw screenshots, and recordings.

**日本語:** cloud-sync path は raw artifact exposure risk を増やします。commit 前に sanitation gate を通します。

**English:** Cloud-sync paths increase raw artifact exposure risk. Run a sanitation gate before commit.
