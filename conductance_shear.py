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


def weights_gamma(P: np.ndarray, edges: Sequence[Edge], gamma: float) -> np.ndarray:
    """Power weights ell^{-gamma}. gamma=0 is combinatorial (metric-blind)."""
    out = []
    for i, j in edges:
        d = max(float(np.linalg.norm(P[i] - P[j])), 1e-18)
        out.append(d ** (-gamma))
    return np.asarray(out, dtype=float)


def force_gamma(level: int, tilt_deg: float, gamma: float, deform=shear_x) -> np.ndarray:
    P, E, C = build_gasket(level)
    Q = deform(P, tilt_deg)
    wt = weights_gamma(Q, E, gamma)
    L = assemble(len(Q), E, wt)
    u = solve_interior(L, C, np.ones(len(Q)))
    return net_flux(Q, E, u, C, wt)


def shear_y(P: np.ndarray, tilt_deg: float) -> np.ndarray:
    t = math.tan(math.radians(tilt_deg))
    Q = P.copy()
    Q[:, 1] = P[:, 1] + P[:, 0] * t
    return Q


def scale_y(P: np.ndarray, tilt_deg: float) -> np.ndarray:
    """Uniaxial y scale by (1 + theta_rad). Not a fit."""
    a = math.radians(tilt_deg)
    Q = P.copy()
    Q[:, 1] = P[:, 1] * (1.0 + a)
    return Q


def scale_isotropic(P: np.ndarray, tilt_deg: float) -> np.ndarray:
    a = math.radians(tilt_deg)
    cen = P.mean(axis=0)
    return (P - cen) * (1.0 + a) + cen


def corner_currents(P, edges, u, corners, wt) -> np.ndarray:
    wmap = {edges[k]: float(wt[k]) for k in range(len(edges))}
    adj: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(len(P))}
    for (i, j), w in wmap.items():
        adj[i].append((j, w))
        adj[j].append((i, w))
    out = []
    for c in corners:
        current = 0.0
        for j, w in adj[int(c)]:
            current += w * (u[int(c)] - u[j])
        out.append(current)
    return np.asarray(out, dtype=float)


def build_hierarchical(level: int):
    """Finest gasket plus every coarser triangle side. Generation 0 is the outer triangle."""
    if level < 0:
        raise ValueError("level >= 0")
    c0 = np.array([0.0, 0.0])
    c1 = np.array([1.0, 0.0])
    c2 = np.array([0.5, math.sqrt(3.0) / 2.0])
    pos_map: Dict[Tuple[float, float], int] = {}
    positions: List[np.ndarray] = []
    raw: List[Tuple[int, int, int]] = []

    def vid(p: np.ndarray) -> int:
        k = _key(p)
        if k not in pos_map:
            pos_map[k] = len(positions)
            positions.append(np.asarray(p, dtype=float).copy())
        return pos_map[k]

    def rec(a, b, c, d, g):
        ia, ib, ic = vid(a), vid(b), vid(c)
        for i, j in ((ia, ib), (ib, ic), (ic, ia)):
            if i != j:
                raw.append((min(i, j), max(i, j), g))
        if d == 0:
            return
        rec(a, 0.5 * (a + b), 0.5 * (c + a), d - 1, g + 1)
        rec(0.5 * (a + b), b, 0.5 * (b + c), d - 1, g + 1)
        rec(0.5 * (c + a), 0.5 * (b + c), c, d - 1, g + 1)

    rec(c0, c1, c2, level, 0)
    uniq: Dict[Edge, int] = {}
    for i, j, g in raw:
        uniq.setdefault((i, j), g)
    P = np.vstack(positions)
    edges = sorted(uniq)
    gens = np.array([uniq[e] for e in edges], dtype=int)
    corners = np.array([pos_map[_key(c0)], pos_map[_key(c1)], pos_map[_key(c2)]], dtype=int)
    return P, edges, gens, corners


def force_hierarchical(level: int, tilt_deg: float, r: float = 1.0) -> np.ndarray:
    """Conductance weights (r^g)/ell on the hierarchical graph. Not thrust."""
    P, E, gens, C = build_hierarchical(level)
    Q = shear_x(P, tilt_deg)
    wt = []
    for (i, j), g in zip(E, gens):
        d = max(float(np.linalg.norm(Q[i] - Q[j])), 1e-18)
        wt.append((r ** int(g)) / d)
    wt_a = np.asarray(wt, dtype=float)
    L = assemble(len(Q), E, wt_a)
    u = solve_interior(L, C, np.ones(len(Q)))
    return net_flux(Q, E, u, C, wt_a)


def interior_nullity_without_finest(level: int) -> int:
    """Drop generation-n edges. Interior Laplacian is singular (buses are not a sensor)."""
    P, E, gens, C = build_hierarchical(level)
    kept = [E[k] for k in range(len(E)) if int(gens[k]) < level]
    wt = np.ones(len(kept), dtype=float)
    L = assemble(len(P), kept, wt)
    mask = np.ones(len(P), dtype=bool)
    mask[C] = False
    interior = np.where(mask)[0]
    ev = np.linalg.eigvalsh(L[np.ix_(interior, interior)])
    return int(np.sum(np.abs(ev) < 1e-8))


def central_gain(level: int, tilt_deg: float, gamma: float = 1.0, deform=shear_x) -> np.ndarray:
    """Central difference dF / d(theta_rad) at ±tilt_deg. Not a fitted constant."""
    fp = force_gamma(level, tilt_deg, gamma, deform=deform)
    fm = force_gamma(level, -tilt_deg, gamma, deform=deform)
    return (fp - fm) / (2.0 * math.radians(tilt_deg))


EXPECTED_LV2_045 = {
    "cond": 0.00367285,
    "geom": 0.00734563,
}


def run() -> None:
    print("Conductance / shear diagnostic. Not thrust. Not LDOS.")
    print("=== level-2 0.45 deg lock ===")
    for mode in ("combo", "cond", "geom"):
        n = float(np.linalg.norm(force(2, 0.45, mode)))
        print(f"{mode} {n:.8e}")
    print("=== rotation blindness ===")
    print(f"{float(np.linalg.norm(force(2, 0.45, 'cond', deform=rotate))):.8e}")
    print("=== zero tilt ===")
    print(f"{float(np.linalg.norm(force(2, 0.0, 'cond'))):.8e}")
    print("=== cond level scan theta=0.45 deg ===")
    prev = None
    for lv in (2, 3, 4, 5):
        nrm = float(np.linalg.norm(force(lv, 0.45, "cond")))
        ratio = None if prev is None else nrm / prev
        print(f"level {lv} ||F||={nrm:.8e} ratio_to_prev={ratio}")
        prev = nrm
    print("ratios are not 5/3")
    print("=== gamma proportionality level 2 ===")
    for g in (0.5, 1.0, 2.0, 3.0):
        nrm = float(np.linalg.norm(force_gamma(2, 0.45, g)))
        print(f"gamma {g} ||F||={nrm:.8e} ||F||/gamma={nrm/g:.8e}")
    print("=== hierarchical / finest cond, r=1 ===")
    for lv in (2, 3, 4):
        h = float(np.linalg.norm(force_hierarchical(lv, 0.45, 1.0)))
        f = float(np.linalg.norm(force(lv, 0.45, "cond")))
        print(f"level {lv} hier/fine={h/f:.6f}")
    h05 = float(np.linalg.norm(force_hierarchical(4, 0.45, 0.5)))
    h1 = float(np.linalg.norm(force_hierarchical(4, 0.45, 1.0)))
    print(f"level 4 r=0.5/r=1 {h05/h1:.6f}")
    print(f"level 2 nullity without finest edges {interior_nullity_without_finest(2)}")
    print("=== central gain level 2, gamma=1, step 0.01 deg ===")
    for name, fn in (("x-shear", shear_x), ("y-shear", shear_y), ("y-scale", scale_y), ("isotropic", scale_isotropic), ("rotate", rotate)):
        d = central_gain(2, 0.01, 1.0, deform=fn)
        print(f"{name} dF/dtheta_rad=({d[0]:.6e}, {d[1]:.6e})")
    print("NOT THRUST")


if __name__ == "__main__":
    run()
