# Workspace Policy / Workspaceポリシー

## Modes / モード

- `new_project`: fresh or intentionally empty local-only root for a new repository.
- `existing_repo_clean`: intentional Git repo with clean tracked files.
- `dirty_existing_repo`: Git repo with tracked modifications. Hard stop.
- `ambiguous_workspace`: unrelated project, nested repo, stale governance, or unclear root. Stop unless files resolve the ambiguity safely.
- `cloud_synced_workspace`: risk flag for OneDrive, Dropbox, iCloud Drive, Google Drive, Box, SynologyDrive, or similar sync roots.

## Rules / ルール

**日本語:** 書き込み前に workspace を分類します。raw path と realpath-equivalent の両方で cloud-sync detection を best effort で行います。`new_project` は過去の app code、dependency files、IDE settings、`.agent-org/`、`.agent-runs/`、`.claude/`、`.antigravity/` を継承しません。

**English:** Classify the workspace before writes. Detect cloud-sync risk with both raw path and realpath-equivalent checks on a best-effort basis. `new_project` must not inherit prior app code, dependency files, IDE settings, `.agent-org/`, `.agent-runs/`, `.claude/`, or `.antigravity/`.

**日本語:** `dirty_existing_repo` は hard stop です。true new project では初回 commit 前の branch 作成は任意です。existing repo bootstrap では bootstrap branch が必須です。cloud-sync risk がある場合は明示 approval なしに書き込みません。

**English:** `dirty_existing_repo` is a hard stop. Branch creation is optional before the first commit in a true new project. Existing repo bootstrap requires a bootstrap branch. If cloud-sync risk is present, do not write without explicit approval.

**日本語:** bootstrap self-audit は、changed files が governance scope に限定され、`.agent-runs/` が ignored and untracked で、forbidden paths がなく、whitespace と sanitation gates が通る場合だけ許可されます。

**English:** Bootstrap self-audit is allowed only when changed files stay within governance scope, `.agent-runs/` is ignored and untracked, forbidden paths are absent, and whitespace and sanitation gates pass.
