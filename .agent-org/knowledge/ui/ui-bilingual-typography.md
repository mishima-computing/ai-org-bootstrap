---
profile_id: ui-bilingual-typography
scope: Human-facing bilingual CJK+Latin text surfaces.
covers: lead language; per-script tokens; CJK mass; measure budgets; mixed-script spacing; noise budget; localization boundary.
freshness: Medium horizon; re-check on W3C req revision, jlreq-d publication signal, or accessibility-guidance change.
supersede_trigger: Supersede on product Stage-A contradiction, JLREQ/CLREQ revision, or accessibility review.
evidence_refs: anchor:typography-cjk-latin#jlreq-line-composition; anchor:typography-cjk-latin#clreq-mixed-spacing; anchor:typography-cjk-latin#wcag22-visual-presentation; anchor:typography-cjk-latin#iso40500-status; anchor:typography-cjk-latin#bringhurst-measure-rhythm
---

Fact: CJK glyph density carries different visual mass than Latin, so rhythm needs per-script validation; cite anchor:typography-cjk-latin#jlreq-line-composition and anchor:typography-cjk-latin#bringhurst-measure-rhythm.
Rule: Choose one lead language per view; use 襯托法 by default and forbid both-prominent treatment with no focal point.
Tokens: Provide per-script size, leading, and measure token sets, citing anchor:typography-cjk-latin#jlreq-line-composition and anchor:typography-cjk-latin#bringhurst-measure-rhythm.
Measure: Treat EN ~45-75ch and JA ~15-40ch as research budgets validated by product tests; mixed containers declare per-script behavior.
Spacing: Bind mixed-script spacing and punctuation squeeze to anchor:typography-cjk-latin#jlreq-mixed-spacing and anchor:typography-cjk-latin#clreq-mixed-spacing.
Noise: Enforce contrast floors by script and display size, with 4.5:1 body and 3:1 large-display floors judged on the worst-case image region; cite anchor:typography-cjk-latin#wcag22-visual-presentation.
Boundary: Translation-only preserves structure; localization may change per-language IA and visual design when focus, scan path, or density requires it.
Detail: Bind mixed-setting micro-rules to anchor:typography-cjk-latin#jlreq-line-composition and anchor:typography-cjk-latin#clreq-mixed-spacing.
Claim limit: Claim legibility and focus effects only; never claim conversion, engagement, or SEO outcomes.
Pointers: anchor:typography-cjk-latin#jlreq-d-watch; anchor:typography-cjk-latin#iso40500-status.
