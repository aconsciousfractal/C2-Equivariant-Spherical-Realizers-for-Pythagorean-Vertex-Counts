"""S^3 integer-layer (1,2,2,1) realizer check (Theorem 7.4 of the paper).

Construction (paper, Section 7): latitude circle layers in S^3,
  R4(n, zeta, w, phi) = {(rho cos 2pi(i/n+phi), rho sin 2pi(i/n+phi), zeta, w)},
  rho = sqrt(1 - zeta^2 - w^2) > 0,
reflection sigma4(x,y,z,w) = (x,y,z,-w).
Layers: A = R4(a, za, 0), E = R4(e, ze, 0)  (sigma4-fixed),
        B+- = R4(b, zb, +-tb), C+- = R4(c, zc, +-tc)  (swapped pairs).
Claim: all a+2b+2c+e points are distinct and are exactly the vertices of
their 4D convex hull; for Euclid triples a+2b+2c = (m+n)(3m+n).

Checks per case: layer disjointness, sigma4-equivariance (set equality),
hull vertex count == a+2b+2c+e == (m+n)(3m+n)+e.
Writes ../results/s3_realizer_check.csv.
"""
import csv
import os

import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "s3_realizer_check.csv")

ZA, ZE = 0.5, -0.4          # sigma4-fixed layers (w = 0), distinct heights
ZB, TB = 0.3, 0.35          # b-pair at w = +-TB
ZC, TC = -0.25, 0.6         # c-pair at w = +-TC


def layer(n, zeta, w, phi=0.0):
    rho = np.sqrt(1.0 - zeta**2 - w**2)
    i = np.arange(n)
    ang = 2 * np.pi * (i / n + phi)
    return np.column_stack([rho * np.cos(ang), rho * np.sin(ang),
                            np.full(n, float(zeta)), np.full(n, float(w))])


def build(a, b, c, e):
    layers = [layer(a, ZA, 0.0), layer(b, ZB, TB), layer(b, ZB, -TB),
              layer(c, ZC, TC), layer(c, ZC, -TC), layer(e, ZE, 0.0)]
    return layers, np.vstack(layers)


def as_set(pts, tol=9):
    return {tuple(np.round(p, tol)) for p in pts}


def check_case(m, n, e):
    a, b, c = m * m - n * n, 2 * m * n, m * m + n * n
    layers, G = build(a, b, c, e)
    expected = a + 2 * b + 2 * c + e
    identity_ok = (expected - e) == (m + n) * (3 * m + n)
    # distinctness (all layers together)
    distinct_ok = len(as_set(G)) == expected
    # equivariance: sigma4(G) == G as a set
    sG = G.copy()
    sG[:, 3] *= -1
    equiv_ok = as_set(sG) == as_set(G)
    # on-sphere sanity
    sphere_ok = np.allclose(np.linalg.norm(G, axis=1), 1.0)
    hull = ConvexHull(G)
    hull_ok = len(hull.vertices) == expected
    ok = identity_ok and distinct_ok and equiv_ok and sphere_ok and hull_ok
    return dict(m=m, n=n, a=a, b=b, c=c, e=e, points=expected,
                hull_vertices=len(hull.vertices), expected=expected,
                identity=identity_ok, distinct=distinct_ok, equivariant=equiv_ok,
                status="OK" if ok else "FAIL")


def main():
    cases = []
    for k in range(1, 13):                      # corridor (m,n) = (k+1,k)
        for e in (1, 2 * k + 1, 7):
            cases.append((k + 1, k, e))
    for (m, n) in [(3, 1), (4, 1), (4, 3), (5, 2), (6, 1), (7, 4), (8, 5)]:
        for e in (1, 5):
            cases.append((m, n, e))
    rows = [check_case(m, n, e) for (m, n, e) in cases]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        wcsv = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wcsv.writeheader()
        wcsv.writerows(rows)
    bad = [r for r in rows if r["status"] != "OK"]
    print(f"{len(rows) - len(bad)}/{len(rows)} OK; "
          f"counts {rows[0]['hull_vertices']} .. {max(r['hull_vertices'] for r in rows)}")
    for r in bad:
        print("FAIL:", r)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
