# Linon Review Precedents

## Purpose

This shelf gives Linon a local-first cache of dated, fetchable kernel-review precedents. It is persuasive only: a local hit never binds a finding, never overrides NN1-NN4, and never blocks PR creation by absence.

## Precedent Card Format

Each precedent card mirrors the ecosystem-card frontmatter grammar and adds review relevance keys. Required frontmatter keys: `precedent_id`, `profile_id`, `scope`, `covers`, `freshness`, `supersede_trigger`, `evidence_refs`, `lens_nn_map`, and `authority`.

Caps: `evidence_refs` cap: 6 pointers, separated by semicolons; each pointer is `YYYY-MM-DD URL`; body cap: 12 nonblank lines; no embedded essays or research excerpts.

Basename contract: card filename stem must equal `precedent_id`, and `profile_id` must equal `precedent_id`; renames are selection-breaking.

Selection: `scripts/select-review-precedents.py` selects only from a Linon-supplied review-time key. The key may be a lens, an NN class, or `lens:NN-class`. It never scans repository manifests, configs, dependency pins, or arbitrary review prose.

Authority: every card must state `persuasive-not-binding` and that precedent never overrides NN1-NN4. A cached precedent lacking a dated fetchable anchor is invalid under NN1 recursion.

Quoting convention: canonical kernel wording may appear only as a quoted label tied to a dated source anchor. New free prohibition prose is not precedent.

## Lens / NN-Class Vocabulary

Allowed lenses: `self-report-trust`, `forgeability`, `unverified-integration`, `silent-failure`, and `other`.

Allowed NN classes: `NN1`, `NN2`, `NN3`, `NN4`, and `none`.

`lens_nn_map` is a semicolon-separated list such as `unverified-integration:NN3; silent-failure:NN4`.

## Declared Gaps

- `talk-is-cheap-show-me-the-code`: no fetchable dated primary anchor was verified for this cycle; do not add an entry from quote aggregators or paraphrase.
- `good-taste-maintainability`: no fetchable dated primary anchor was verified for this cycle; keep as a gap until genius verifies a primary dated source.

The shelf may grow toward a 15-30 entry ceiling only by promote-on-demand from repeated verified use. It is not padded to a floor.
