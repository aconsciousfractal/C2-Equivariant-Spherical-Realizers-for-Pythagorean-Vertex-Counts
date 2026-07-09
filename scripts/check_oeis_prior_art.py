"""OEIS evidence check for the identities and sequence facts cited in the paper.

Verifies, against the archived OEIS JSON pulls in ../sources/oeis/ and the
regenerated baselines in ../results/baseline_k1_20.csv:
  1. All identities cited in the paper, Section 5 (sympy, exact).
  2. A139267(k+1) == corridor hull count for k = 1..20.
  3. A033567(k+1) == corridor a+2b+2c for k = 1..20 (offset trap: a(0..1)=1,3).
  4. The Bergot 2013 comment is present verbatim in the archived A000567 entry.
Run from this directory: python check_oeis_prior_art.py
"""
import csv
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "sources", "oeis")
RES = os.path.join(HERE, "..", "results")

failures = []


def check(label, ok):
    print(("PASS" if ok else "FAIL"), "-", label)
    if not ok:
        failures.append(label)


def entry(aname):
    with open(os.path.join(SRC, aname + ".json"), encoding="utf-8") as f:
        d = json.load(f)
    if isinstance(d, dict):
        d = d.get("results") or []
    return d[0]


# 1. Identities (exact, sympy)
m, n, k = sp.symbols("m n k", positive=True)
A, B, C = m**2 - n**2, 2 * m * n, m**2 + n**2
check("a+2b+c == 2m(m+2n)", sp.simplify(A + 2 * B + C - 2 * m * (m + 2 * n)) == 0)
check("a+2b+2c == (m+n)(3m+n)", sp.simplify(A + 2 * B + 2 * C - (m + n) * (3 * m + n)) == 0)
check("perimeter == 2m(m+n)", sp.simplify(A + B + C - 2 * m * (m + n)) == 0)
corr = [(m, k + 1), (n, k)]
check("corridor a+2b+c == 2(k+1)(3k+1)",
      sp.simplify((A + 2 * B + C).subs(corr) - 2 * (k + 1) * (3 * k + 1)) == 0)
check("corridor a+2b+2c == (2k+1)(4k+3)",
      sp.simplify((A + 2 * B + 2 * C).subs(corr) - (2 * k + 1) * (4 * k + 3)) == 0)
# NB: substitute into fresh symbol k (simultaneous), not (m,n)->(n,n-1),
# which sympy applies sequentially and corrupts.
check("Bergot: B+(A+C)/2 == k(3k-2) under Euclid (k,k-1)",
      sp.simplify((B + (A + C) / 2).subs([(m, k), (n, k - 1)]) - k * (3 * k - 2)) == 0)

# 2./3. Sequence diffs against the baselines
a139267 = [int(x) for x in entry("A139267")["data"].split(",")]
a033567 = [int(x) for x in entry("A033567")["data"].split(",")]
with open(os.path.join(RES, "baseline_k1_20.csv"), encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
ok1 = ok2 = True
for r in rows:
    kk = int(r["k"])
    a, b, c = int(r["a"]), int(r["b"]), int(r["c"])
    if a139267[kk + 1] != int(r["hull_vertices"]):
        ok1 = False
    if a033567[kk + 1] != a + 2 * b + 2 * c:
        ok2 = False
check("A139267(k+1) == hull count, k=1..20 (20/20)", ok1 and len(rows) == 20)
check("A033567(k+1) == a+2b+2c, k=1..20 (20/20)", ok2)
check("A033567 offset trap: a(0),a(1) == 1,3 (not corridor values)",
      a033567[0] == 1 and a033567[1] == 3)

# 4. Bergot comment verbatim in archived A000567
bergot = ("Generate a Pythagorean triple using Euclid's formula with (n, n-1) "
          "to give A,B,C. a(n) = B + (A + C)/2.")
check("A000567 contains the Bergot 2013 comment",
      any(bergot in c for c in entry("A000567").get("comment", [])))
check("A139267 name is 'Twice octagonal numbers: 2*n*(3*n-2).'",
      entry("A139267")["name"] == "Twice octagonal numbers: 2*n*(3*n-2).")

print()
print("RESULT:", "ALL PASS" if not failures else f"{len(failures)} FAILURE(S)")
sys.exit(1 if failures else 0)
