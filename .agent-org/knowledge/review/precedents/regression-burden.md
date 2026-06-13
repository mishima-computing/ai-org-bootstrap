---
precedent_id: regression-burden
profile_id: regression-burden
scope: Kernel review precedent for handling regressions as kernel-owned user-workflow breakage.
covers: Regression reporting burden; revert pressure; user workflow as the review object.
freshness: Low-rot primary LKML anchor from 2012-12-23; re-check on documented kernel regression-handling policy shift.
supersede_trigger: Supersede when kernel review culture or documentation materially changes regression handling or user-workflow policy.
evidence_refs: 2012-12-23 https://lkml.iu.edu/hypermail/linux/kernel/1212.2/03058.html
lens_nn_map: silent-failure:NN4; unverified-integration:NN3
authority: persuasive-not-binding; never-overrides-NN1-NN4
---

Quoted precedent label: "It's a bug alright - in the kernel."
Review use: cite when a change hides, normalizes, or shifts the burden of a user-visible regression.
Claim limit: the card supports regression framing, not a binding outcome.
See also: https://docs.kernel.org/process/handling-regressions.html for living regression-process guidance.
Linon must still cite repository evidence for the defect and disclose runtime-only gaps.
Authority: persuasive-not-binding and never overrides NN1-NN4.
