# UI/UX Profile Cards

## Purpose

UI/UX profile cards are pack-level knowledge pointers for objectives that explicitly declare design capability needs. They do not authorize selector inference of design intent.

## Profile Card Format

Each card has exactly these frontmatter keys: `profile_id`, `scope`, `covers`, `freshness`, `supersede_trigger`, and `evidence_refs`.

Caps: evidence_refs cap: 6 pointers, separated by semicolons; body cap: 12 nonblank lines; no embedded research excerpts.

F11 boundary: profile cards carry reusable UI/UX constraints only. Product-specific worldview cards, for example `yatai`, stay repo-local under `.agent-org/knowledge/cards/` per the #32 boundary.

## Use

An objective may name UI/UX profiles in Experience Constraints. Controllers forward those names verbatim; `conservative-designer` may use only named profiles and still respects the `selected_profiles` cap of 5.
