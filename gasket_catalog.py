#!/usr/bin/env python3
"""Runnable catalog for sierpinski-geometry-045.

Prints the numbers this repository actually computes: mesh counts, graph
flux, conductance/shear, combinatorial spectrum, Kigami energy and
resistance, heat trace, and the pre-registered log-periodic test.

Not a field solver. Not thrust. Not a Ware constant. Constants are not refit.
"""
from __future__ import annotations

import argparse
import math
from functools import lru_cache

import numpy as np

from conductance_shear import (
    central_gain,
    force,
    force_gamma,
    force_hierarchical,
    interior_nullity_without_finest,
    rotate,
    scale_isotropic,
    scale_y,
    shear_x,
    shear_y,
)
from gasket_flux_audit import alpha_sweep, symmetric_flux, tilt_norm
from gasket_graph import build_gasket, combinatorial_laplacian
from sierpinski_generator import generate_asymmetric_sierpinski

DS = 2.0 * math.log(3.0) / math.log(5.0)
DS_OVER_2 = 0.5 * DS
LOG5 = math.log(5.0)


@lru_cache(maxsize=8)
def _eigen(level: int):
    if level < 0:
        raise ValueError("level >= 0")
    P, E, C = build_gasket(level)
    L = combinatorial_laplacian(len(P), E)
    free = np.linalg.eigvalsh(L)
    mask = np.ones(len(P), dtype=bool)
    mask[C] = False
    interior = np.where(mask)[0]
    if len(interior) == 0:
        diri = np.array([], dtype=float)
    else:
        diri = np.linalg.eigvalsh(L[np.ix_(interior, interior)])
    return L, C, free, diri


def mesh_counts(alpha: float = 0.45, n_aft: int = 3, n_fore: int = 1) -> tuple[int, int]:
    V, F = generate_asymmetric_sierpinski(alpha=alpha, n_aft=n_aft, n_fore=n_fore)
    return int(len(V)), int(len(F))


def free_spectrum(level: int) -> dict:
    _L, _C, free, _d = _eigen(level)
    w = free
    def mult(target: float) -> int:
        return int(np.sum(np.abs(w - target) < 1e-6))
    return {
        "N": int(w.shape[0]),
        "lambda_max": float(w.max()),
        "mult3": mult(3.0),
        "mult5": mult(5.0),
        "mult6": mult(6.0),
    }


def dirichlet_ground(level: int) -> dict:
    _L, _C, _f, diri = _eigen(level)
    if diri.size == 0:
        raise ValueError("no Dirichlet interior at this level")
    lmin = float(diri.min())
    return {
        "dim": int(diri.size),
        "lambda_min": lmin,
        "lambda_max": float(diri.max()),
        "scaled": (5.0 ** level) * lmin,
    }


def harmonic_energy(level: int) -> float:
    """Sum of (u_i-u_j)^2 over edges. Equals u^T L u, not half of it.

    Boundary data (1,0,0). Returns 2*(3/5)^n on this combinatorial gasket.
    """
    P, E, C = build_gasket(level)
    L = combinatorial_laplacian(len(P), E)
    u = np.zeros(len(P), dtype=float)
    u[C] = (1.0, 0.0, 0.0)
    mask = np.ones(len(P), dtype=bool)
    mask[C] = False
    interior = np.where(mask)[0]
    if len(interior):
        rhs = -L[np.ix_(interior, C)] @ u[C]
        u[interior] = np.linalg.solve(L[np.ix_(interior, interior)], rhs)
    energy = 0.0
    for i, j in E:
        d = u[i] - u[j]
        energy += float(d * d)
    return energy


def two_corner_resistance(level: int) -> float:
    """Effective resistance between two corners; the third corner floats."""
    P, E, C = build_gasket(level)
    L = combinatorial_laplacian(len(P), E)
    fixed = np.array([int(C[0]), int(C[1])])
    u = np.zeros(len(P), dtype=float)
    u[fixed] = (1.0, 0.0)
    mask = np.ones(len(P), dtype=bool)
    mask[fixed] = False
    free = np.where(mask)[0]
    rhs = -L[np.ix_(free, fixed)] @ u[fixed]
    u[free] = np.linalg.solve(L[np.ix_(free, free)], rhs)
    c0 = int(C[0])
    current = 0.0
    for i, j in E:
        if i == c0 or j == c0:
            other = j if i == c0 else i
            current += u[c0] - u[other]
    return float((u[c0] - u[int(C[1])]) / current)


def heat_trace(level: int, tau: float) -> float:
    """Killed Kigami trace Z(tau) = sum exp(-tau * 5^n * lambda_k^D)."""
    _L, _C, _f, diri = _eigen(level)
    if diri.size == 0:
        raise ValueError("no Dirichlet spectrum")
    scaled = (5.0 ** level) * diri
    return float(np.exp(-tau * scaled).sum())


def log_periodic(level: int, t0: float, t1: float, npts: int = 48) -> dict:
    """Least-squares slope of log Z vs log tau, and amplitude A = Z * tau^{d_s/2}.

    Pre-registered pass would need the slope within a few percent of -d_s/2
    and at least two periods of log 5. This function does not fit 0.08.
    """
    _L, _C, _f, diri = _eigen(level)
    scaled = (5.0 ** level) * diri
    taus = np.geomspace(t0, t1, npts)
    Z = np.exp(-taus[:, None] * scaled[None, :]).sum(axis=1)
    x = np.log(taus)
    y = np.log(Z)
    design = np.vstack([x, np.ones_like(x)]).T
    slope, _intercept = np.linalg.lstsq(design, y, rcond=None)[0]
    amp = Z * np.exp(x * DS_OVER_2)
    periods = math.log(t1 / t0) / LOG5
    rel = abs(float(slope) - (-DS_OVER_2)) / DS_OVER_2
    return {
        "slope": float(slope),
        "target": -DS_OVER_2,
        "rel_miss": float(rel),
        "periods": float(periods),
        "amp_rel_std": float(amp.std() / amp.mean()),
        "amp_start": float(amp[0]),
        "amp_end": float(amp[-1]),
        "passes": bool(rel < 0.05 and periods >= 2.0 - 1e-9),
    }


def poisson_renormalized(level: int) -> tuple[float, float]:
    """(5/3)^n L with load 3^{-n} on each interior vertex. Returns max|u|, u^T L u."""
    P, E, C = build_gasket(level)
    L = combinatorial_laplacian(len(P), E) * ((5.0 / 3.0) ** level)
    mask = np.ones(len(P), dtype=bool)
    mask[C] = False
    interior = np.where(mask)[0]
    b = np.zeros(len(P), dtype=float)
    b[interior] = 3.0 ** (-level)
    u = np.zeros(len(P), dtype=float)
    u[interior] = np.linalg.solve(L[np.ix_(interior, interior)], b[interior])
    energy = float(u @ L @ u)
    return float(np.max(np.abs(u))), energy


def format_report(include_level6: bool = True) -> str:
    lines: list[str] = []
    w = lines.append
    w("sierpinski-geometry-045 catalog")
    w("claim_level=1  thrust=false  energy_extraction=false  experimental_validation=false")
    w("design alpha=0.45 is a mesh scale factor, not a spectral threshold and not 0.08")
    w(f"d_s={DS:.6f}  d_s/2={DS_OVER_2:.6f}  (d_s/2 < 1/2 is false)")
    nv, nf = mesh_counts()
    w(f"mesh default n_aft=3 n_fore=1 alpha=0.45: vertices={nv} faces={nf}")
    w("--- flux level 2, combinatorial L^alpha, not momentum ---")
    w(f"symmetric Dirichlet ||F||(0.45)={symmetric_flux():.6e}")
    sweep = alpha_sweep()
    for a, nrm in sweep.items():
        note = ""
        if abs(a - 0.45) < 1e-12:
            note = "  not a maximum"
        w(f"asymmetric alpha={a:.4f} ||F||={nrm:.6f}{note}")
    w("--- geometric-weight tilt, level 2, not thrust ---")
    for th in (0.0, 0.45, 1.0):
        nrm = tilt_norm(2, th)
        w(f"theta={th:.2f} deg ||F||={nrm:.6e}")
    w("--- conductance gamma=1, theta=0.45 deg ---")
    prev = None
    norms = {}
    for lv in (2, 3, 4, 5):
        nrm = float(np.linalg.norm(force(lv, 0.45, "cond")))
        norms[lv] = nrm
        ratio = "" if prev is None else f"  ratio={nrm/prev:.6f}"
        w(f"level {lv} ||F||={nrm:.8e}{ratio}")
        prev = nrm
    w("generation ratios are not 5/3")
    k4 = norms[4]
    w("K_4 angle meter Theta_diag/theta = ||F||_n/||F||_4 (not invariant):")
    for lv in (2, 3, 4, 5):
        w(f"  n={lv} {norms[lv]/k4:.6f}")
    w("--- gamma at level 2, theta=0.45 deg ---")
    for g in (0.5, 1.0, 2.0, 3.0):
        nrm = float(np.linalg.norm(force_gamma(2, 0.45, g)))
        w(f"gamma={g:.1f} ||F||={nrm:.8e} ||F||/gamma={nrm/g:.8e}")
    w("--- hierarchical buses / finest, r=1, theta=0.45 deg ---")
    for lv in (2, 3, 4):
        h = float(np.linalg.norm(force_hierarchical(lv, 0.45, 1.0)))
        f = float(np.linalg.norm(force(lv, 0.45, "cond")))
        w(f"level {lv} hier/fine={h/f:.6f}")
    h05 = float(np.linalg.norm(force_hierarchical(4, 0.45, 0.5)))
    h1 = float(np.linalg.norm(force_hierarchical(4, 0.45, 1.0)))
    w(f"level 4 ||F||(r=0.5)/||F||(r=1)={h05/h1:.6f}")
    w(f"nullity of interior Laplacian without finest edges, level 2: {interior_nullity_without_finest(2)}")
    w("--- central dF/dtheta_rad, level 2, gamma=1, step 0.01 deg ---")
    for name, fn in (
        ("x-shear", shear_x),
        ("y-shear", shear_y),
        ("y-scale", scale_y),
        ("isotropic", scale_isotropic),
        ("rotate", rotate),
    ):
        d = central_gain(2, 0.01, 1.0, deform=fn)
        w(f"{name} ({d[0]:.6e}, {d[1]:.6e})")
    w("--- combinatorial spectrum (lambda_max=6 only for n>=2; n=1 misses 6) ---")
    for n in range(0, 6):
        fre = free_spectrum(n)
        w(
            f"n={n} N={fre['N']} lambda_max={fre['lambda_max']:.6f} "
            f"mult6={fre['mult6']} mult5={fre['mult5']} mult3={fre['mult3']}"
        )
    w("--- Dirichlet 5^n lambda_min (not 0.08) ---")
    prev = None
    # Level 6 is optional: one dense eigen-solve, about 10 seconds.
    for n in range(1, 6):
        d = dirichlet_ground(n)
        ratio = "" if prev is None else f"  ratio={d['lambda_min']/prev:.6f}"
        w(
            f"n={n} dim={d['dim']} lambda_min={d['lambda_min']:.6e} "
            f"5^n*lambda_min={d['scaled']:.6f}{ratio}"
        )
        prev = d["lambda_min"]
    if include_level6:
        d6 = dirichlet_ground(6)
        ratio = d6["lambda_min"] / prev
        w(
            f"n=6 dim={d6['dim']} lambda_min={d6['lambda_min']:.6e} "
            f"5^n*lambda_min={d6['scaled']:.6f}  ratio={ratio:.6f}"
        )
        w(f"n=6 scaled ground {d6['scaled']:.6f} is not 0.08 and lambda_max(D)={d6['lambda_max']:.6f} is not a force")
    w("--- harmonic energy boundary (1,0,0); sum_edges (du)^2 = u^T L u ---")
    for n in range(0, 6):
        e = harmonic_energy(n)
        ren = (5.0 / 3.0) ** n * e
        half = (5.0 / 3.0) ** n * (0.5 * e)
        w(f"n={n} E={e:.8f} (5/3)^n*E={ren:.8f} (5/3)^n*(E/2)={half:.8f}")
    w("(5/3)^n * edge-sum is 2, not 1. Half-energy reading of that formula is 1.")
    w("--- two-corner resistance, third corner floating ---")
    for n in range(0, 6):
        r = two_corner_resistance(n)
        w(f"n={n} R={r:.8f} R/((2/3)*(5/3)^n)={r/((2.0/3.0)*(5.0/3.0)**n):.8f}")
    w("--- renormalized Poisson, load 3^{-n}; limit of energy is not claimed ---")
    for n in range(1, 6):
        umax, en = poisson_renormalized(n)
        w(f"n={n} max|u|={umax:.8f} u^T L_ren u={en:.8f}")
    w("--- Kigami heat trace Z(tau) ---")
    for n in range(2, 6):
        zs = [heat_trace(n, tau) for tau in (0.01, 0.03, 0.10)]
        w(f"n={n} Z(0.01,0.03,0.10)={zs[0]:.6f} {zs[1]:.6f} {zs[2]:.6f}")
    w("--- pre-registered log-periodic test (not a fit to 0.08) ---")
    windows = ((0.003, 0.075), (0.004, 0.100), (0.005, 0.125), (0.003, 0.015))
    levels = (5, 6) if include_level6 else (5,)
    any_pass = False
    for n in levels:
        for t0, t1 in windows:
            row = log_periodic(n, t0, t1)
            any_pass = any_pass or row["passes"]
            w(
                f"n={n} [{t0:.3f},{t1:.3f}] periods={row['periods']:.3f} "
                f"slope={row['slope']:.6f} target={row['target']:.6f} "
                f"rel_miss={row['rel_miss']:.3f} "
                f"A={row['amp_start']:.6f}->{row['amp_end']:.6f} "
                f"pass={row['passes']}"
            )
    w(f"log-periodic DSI period established={any_pass}")
    w("NOT THRUST. NOT A COMPLETED PHYSICAL LAW.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print gasket geometry and graph locks. Not thrust.")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="skip level-6 Dirichlet and log-periodic (saves about 10 seconds)",
    )
    args = parser.parse_args()
    print(format_report(include_level6=not args.quick), end="")


if __name__ == "__main__":
    main()
