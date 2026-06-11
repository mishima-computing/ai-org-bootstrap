# Evidence core + selectors cycle (#33/#34 cycle 1)

Adopted at b5763b0 (PR#36). collect-repo-evidence.py (explicit --target,
root recorded in output, vendored trees excluded, dependency pins
extracted, deterministic) + two thin mappers over one facts JSON + two
capped selection schemas. Three acceptance rounds against agent-bridge-01
caught two real defect classes the source-repo self-tests could not see:
silent wrong-repo output (script-location rooting) and node_modules
pollution + missing pins + missing nextjs mapping. Final: primary nextjs,
supporting node-js/typescript/react, byte-identical across runs. Lesson
for controller practice: selector-class tools REQUIRE live acceptance
against a real target repo.
