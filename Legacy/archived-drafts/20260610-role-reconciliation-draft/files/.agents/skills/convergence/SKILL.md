# Convergence Skill Loader

## Purpose
Load convergence-manager behavior as a stateful stop/admission controller.

## Canonical Role Spec
`roles/convergence-manager.md`

## Relevant Schema
`schemas/convergence-decision.schema.json`

## Runtime Semantics
Evaluate current objective, active packet, split requests, recent events, counters, P0/P1/P2 acceptance, and context status.

Reset only per `run_id` / `objective_id`.

Context degradation is a stop or reentry condition, not permission to expand scope.

## Authority
This skill is not adoption authority.
