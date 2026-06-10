# Role: local-tooling-pod

## Purpose
Run deterministic non-LLM checks.

## Primary Carrier
Deterministic scripts.

## Secondary Carrier
None.

## Authority
May collect local evidence and produce machine-readable reports.

## Forbidden Actions
Must not make release, audit, adoption, or product decisions.

## Inputs
Repository checkout, work packet, candidate diff, allowed files, forbidden files, and check commands.

## Required Output
Deterministic gate evidence.

## Stop Conditions
Required tool unavailable, patch cannot be parsed, forbidden path touched, or check cannot run.

## Evidence Requirements
Git status, HEAD SHA, patch parse, isolated patch apply, forbidden path check, secret scan, lint, typecheck, tests, build, local migration up/down, and artifact hash when applicable.

## Interaction With Other Roles
Feeds Gate Report Builder and auditors.

## Anti-patterns
Inferring intent, hiding failed checks, or deciding adoption.

## Notes For Carrier Adapters
Canonical role spec controls behavior. This is a deterministic role.
