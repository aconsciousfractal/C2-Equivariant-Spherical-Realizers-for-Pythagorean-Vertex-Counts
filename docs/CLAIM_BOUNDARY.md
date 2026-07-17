# Claim Boundary

Level column uses the official PAPP taxonomy
(Gate-Disciplined-Computational-Mathematics/docs/CLAIM_LEVELS.md); added
2026-07-17 (ledger A-1).

This repository is an **expository, no-novelty note**. It **claims no CLx
result** (no CL1–CL6 promotable result of its own): the repository originates
**CLM metadata and CL0 observation only**. The mathematical content it presents
is classical and enters by external reference (CL4 imports that belong to the
cited sources, not to this repo); the note asserts **no internal theorem (no
CL5)**, as the README's "Status and claims" section already states verbatim.

This file is a **companion / additive** boundary note. It **does not alter** any
claim wording, identity, script, verifier pointer, or scope caveat in the
README, the paper, or the sources. It only records the official CL code that
each pre-existing element already corresponds to.

## Boundary crosswalk (repo element → official CL code)

| Repo element | Pre-existing wording (unchanged) | Official CL |
|---|---|---|
| Overall note | "expository and claims no new theorem" (README) | no CLx result (CLM/CL0 only) |
| Vertex-count identities `a+2b+c = 2m(m+2n)` (S^2), `a+2b+2c+e` (S^3) | "one line from the classical perimeter formula"; recorded in OEIS | CL4 (external import — belongs to the cited classical/OEIS sources, not a result of this repo; no CL5 internal theorem asserted) |
| Convex-position fact (finite sphere subsets in convex position) | "textbook material" (README) | CL4 (external import — textbook) |
| `scripts/verify_c2_realizer.py` output (S^2 replay, k = 1..20) | "implementation checks and descriptive data; none is an ingredient in the proofs" | CL0 (descriptive output; a bounded replay path exists but the note disclaims it as a result) |
| `scripts/verify_s3_realizer.py` output (S^3 integer-layer, 50 runs) | same disclaimer as above | CL0 (descriptive output) |
| `scripts/atlas_boundary.py` + `results/atlas_boundary.csv` (merged f-vectors) | "A small computed boundary atlas ... is included as data" | CL0 (descriptive computed data) |
| `scripts/check_oeis_prior_art.py` output (symbolic identity + OEIS term diffs) | "implementation checks and descriptive data" | CL0 (descriptive prior-art check) |
| `results/*.csv`, `results/*.txt` | script outputs | CLM (recorded outputs / data artifacts) |
| `sources/oeis/*.json` (A000567, A001844, A033567, A046092, A139267) | "unmodified JSON snapshots ... included for reproducibility" | CLM (source snapshots / metadata) |
| `paper/SHA256SUMS.txt` | checksums of the paper artifacts | CLM (manifest / integrity metadata) |
| `CITATION.cff`, `LICENSE`, `paper/BUILD.md` | citation, license, build instructions | CLM (metadata) |

Where a level was uncertain, the **weaker** level was recorded (PAPP
"weakest sufficient" rule): the reproducibility scripts have a bounded replay
path (which would read as CL2), but because the note itself disclaims them as
"not ... an ingredient in the proofs" and presents them as descriptive checks,
they are recorded here at **CL0**, not CL2.

## Manifest / verifier status

- `paper/SHA256SUMS.txt` pins only the two paper artifacts (`.tex`, `.pdf`),
  both under `paper/`. This `docs/` file is **outside that manifest's scope**,
  so **no repin is required** and none was performed.
- The four `scripts/verify_*.py` / `atlas_boundary.py` / `check_oeis_prior_art.py`
  scripts verify mathematical content, not this boundary note; this additive
  file does not affect their outcomes.
