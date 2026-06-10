# Genius A/B Evaluation Protocol

Issue #12 records the measured genius-v1 baseline, the first retrospective v2 pair, the composite evaluation metric, and the protocol for future A/B comparisons. This document is the permanent record of the decision; it does not modify role specs, schemas, adapters, CI, or workflow defaults.

## V1 baseline results

The measured v1 baseline covers 10 completed designer cycles. The source run set contained 88 distinct genius items, counted from `core_mechanisms` plus `what_to_copy` and judged against the corresponding `aufheben-designer` implementation contract.

| Measure | Value |
| --- | --- |
| Cycles measured | 10 |
| Items handed off | 88 |
| Used items | 80 |
| Partial uses included in used | 9 |
| Rejected items | 8 |
| Ignored items | 0 |
| Nominal survival | 90.9% |
| Full-fidelity survival | ~81% |

Nominal survival is 90.9% because 80 of 88 handed-off items survived into the contracts, including 9 partial survivals. Full-fidelity survival is ~81% because partial survivals are discounted. These figures must not be conflated: the nominal figure measures traceable engagement, while the full-fidelity figure better approximates unmodified adoption.

Zero ignored items is attributed to the contract format forcing engagement through `rejected_parts`. Every v1 item was either reflected in the contract or explicitly rejected; none disappeared silently.

### Mortality analysis

Ground-truth facts survive at ~100%. Examples include verified API surfaces, documented field names, protocol envelopes, runtime constraints, and source-confirmed product semantics.

ALL mortality is discretionary suggestions: defaults, extras, architectural alternatives, or optional process choices. The 8 rejected items were not rejected because the source fact was wrong; they were rejected because the contract chose a narrower or different implementation path.

Rejection causes were mostly external constraints or repo facts genius did not verify:

- File allowlists blocked otherwise plausible changes.
- Frozen manifests and CI constraints ruled out dependency or workflow expansion.
- Existing repo facts overrode generic precedent, such as the absent server transformer that made superjson client wiring invalid.
- Some suggested extras were out of scope, such as health/stat polling, keep-alive response headers, or content-addressed storage.

The v1 baseline therefore shows high engagement but also reveals why `survival_rate` alone is inflated: cheap suggestions and broad precedent vocabulary can survive nominally without being the most load-bearing part of the design.

## First v2 pair: key-lifecycle

The first v2 pair is the key-lifecycle objective in `20260611-041358-270f526`.

Retrospective caveat: the implementation contract predates the v2 packet. The v2 packet was judged against a contract that had already been synthesized, so the results are a retrospective comparison rather than evidence that v2 caused the contract content.

The v2 packet contained 3 hypotheses and 4 guardrails.

| V2 item | Outcome |
| --- | --- |
| H1: scope already implemented | Detected a STALE OBJECTIVE: the controller substrate claimed the lifecycle work was not implemented, but current working-tree evidence showed it already existed. This is a category v1 cannot produce because v1 did not read and verify repo state in that way. |
| H2: revoke/lastUsed race handled | Matched contract requirements exactly. The contract required store-level preservation of revoked status during stale `lastUsedAt` updates, plus a 60-second write threshold and fire-and-forget usage recording. |
| H3: optional ledger-event gap | Agreement-via-rejection. V2 identified `auth.key_revoked` as optional and valid to skip; the contract explicitly rejected/cut the ledger event. |
| Guardrails | Used. The contract retained no revoked-vs-unknown oracle, no un-revoke/expiry/rotation/scope expansion, listed revoked keys, and frozen manifests/CI boundaries. |

The paired finding is that v1 supplied broad external precedent vocabulary for revocation, last-used tracking, generic auth failure responses, and lazy schemaless migration. V2 supplied repo-anchored verification, including the stale-objective finding, exact implementation evidence, and concrete rejection conditions.

## Composite metric

Future comparisons must use a composite metric rather than raw survival alone.

### `survival_rate`

Definition: items judged `USED`, including explicitly partial uses, divided by total items handed off.

Computation: for each packet, enumerate the handed-off items, then judge each item against the downstream contract as `USED`, `REJECTED`, or `IGNORED`. Report partial uses separately so the nominal survival figure and full-fidelity figure remain distinct.

Rationale: this preserves continuity with the measured v1 baseline of 90.9% nominal survival and ~81% full-fidelity survival.

### `load_bearing_rate`

Definition: items cited as requirements or acceptance criteria over items handed off.

Computation: count a handed-off item as load-bearing only when it becomes a concrete requirement, acceptance criterion, security requirement, nonfunctional requirement, file-scope rule, or explicit implementation constraint in the downstream contract. General background, vocabulary, or optional rationale does not count unless the contract makes it binding.

Rationale: this separates merely surviving ideas from items that actually constrain implementer behavior.

### `reverification_burden`

Definition: genius claims the designer re-checked, or that proved wrong, over items handed off.

Computation: count each claim that forced the designer to verify repo state, installed dependency behavior, schema/config facts, or source accuracy before it could be safely used. Also count claims later found wrong or stale. Example: v1 missed the absent superjson transformer, so the designer had to re-check and reject superjson client wiring.

Rationale: a packet that survives only after heavy designer re-verification is less valuable than one that carries verified claims and clear evidence references.

### `bad_idea_prevention`

Definition: refuted or rejected items not reintroduced downstream.

Computation: track items explicitly rejected by genius, by the designer, or by later evidence. Score credit when the bad idea stays out of the downstream contract and later implementation guidance. Count regressions when a rejected idea reappears downstream without new evidence.

Rationale: good A/B output is not only what gets adopted; it is also what prevents known-bad ideas from re-entering the design.

### Qualitative notes

Each pair must include qualitative notes. Survival rate alone is inflated by cheap suggestions, especially broad vocabulary that is easy to mention in a contract. Notes should identify whether surviving items were ground-truth facts, binding requirements, optional vocabulary, rejected-but-useful guardrails, or stale-substrate findings.

## Protocol mechanics

Each A/B pair compares packets for the same objective. The normal comparison is v1-vs-v2; after v2 becomes the baseline, the same mechanism may compare vN-vs-vN+1.

The judge is post-hoc LLM/manual matching over run artifacts. The judge reads the packet artifacts and the downstream contract, enumerates distinct handed-off items, and assigns `USED`, `REJECTED`, or `IGNORED`. Paraphrase counts only when the mechanism is unmistakably the same.

The contract schema is never extended for tracing. Traceability comes from artifact comparison and this protocol's metric definitions, not from adding fields to the implementation-contract schema.

Protocol records must include:

- The objective and run artifact identifiers.
- The compared packet versions.
- The downstream contract identifier.
- Item enumeration rules.
- Per-item judgments.
- Composite metric results.
- Qualitative notes.
- Hazards observed during the pair.

### Recorded hazards

Substrate state must be recorded AND fresh. The first v2 pair found a stale-substrate hazard: the controller substrate said key lifecycle work still needed implementation, while direct working-tree evidence showed the scope was already implemented and tested. Future packets must record substrate state with enough freshness evidence that stale objectives can be detected.

Schema supplied via flag AND file must agree. The precedence hazard is that a run can receive schema information through both an invocation flag and a schema file; if they diverge, the judge or role may follow the wrong source of truth. Future A/B runs must record both sources when present and verify agreement before judging or producing a contract.

## Verdict and open questions

Verdict recorded: v2 is adopted as the default genius for future work. This document records that verdict only; it does not enact role, workflow, adapter, or schema changes.

The reason is not raw item count. V1 has a strong nominal survival baseline, but v2 produced repo-grounded findings, lower reverification burden, explicit rejection conditions, and the stale-objective category that v1 cannot produce.

V1's residual advantage remains an open question: breadth of external precedent vocabulary. Candidate follow-ups are:

- A widen-then-gate hybrid: collect broad external precedent first, then gate it through v2-style repo verification and evidence scoring.
- Richer substrate cards: give v2 more structured outside precedent and repo-state context without losing the verification discipline.

No hybrid or richer substrate mechanism is implemented by this document.
