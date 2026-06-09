# Workspace Policy

## Modes

- `new_project`: fresh or intentionally empty local-only root for a new repository.
- `existing_repo_clean`: intentional Git repo with clean tracked files.
- `dirty_existing_repo`: Git repo with tracked modifications. Hard stop.
- `ambiguous_workspace`: unrelated project, nested repo, stale governance, or unclear root. Stop unless files resolve the ambiguity safely.
- `cloud_synced_workspace`: risk flag for OneDrive, Dropbox, iCloud Drive, Google Drive, Box, SynologyDrive, or similar sync roots.

## Rules

Classify the workspace before writes.

Detect cloud-sync risk with both raw path and realpath-equivalent checks on a best-effort basis.

`new_project` must not inherit prior app code, dependency files, IDE settings, `.agent-org/`, `.agent-runs/`, `.claude/`, or `.antigravity/`.

`dirty_existing_repo` is a hard stop.

Branch creation is optional before the first commit in a true new project. Existing repo bootstrap requires a bootstrap branch.

If cloud-sync risk is present, do not write without explicit approval.

Bootstrap self-audit is allowed only when changed files stay within governance scope, `.agent-runs/` is ignored and untracked, forbidden paths are absent, and whitespace and sanitation gates pass.
