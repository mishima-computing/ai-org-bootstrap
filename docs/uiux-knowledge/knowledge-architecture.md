# UI/UX Knowledge Architecture

Status: Cycle 1 docs-only decision. This file specifies future pack changes but does not edit `.agent-org/knowledge/ui/`, `pack-manifest.json`, scripts, CI, or workflows.

Related docs: [domain map](domain-map.md), [absorption ledger](absorption-ledger.md), [authoring program](authoring-program.md).

## Layers

| Layer | Location | Purpose | Authored this cycle |
| --- | --- | --- | --- |
| L1 domain-map ledger | `docs/uiux-knowledge/domain-map.md` | Full UI/UX ontology, status, sourcing plan, and coverage honesty. | Yes |
| L2 anchor index | Future `.agent-org/knowledge/ui/anchors/*.md` | Pointer-first canonical-source maps by area. Default reusable knowledge layer. | No |
| L3 profile cards | Existing `.agent-org/knowledge/ui/*.md` | Sharp 12-line cards selected explicitly by objectives. Cards cite anchor IDs after authoring cycles. | No changes |
| Demand-promoted handbooks | Future `.agent-org/knowledge/ui/handbooks/*.md` | Owned synthesis only when anchor/card compression fails. | No |

## Anchor Index Format

Future anchor files under `.agent-org/knowledge/ui/anchors/` use this format:

| Field | Rule |
| --- | --- |
| Filename | One area slug, for example `typography-cjk-latin.md`. |
| Length cap | Approximately 40 nonblank lines; exceeding the cap is a compression-failure signal. |
| Stable section IDs | Every canonical body gets a stable ID such as `#wcag22-contrast` or `#jlreq-line-composition`. |
| Content model | Public canonical pointer, date/version, scope note, local use boundary, and card-facing citation ID. No copied excerpts. |
| Fast-moving sources | Apple HIG, Material 3, market convention sources, and similar guidance must be dated in the anchor entry. |
| Card citation rule | Future cards cite anchor IDs, not raw source URLs, for every semantic guard they depend on. |

## Handbook Promotion

Handbooks are not the primary owned layer. They are demand-promoted per area only when all tests below are met.

| Promotion test | Required evidence |
| --- | --- |
| Compression failure | The area cannot fit in one anchor index at the 40 nonblank-line cap plus one or more 12-line cards without losing a needed decision rule. |
| Reuse pressure | At least two card or cycle decisions need the same cross-source synthesis. |
| Freshness plan | The handbook names source versions/dates and a re-check trigger. |
| Validator path | The handbook provides stable IDs that cards can cite, and any prose prohibition follows the graduation rule below. |
| Owner value | The handbook changes a deliverable decision listed in [domain-map.md](domain-map.md#ontology), not merely background knowledge. |

If any test fails, the area stays anchor-first and any synthesis remains in cycle notes, not reusable pack guidance.

## Prohibition Graduation Law

Binding format law for all new UI/UX knowledge artifacts:

Every textual prohibition must carry a graduation path. Permanent prose prohibitions are inadmissible.

| Graduation path | Meaning |
| --- | --- |
| Structural check | Replace the prohibition with a validator/checklist condition that can be mechanically or procedurally checked. |
| Positive rewrite | Replace the prohibition with the required positive behavior and acceptance evidence. |
| Delete | Remove the prohibition when the absorbing anchor/card makes it unnecessary. |

This law applies to:

| Surface | Application |
| --- | --- |
| [absorption-ledger.md](absorption-ledger.md) | Every existing prose prohibition is annotated with one of the three paths. |
| Future anchor/card authoring | No new `never`, `do not`, `avoid`, `forbid`, or equivalent rule lands without a path. |
| Controller boilerplate | Any boilerplate that warns controllers about UI/UX scope is ratified only if it is pack-template text, names a structural check or positive forwarding rule, and has a deletion condition once selector/profile validation is enforceable. |

## Manifest Delta

Future authoring cycles should land this manifest delta after the first anchor index is authored:

| Manifest item | Future value |
| --- | --- |
| Path | `.agent-org/knowledge/ui/anchors/` |
| Tier | Pack-level reusable knowledge, same UI/UX pack boundary as `.agent-org/knowledge/ui/`. |
| Requiredness | Required once at least one authored anchor exists. |
| Distribution | Included in pack sync so downstream repos receive anchor IDs cited by UI profile cards. |
| Boundary | Product-specific worldview knowledge remains repo-local under `.agent-org/knowledge/cards/` per the existing #32 boundary. |

Optional later delta after demand promotion:

| Manifest item | Future value |
| --- | --- |
| Path | `.agent-org/knowledge/ui/handbooks/` |
| Tier | Pack-level reusable knowledge, demand-promoted only. |
| Requiredness | Required only if any card cites a handbook ID. |

## Validator Future State

No validator change lands in Cycle 1. The future validator state is:

| Check family | Future behavior |
| --- | --- |
| Discovery | Glob-discover `.agent-org/knowledge/ui/*.md`, `.agent-org/knowledge/ui/anchors/*.md`, and later `.agent-org/knowledge/ui/handbooks/*.md`. |
| Format-only caps | Enforce existing card frontmatter, evidence pointer caps, optional exemplar format, 12 nonblank-line card body cap, and anchor approximate 40 nonblank-line cap. |
| Citation resolution | For each future card citation such as `anchor:typography-cjk-latin#jlreq-line-composition`, verify the target anchor file and stable section ID exist. |
| Phrase checks | Retire a per-card phrase check only in the authoring cycle where the absorbing area lands an anchor entry, the card cites the replacement anchor ID, and [absorption-ledger.md](absorption-ledger.md) records the retired phrase's destination. |
| Prohibition checks | Flag new prose prohibitions that lack a graduation path: structural check, positive rewrite, or delete. |
| Exemplar checks | Treat exemplar URLs as pointers only; unverified exemplars such as antgroup cannot satisfy acceptance evidence. |

The phrase-check path is a graduation path, not silent deletion. Existing phrase checks remain authoritative until their absorbing area is authored.
