#!/usr/bin/env python3
"""Conductance / hierarchical / shear diagnostics. Not a field solver. Not thrust."""
from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

import numpy as np

Edge = Tuple[int, int]


def _key(p: np.ndarray, nd: int = 10) -> Tuple[float, float]:
    return (round(float(p[0]), nd), round(float(p[1]), nd))


def build_gasket(level: int):
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


def shear_x(P: np.ndarray, tilt_deg: float) -> np.ndarray:
    t = math.tan(math.radians(tilt_deg))
    Q = P.copy()
    Q[:, 0] = P[:, 0] + P[:, 1] * t
    return Q


def rotate(P: np.ndarray, tilt_deg: float) -> np.ndarray:
    a = math.radians(tilt_deg)
    c, s = math.cos(a), math.sin(a)
    R = np.array([[c, -s], [s, c]])
    cen = P.mean(axis=0)
    return (P - cen) @ R.T + cen


def weights_for(P: np.ndarray, edges: Sequence[Edge], mode: str) -> np.ndarray:
    out = []
    for i, j in edges:
        d = max(float(np.linalg.norm(P[i] - P[j])), 1e-18)
        if mode == "combo":
            out.append(1.0)
        elif mode == "cond":
            out.append(1.0 / d)
        elif mode == "geom":
            out.append(1.0 / (d * d))
        else:
            raise ValueError(mode)
    return np.asarray(out, dtype=float)


def assemble(n: int, edges: Sequence[Edge], wt: np.ndarray) -> np.ndarray:
    L = np.zeros((n, n), dtype=float)
    for (i, j), w in zip(edges, wt):
        L[i, i] += w
        L[j, j] += w
        L[i, j] -= w
        L[j, i] -= w
    return L


def solve_interior(L: np.ndarray, corners: np.ndarray, b: np.ndarray) -> np.ndarray:
    mask = np.ones(L.shape[0], dtype=bool)
    mask[corners] = False
    interior = np.where(mask)[0]
    u = np.zeros(L.shape[0], dtype=float)
    u[interior] = np.linalg.solve(L[np.ix_(interior, interior)], b[interior])
    return u


def net_flux(P, edges, u, corners, wt) -> np.ndarray:
    wmap = {edges[k]: float(wt[k]) for k in range(len(edges))}
    adj: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(len(P))}
    for (i, j), w in wmap.items():
        adj[i].append((j, w))
        adj[j].append((i, w))
    centroid = P.mean(axis=0)
    F = np.zeros(2, dtype=float)
    for c in corners:
        current = 0.0
        for j, w in adj[int(c)]:
            current += w * (u[int(c)] - u[j])
        F += current * (P[int(c)] - centroid)
    return F


def force(level: int, tilt_deg: float, mode: str = "cond", deform=shear_x) -> np.ndarray:
    P, E, C = build_gasket(level)
    Q = deform(P, tilt_deg)
    wt = weights_for(Q, E, mode)
    L = assemble(len(Q), E, wt)
    u = solve_interior(L, C, np.ones(len(Q)))
    return net_flux(Q, E, u, C, wt)


EXPECTED_LV2_045 = {
    "cond": 0.00367285,
    "geom": 0.00734563,
}


def run() -> None:
    print("=== level-2 0.45 deg lock ===")
    for mode in ("combo", "cond", "geom"):
        n = float(np.linalg.norm(force(2, 0.45, mode)))
        print(mode, n)
    print("=== rotation blindness ===")
    print(float(np.linalg.norm(force(2, 0.45, "cond", deform=rotate))))
    print("=== zero tilt ===")
    print(float(np.linalg.norm(force(2, 0.0, "cond"))))


if __name__ == "__main__":
    run()
