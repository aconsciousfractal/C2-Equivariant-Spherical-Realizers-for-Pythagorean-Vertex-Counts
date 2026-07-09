"""Verify the C2-equivariant corridor realizer (Theorem 6.1 of the paper).

For k = 1..KMAX build G_k = A_k | B_k+ | B_k- | C_k on S^2 with
(a,b,c) = (2k+1, 2k(k+1), 2k(k+1)+1) and check:
  - layer disjointness (all |G_k| points distinct),
  - every point is a convex-hull vertex,
  - |Vert(Conv(G_k))| = a + 2b + c = 2(k+1)(3k+1).

Writes results/baseline_k1_20.csv. The proof itself is computation-free;
this is an implementation check (paper, Appendix A).
"""

import csv
import os
import numpy as np
from scipy.spatial import ConvexHull

KMAX = 20
H = 0.5
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "baseline_k1_20.csv")


def layer(n, z, phase):
    r = np.sqrt(1.0 - z * z)
    return [
        (r * np.cos(2 * np.pi * (i / n + phase)),
         r * np.sin(2 * np.pi * (i / n + phase)),
         z)
        for i in range(n)
    ]


def main():
    rows = []
    all_ok = True
    for k in range(1, KMAX + 1):
        a, b, c = 2 * k + 1, 2 * k * (k + 1), 2 * k * (k + 1) + 1
        assert a * a + b * b == c * c
        expected = a + 2 * b + c
        assert expected == 2 * (k + 1) * (3 * k + 1)
        G = (layer(a, H, 0.0) + layer(b, 0.0, 1 / (4 * b))
             + layer(b, 0.0, -1 / (4 * b)) + layer(c, -H, 0.0))
        P = np.array(G)
        distinct = len(np.unique(np.round(P, 12), axis=0)) == len(P)
        nv = len(ConvexHull(P).vertices)
        ok = distinct and nv == expected
        all_ok &= ok
        rows.append([k, a, b, c, len(P), nv, expected, "OK" if ok else "FAIL"])

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["k", "a", "b", "c", "points", "hull_vertices", "expected", "status"])
        w.writerows(rows)

    print(f"k=1..{KMAX}: {'ALL OK' if all_ok else 'FAILURES PRESENT'}; "
          f"first count {rows[0][6]}, last count {rows[-1][6]}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
