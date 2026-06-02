# Artifact Retention Policy

`.agent-runs/` is raw local runtime material. It is ignored and untracked by default and must not be committed.

## Raw material

Raw material includes prompts, invocation manifests, stdout and stderr, model and tool metadata, tool versions, parameters, parsed patch extraction notes, candidate base SHA records, screenshots, recordings, DOM snapshots, browser traces, visual comparison images, and candidate artifacts.

## Committed history

Committed history is limited to sanitized summaries under `.agent-org/history/`.

Committed files must exclude secrets, credentials, raw prompts, raw stderr, local absolute paths, personal data, customer data, raw screenshots, recordings, and unredacted candidate artifacts.

Cloud-sync paths increase raw artifact exposure risk.

Run a sanitation gate before commit.
