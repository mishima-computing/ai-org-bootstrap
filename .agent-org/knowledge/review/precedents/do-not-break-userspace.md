---
precedent_id: do-not-break-userspace
profile_id: do-not-break-userspace
scope: Kernel review precedent for user-visible behavior compatibility and regressions.
covers: Canonical quoted label for userspace breakage; user workflow breakage; compatibility regression pressure.
freshness: Low-rot primary LKML anchor from 2012-12-23; re-check on documented kernel userspace-compatibility policy shift.
supersede_trigger: Supersede only on a documented kernel-review culture or policy shift that changes userspace compatibility expectations.
evidence_refs: 2012-12-23 https://lkml.org/lkml/2012/12/23/75
lens_nn_map: unverified-integration:NN3; silent-failure:NN4
authority: persuasive-not-binding; never-overrides-NN1-NN4
---

Quoted precedent label: "do not break userspace".
Review use: cite when a change makes previously working user behavior fail without verified migration evidence.
Claim limit: this does not prove a repo-specific regression; Linon still needs file:line evidence and live checks where runtime truth is required.
Authority: persuasive-not-binding and never overrides NN1-NN4.
