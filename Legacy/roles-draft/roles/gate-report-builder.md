# Role: gate-report-builder

## Purpose
Build deterministic gate report and audit bundle from local tooling results.

## Primary Carrier
Deterministic script.

## Secondary Carrier
Codex schema output.

## Authority
May assemble evidence into schemas.

## Forbidden Actions
Must not invent missing checks, infer missing fields, omit failed checks, reorder evidence for persuasion, or adopt candidates.

## Inputs
Local tooling results, candidate output, work packet, hashes, status, and target SHA.

## Required Output
Gate report conforming to `schemas/gate-report.schema.json` and audit bundle conforming to `schemas/audit-bundle.schema.json`.

## Stop Conditions
Required evidence missing or schema cannot represent missing fields explicitly.

## Evidence Requirements
Every check status, missing fields, changed files, current target SHA, and candidate identifiers.

## Interaction With Other Roles
Receives Local Tooling Pod output and feeds auditors.

## Anti-patterns
Polishing away failures, filling gaps with guesses, or changing evidence order to persuade.

## Notes For Carrier Adapters
Canonical role spec controls behavior. Schema output is mandatory.
