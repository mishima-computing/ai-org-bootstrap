---
profile_id: ui-bilingual-typography
scope: Human-facing bilingual CJK+Latin text surfaces.
covers: lead language; per-script tokens; CJK mass; measure budgets; mixed-script spacing; noise budget; localization boundary.
freshness: Medium horizon; re-check on W3C req revision or accessibility-guidance change.
supersede_trigger: Supersede on product Stage-A contradiction, JLREQ/CLREQ revision, or accessibility review.
evidence_refs: ALA-cross-cultural-design; justfont-zhongying-mixing; The-Plant-line-length; W3C-JLREQ-CLREQ; NNg-text-over-images+crosscultural; Heti-mixed-script-spacing
---

Fact: CJK glyph density carries different visual mass than Latin, so shared rhythm can mislead focus.
Rule: Choose one lead language per view; use 襯托法 by default and forbid both-prominent treatment with no focal point.
Tokens: Maintain per-script size, leading, and measure token sets; never share one token set across CJK and Latin.
Measure: Treat EN ~45-75ch and JA ~15-40ch as research budgets validated by product tests, not fixed constants; one container cannot serve both.
Spacing: Correct mixed-script spacing per Heti convention, including 1/4-em class gaps and punctuation squeeze.
Noise: Enforce contrast floors by script and display size, with 4.5:1 body and 3:1 large-display floors judged on the worst-case image region.
Boundary: Translation-only preserves structure; localization may change per-language IA and visual design when focus, scan path, or density requires it.
Detail: Bind mixed-setting micro-rules to JLREQ/CLREQ and cite them instead of restating local exceptions in pack cards.
Claim limit: Claim legibility and focus effects only; never claim conversion, engagement, or SEO outcomes.
Pointers: ALA cross-cultural design, justfont mixing, The Plant line length, W3C JLREQ/CLREQ, NN/g text-over-images plus crosscultural, Heti spacing.
