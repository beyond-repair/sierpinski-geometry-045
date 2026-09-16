"""Exact recursive Sierpinski gasket graph (combinatorial).

Not the 3-D tetrahedron mesh and not a propulsion model.
N(0)=3, N(1)=6, N(2)=15, N(3)=42, N(4)=123; E(n)=3**(n+1).
"""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np

Edge = Tuple[int, int]


def _key(p: np.ndarray, nd: int = 10) -> Tuple[float, float]:
    return (round(float(p[0]), nd), round(float(p[1]), nd))


def build_gasket(level: int) -> Tuple[np.ndarray, List[Edge], np.ndarray]:
    if level < 0:
        raise ValueError("level >= 0")
    c0 = np.array([0.0, 0.0])
    c1 = np.array([1.0, 0.0])
    c2 = np.array([0.5, math.sqrt(3.0) / 2.0])
    pos_map: Dict[Tuple[float, float], int] = {}
    positions: List[np.ndarray] = []
    edges: set[Edge] = set()

    def vid(p: np.ndarray) -> int:
        k = _key(p)
        if k not in pos_map:
            pos_map[k] = len(positions)
            positions.append(p.copy())
        return pos_map[k]

    def rec(a, b, c, d):
        if d == 0:
            ia, ib, ic = vid(a), vid(b), vid(c)
            for i, j in ((ia, ib), (ib, ic), (ic, ia)):
                if i != j:
                    edges.add((min(i, j), max(i, j)))
            return
        rec(a, 0.5 * (a + b), 0.5 * (c + a), d - 1)
        rec(0.5 * (a + b), b, 0.5 * (b + c), d - 1)
        rec(0.5 * (c + a), 0.5 * (b + c), c, d - 1)

    rec(c0, c1, c2, level)
    P = np.vstack(positions)
    corners = np.array([pos_map[_key(c0)], pos_map[_key(c1)], pos_map[_key(c2)]], dtype=int)
    return P, sorted(edges), corners


def combinatorial_laplacian(n: int, edges: List[Edge]) -> np.ndarray:
    L = np.zeros((n, n), dtype=float)
    for i, j in edges:
        L[i, i] += 1.0
        L[j, j] += 1.0
        L[i, j] -= 1.0
        L[j, i] -= 1.0
    return L


def graph_invariants(level: int) -> dict:
    P, E, C = build_gasket(level)
    L = combinatorial_laplacian(len(P), E)
    deg = np.diag(L)
    w = np.linalg.eigvalsh(L)
    L2 = L @ L
    L3 = L2 @ L
    return {
        "level": level,
        "N": int(len(P)),
        "E": int(len(E)),
        "Delta": float(deg.max()),
        "lambda_max": float(w.max()),
        "TrL": float(np.trace(L)),
        "TrL2": float(np.trace(L2)),
        "TrL3": float(np.trace(L3)),
        "n_zero": int(np.sum(np.abs(w) < 1e-10)),
    }


EXPECTED = {
    2: dict(N=15, E=27, Delta=4.0, lambda_max=6.0, TrL=54.0, TrL2=258.0, TrL3=1332.0),
    3: dict(N=42, E=81, Delta=4.0, lambda_max=6.0, TrL=162.0, TrL2=798.0, TrL3=4212.0),
    4: dict(N=123, E=243, Delta=4.0, lambda_max=6.0, TrL=486.0, TrL2=2418.0, TrL3=12852.0),
}
