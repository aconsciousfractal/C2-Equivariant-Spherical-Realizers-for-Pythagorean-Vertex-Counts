"""Boundary atlas for the corridor realizer (Section 8 of the paper).

For each k (corridor triple, Euclid (k+1,k)) and each height h, build G_k
exactly as in the paper (phases 0, +-1/(4b), 0), take the 3D convex
hull, MERGE the qhull triangulation into true planar faces (grouping facet
plane equations), and record the honest f-vector:
  V (vertices), E (= sum of face sizes / 2), F (merged faces),
  Euler check V - E + F == 2, and the face-size profile.

Purely descriptive: no f-vector formula is claimed anywhere. The vertex
count V is parameter-free (theorem); E and F are properties of the specific
realizer and are recorded per h to test parameter dependence empirically.

Writes ../results/atlas_boundary.csv.
"""
import csv
import os
from collections import Counter

import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "atlas_boundary.csv")

HS = (0.2, 0.5, 0.8)
KS = range(1, 21)


def latitude(n, z, phi):
    r = np.sqrt(1.0 - z * z)
    i = np.arange(n)
    ang = 2 * np.pi * (i / n + phi)
    return np.column_stack([r * np.cos(ang), r * np.sin(ang), np.full(n, float(z))])


def corridor_points(k, h):
    a, b, c = 2 * k + 1, 2 * k * (k + 1), 2 * k * (k + 1) + 1
    G = np.vstack([latitude(a, h, 0.0),
                   latitude(b, 0.0, 1.0 / (4 * b)),
                   latitude(b, 0.0, -1.0 / (4 * b)),
                   latitude(c, -h, 0.0)])
    return (a, b, c), G


def merged_f_vector(points, tol=7):
    hull = ConvexHull(points)
    V = len(hull.vertices)
    # group triangulated facets by their (outward) plane equation
    groups = {}
    for eq, simplex in zip(hull.equations, hull.simplices):
        key = tuple(np.round(eq, tol))
        groups.setdefault(key, set()).update(simplex.tolist())
    face_sizes = sorted(len(v) for v in groups.values())
    F = len(face_sizes)
    twice_E = sum(face_sizes)
    if twice_E % 2:
        raise RuntimeError("face-size sum odd: merging tolerance failed")
    E = twice_E // 2
    return V, E, F, face_sizes


def main():
    rows = []
    for k in KS:
        per_h = []
        for h in HS:
            (a, b, c), G = corridor_points(k, h)
            V, E, F, sizes = merged_f_vector(G)
            euler = V - E + F
            profile = dict(Counter(sizes))
            per_h.append((V, E, F))
            rows.append(dict(k=k, a=a, b=b, c=c, h=h, V=V, E=E, F=F,
                             euler=euler,
                             expected_V=a + 2 * b + c,
                             V_ok=V == a + 2 * b + c,
                             euler_ok=euler == 2,
                             face_profile=str(sorted(profile.items()))))
        stable = len(set(per_h)) == 1
        for r in rows[-len(HS):]:
            r["h_stable"] = stable
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if not (r["V_ok"] and r["euler_ok"])]
    unstable = sorted({r["k"] for r in rows if not r["h_stable"]})
    print(f"{len(rows)} rows ({len(list(KS))} k-values x {len(HS)} heights); "
          f"V/Euler failures: {len(bad)}; h-unstable k: {unstable or 'none'}")
    # compact atlas view at h = 0.5
    print("k  (a,b,c)          V     E     F   profile")
    for r in rows:
        if r["h"] == 0.5:
            print(f"{r['k']:>2} ({r['a']},{r['b']},{r['c']})".ljust(20)
                  + f"{r['V']:>5} {r['E']:>5} {r['F']:>4}   {r['face_profile']}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
