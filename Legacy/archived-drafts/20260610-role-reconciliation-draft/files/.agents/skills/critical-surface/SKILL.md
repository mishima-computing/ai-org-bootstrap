# Critical Surface Skill Loader

## Purpose
Load critical-surface gate classification behavior.

## Canonical Role Spec
`roles/critical-surface-manager.md`

## Relevant Schema
`schemas/critical-surface-decision.schema.json`

## Required Semantics
1. Classify gates; do not implement.
2. Convert critical surfaces into lower-risk allowed work plus gated actions.
3. Use L0 through L5.
4. Continue below the blocked gate when safe work remains.
5. Require explicit human approval for L5.
6. Reject vague blockers.

## Authority
This skill is not adoption authority.
