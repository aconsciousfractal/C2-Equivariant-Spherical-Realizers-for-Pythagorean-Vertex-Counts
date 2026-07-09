# C2-Equivariant Spherical Realizers for Pythagorean Vertex Counts

An **expository note** in elementary convex geometry and arithmetic, with
fully reproducible computational checks.

For a Pythagorean triple `(a, b, c) = (m^2 - n^2, 2mn, m^2 + n^2)` the note
constructs explicit C2-equivariant finite point sets on the spheres S^2 and
S^3 whose convex hulls are full-dimensional and have exactly

- `a + 2b + c = 2m(m + 2n)` vertices (on S^2), and
- `a + 2b + 2c + e = (m + n)(3m + n) + e` vertices (on S^3, for any declared
  integer top layer `e >= 1`),

with the doubled coefficients realized as mirror pairs of layers exchanged
by the involution. A small computed boundary atlas (merged f-vectors of the
corridor realizers) is included as data.

**Status and claims.** This note is expository and claims no new theorem:
the count sequences and the corridor identity are recorded in the OEIS
(A139267; J. M. Bergot's 2013 comment on A000567; A001844/A046092/A005408
for the classical family; A033567), the underlying convex-geometric fact
(finite subsets of spheres are in convex position) is textbook material,
and the identities are one line from the classical perimeter formula. The
note is self-published in this repository and has not been submitted to
any journal.

## Contents

| Path | What it is |
|---|---|
| `paper/*.tex` / `paper/*.pdf` | The note (LaTeX source and built PDF) |
| `paper/BUILD.md` | Exact build instructions |
| `paper/SHA256SUMS.txt` | Checksums of the paper artifacts |
| `scripts/verify_c2_realizer.py` | S^2 corridor replay, k = 1..20 (20/20) |
| `scripts/verify_s3_realizer.py` | S^3 integer-layer check, 50 runs (50/50, 4D hulls) |
| `scripts/atlas_boundary.py` | Boundary atlas: merged f-vectors, k ≤ 20, 3 heights (60/60) |
| `scripts/check_oeis_prior_art.py` | Symbolic identity checks + OEIS term diffs (11/11) |
| `results/` | CSV/txt outputs of the four scripts |
| `sources/oeis/` | Snapshots of the cited OEIS entries (see attribution below) |

## Reproducing

Requirements: Python 3 with `numpy`, `scipy`, `sympy`.

```
cd scripts
python verify_c2_realizer.py
python verify_s3_realizer.py
python atlas_boundary.py
python check_oeis_prior_art.py
```

Each script prints a pass/fail summary and rewrites its output under
`results/`. All computations are implementation checks and descriptive
data; none is an ingredient in the proofs.

## OEIS attribution

The files in `sources/oeis/` are unmodified JSON snapshots of the entries
A000567, A001844, A033567, A046092, A139267 from the
[On-Line Encyclopedia of Integer Sequences](https://oeis.org)
(© The OEIS Foundation Inc.), included for reproducibility of
`check_oeis_prior_art.py` under the
[CC BY-SA 4.0 license](https://oeis.org/LICENSE) with attribution.

## License and citation

Code and text of this repository: MIT License (see `LICENSE`).
To cite, see `CITATION.cff`.
