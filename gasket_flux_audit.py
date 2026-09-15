#!/usr/bin/env python3
"""Graph-level Sierpinski gasket flux audit.

Not a field solver and not a thrust claim.
Checks four statements that can be computed:

1. Vertex counts: level 2 -> 15, level 3 -> 42.
2. Symmetric Dirichlet data on D3-invariant geometry => net flux ~ 0.
3. Asymmetric Dirichlet data => nonzero flux at any alpha; alpha=0.45 is not a peak.
4. Small shear of coordinates + weighted Laplacian + symmetric interior load => flux linear in tilt.
"""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np

Corner = int
Edge = Tuple[int, int]


def _key(p: np.ndarray, nd: int = 10) -> Tuple[float, float]:
    return (round(float(p[0]), nd), round(float(p[1]), nd))


def build_gasket(level: int) -> Tuple[np.ndarray, List[Edge], np.ndarray]:
    """Return positions (N,2), undirected edges, corner indices [3]."""
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

    def add_edge(i: int, j: int) -> None:
        if i == j:
            return
        edges.add((min(i, j), max(i, j)))

    def rec(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: int) -> None:
        if d == 0:
            ia, ib, ic = vid(a), vid(b), vid(c)
            add_edge(ia, ib)
            add_edge(ib, ic)
            add_edge(ic, ia)
            return
        ab = 0.5 * (a + b)
        bc = 0.5 * (b + c)
        ca = 0.5 * (c + a)
        rec(a, ab, ca, d - 1)
        rec(ab, b, bc, d - 1)
        rec(ca, bc, c, d - 1)

    rec(c0, c1, c2, level)
    P = np.vstack(positions)
    corners = np.array([pos_map[_key(c0)], pos_map[_key(c1)], pos_map[_key(c2)]], dtype=int)
    return P, sorted(edges), corners


def laplacian(n: int, edges: List[Edge], positions: np.ndarray | None = None) -> np.ndarray:
    """Combinatorial Laplacian, or 1/length^2 geometric weights if positions given."""
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


def net_flux(
    P: np.ndarray,
    edges: List[Edge],
    u: np.ndarray,
    corners: np.ndarray,
    weighted: bool = False,
) -> np.ndarray:
    """Vector flux = sum over corner currents * corner position (from centroid)."""
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
    """One-sided shear: x' = x + y * tan(tilt). Connectivity unchanged."""
    t = math.tan(math.radians(tilt_deg))
    Q = P.copy()
    Q[:, 0] = P[:, 0] + P[:, 1] * t
    return Q


def run() -> None:
    print("=== vertex counts ===")
    for lv in range(0, 5):
        P, E, C = build_gasket(lv)
        print(f"level {lv}: N={len(P)} E={len(E)} corners={list(C)}")

    P, E, C = build_gasket(2)
    L = laplacian(len(P), E)
    print(f"\nlevel-2 N={len(P)} (expect 15), level-3 check:")
    P3, E3, _ = build_gasket(3)
    print(f"level-3 N={len(P3)} (expect 42)")

    print("\n=== Test 1/2: alpha=0.45 asymmetric vs symmetric source ===")
    A = fractional_laplacian(L, 0.45)
    u_asym = dirichlet_solve(A, C, np.array([1.0, -0.5, 0.0]))
    F_asym = net_flux(P, E, u_asym, C)
    u_sym = dirichlet_solve(A, C, np.array([1.0, 1.0, 1.0]))
    F_sym = net_flux(P, E, u_sym, C)
    print(f"asymmetric F = {F_asym}  ||F||={np.linalg.norm(F_asym):.6e}")
    print(f"symmetric  F = {F_sym}  ||F||={np.linalg.norm(F_sym):.6e}")

    print("\n=== Test 3: ||F|| vs alpha, same asymmetric source ===")
    for a in (0.25, 0.45, 0.6826, 1.0, 1.5, 2.0):
        Aa = fractional_laplacian(L, a)
        ua = dirichlet_solve(Aa, C, np.array([1.0, -0.5, 0.0]))
        Fa = net_flux(P, E, ua, C)
        print(f"alpha={a:7.4f}  ||F||={np.linalg.norm(Fa):.6e}  F={Fa}")

    print("\n=== Geometric tilt + weighted Laplacian ===")
    print("Dirichlet 0 on corners, unit interior load (symmetric excitation).")
    print(f"{'tilt':>8} {'Fx':>12} {'Fy':>12} {'||F||':>12} {'||F||/eps':>12}")
    for tilt in (0.0, 0.1, 0.45, 1.0, 2.0, 5.0):
        Q = shear_positions(P, tilt)
        Lw = laplacian(len(Q), E, Q)
        n = Lw.shape[0]
        mask = np.ones(n, dtype=bool)
        mask[C] = False
        interior = np.where(mask)[0]
        u = np.zeros(n, dtype=float)
        rhs = np.ones(len(interior), dtype=float)
        u[interior] = np.linalg.solve(Lw[np.ix_(interior, interior)], rhs)
        F = net_flux(Q, E, u, C, weighted=True)
        nrm = float(np.linalg.norm(F))
        ratio = nrm / tilt if tilt else float("nan")
        print(f"{tilt:8.2f} {F[0]:12.6f} {F[1]:12.6f} {nrm:12.6f} {ratio:12.4f}")


if __name__ == "__main__":
    run()
