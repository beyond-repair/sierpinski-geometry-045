#!/usr/bin/env python3
"""Graph-level Sierpinski gasket flux audit. Not a field solver and not a thrust claim."""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np

Corner = int
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


def laplacian(n: int, edges: List[Edge], positions: np.ndarray | None = None) -> np.ndarray:
    L = np.zeros((n, n), dtype=float)
    for i, j in edges:
        if positions is None:
            w = 1.0
        else:
            d = float(np.linalg.norm(positions[i] - positions[j]))
            w = 1.0 / max(d * d, 1e-18)
        L[i, i] += w
        L[j, j] += w
        L[i, j] -= w
        L[j, i] -= w
    return L


def fractional_laplacian(L: np.ndarray, alpha: float) -> np.ndarray:
    w, V = np.linalg.eigh(L)
    w = np.clip(w, 0.0, None)
    return (V * (w ** alpha)) @ V.T


def dirichlet_solve(A: np.ndarray, corners: np.ndarray, u_c: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    mask = np.ones(n, dtype=bool)
    mask[corners] = False
    interior = np.where(mask)[0]
    u = np.zeros(n, dtype=float)
    u[corners] = u_c
    rhs = -A[np.ix_(interior, corners)] @ u_c
    u[interior] = np.linalg.solve(A[np.ix_(interior, interior)], rhs)
    return u


def net_flux(P, edges, u, corners, weighted: bool = False) -> np.ndarray:
    adj: Dict[int, List[int]] = {i: [] for i in range(len(P))}
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    centroid = P.mean(axis=0)
    F = np.zeros(2, dtype=float)
    for c in corners:
        current = 0.0
        for j in adj[int(c)]:
            w = 1.0
            if weighted:
                d = float(np.linalg.norm(P[int(c)] - P[j]))
                w = 1.0 / max(d * d, 1e-18)
            current += w * (u[int(c)] - u[j])
        F += current * (P[int(c)] - centroid)
    return F


def shear_positions(P: np.ndarray, tilt_deg: float) -> np.ndarray:
    t = math.tan(math.radians(tilt_deg))
    Q = P.copy()
    Q[:, 0] = P[:, 0] + P[:, 1] * t
    return Q


def force_from_tilt(level: int, tilt_deg: float) -> np.ndarray:
    P, E, C = build_gasket(level)
    Q = shear_positions(P, tilt_deg)
    Lw = laplacian(len(Q), E, Q)
    n = Lw.shape[0]
    mask = np.ones(n, dtype=bool)
    mask[C] = False
    interior = np.where(mask)[0]
    u = np.zeros(n, dtype=float)
    u[interior] = np.linalg.solve(Lw[np.ix_(interior, interior)], np.ones(len(interior)))
    return net_flux(Q, E, u, C, weighted=True)


def odd_even_force(level: int, tilt_deg: float):
    fp = force_from_tilt(level, tilt_deg)
    fm = force_from_tilt(level, -tilt_deg)
    return 0.5 * (fp - fm), 0.5 * (fp + fm)


def alpha_sweep(level: int = 2, bc=None, alphas=None) -> dict:
    """||F|| of combinatorial L^alpha under fixed Dirichlet data. Not momentum."""
    if bc is None:
        bc = np.array([1.0, -0.5, 0.0])
    if alphas is None:
        alphas = (0.25, 0.45, 0.6826, 1.0, 2.0)
    P, E, C = build_gasket(level)
    L = laplacian(len(P), E)
    out = {}
    for a in alphas:
        A = fractional_laplacian(L, a)
        u = dirichlet_solve(A, C, bc)
        out[float(a)] = float(np.linalg.norm(net_flux(P, E, u, C)))
    return out


def symmetric_flux(level: int = 2, alpha: float = 0.45) -> float:
    P, E, C = build_gasket(level)
    L = laplacian(len(P), E)
    A = fractional_laplacian(L, alpha)
    u = dirichlet_solve(A, C, np.array([1.0, 1.0, 1.0]))
    return float(np.linalg.norm(net_flux(P, E, u, C)))


def tilt_norm(level: int, tilt_deg: float) -> float:
    return float(np.linalg.norm(force_from_tilt(level, tilt_deg)))


def run() -> None:
    print("Graph flux audit. Not a field solver. Not thrust.")
    print("=== vertex counts ===")
    for lv in range(0, 5):
        P, E, C = build_gasket(lv)
        print(f"level {lv}: N={len(P)} E={len(E)} corners={list(map(int, C))}")
    sym = symmetric_flux()
    print(f"=== symmetric Dirichlet ||F|| at alpha=0.45 level 2: {sym:.6e} ===")
    print("=== asymmetric Dirichlet ||F|| vs alpha, level 2, bc=(1,-0.5,0) ===")
    sweep = alpha_sweep()
    for a, nrm in sweep.items():
        mark = "  <-- not a maximum" if abs(a - 0.45) < 1e-12 else ""
        print(f"alpha {a:.4f} ||F||={nrm:.6f}{mark}")
    print("=== geometric-weight tilt ||F||, level 2 ===")
    for th in (0.0, 0.10, 0.45, 1.0, 2.0, 5.0):
        nrm = tilt_norm(2, th)
        gain = nrm / math.radians(th) if th else float("nan")
        print(f"theta {th:.2f} deg ||F||={nrm:.6e} ||F||/theta_rad={gain:.6f}")
    print("0.45 deg is one point on a line through the origin, not a threshold.")
    print("NOT THRUST")


if __name__ == "__main__":
    run()
