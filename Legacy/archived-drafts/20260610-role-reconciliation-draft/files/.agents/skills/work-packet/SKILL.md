# Work Packet Skill Loader

## Purpose
Load executable work packet dispatch behavior.

## Canonical Role Spec
`roles/work-packet-dispatcher.md`

## Relevant Schema
`schemas/work-packet.schema.json`

## Runtime Semantics
Convert one accepted convergence decision into one scoped, file-bound packet.

Include assigned role, primary carrier, input context, expected artifacts, evidence, guardrails, and exit rules.

Do not expand P0 or admit vague packets without concrete artifacts and evidence.

## Authority
This skill is not adoption authority.
