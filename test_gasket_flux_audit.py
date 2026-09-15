"""Graph-level flux audit locks. Not a thrust claim."""
import math

import numpy as np

from gasket_flux_audit import (
    build_gasket,
    dirichlet_solve,
    fractional_laplacian,
    laplacian,
    net_flux,
    shear_positions,
)


def test_vertex_counts():
    expected = {0: 3, 1: 6, 2: 15, 3: 42, 4: 123}
    for level, n in expected.items():
        P, E, C = build_gasket(level)
        assert len(P) == n
        assert len(C) == 3
        assert len(E) > 0


def test_symmetric_dirichlet_machine_zero_flux():
    P, E, C = build_gasket(2)
    L = laplacian(len(P), E)
    A = fractional_laplacian(L, 0.45)
    u = dirichlet_solve(A, C, np.array([1.0, 1.0, 1.0]))
    F = net_flux(P, E, u, C)
    assert np.linalg.norm(F) < 1e-12


def test_asymmetric_dirichlet_nonzero_and_alpha_not_peak():
    P, E, C = build_gasket(2)
    L = laplacian(len(P), E)
    bc = np.array([1.0, -0.5, 0.0])
    norms = {}
    for a in (0.25, 0.45, 1.0, 2.0):
        A = fractional_laplacian(L, a)
        u = dirichlet_solve(A, C, bc)
        norms[a] = float(np.linalg.norm(net_flux(P, E, u, C)))
    assert norms[0.45] > 0.5
    assert math.isfinite(norms[0.45])
    assert abs(norms[0.45] - 1.165909) < 5e-3
    # On this combinatorial operator, ||F|| is not maximized at 0.45.
    assert norms[0.45] < norms[0.25]


def test_ds_over_two_is_not_below_half():
    ds = 2.0 * math.log(3.0) / math.log(5.0)
    assert ds / 2.0 > 0.5


def test_tilt_zero_and_linear():
    P, E, C = build_gasket(2)
    norms = {}
    for tilt in (0.0, 0.45, 1.0):
        Q = shear_positions(P, tilt)
        Lw = laplacian(len(Q), E, Q)
        n = Lw.shape[0]
        mask = np.ones(n, dtype=bool)
        mask[C] = False
        interior = np.where(mask)[0]
        u = np.zeros(n)
        u[interior] = np.linalg.solve(Lw[np.ix_(interior, interior)], np.ones(len(interior)))
        norms[tilt] = float(np.linalg.norm(net_flux(Q, E, u, C, weighted=True)))
    assert norms[0.0] < 1e-12
    assert abs(norms[0.45] - 0.007346) < 5e-4
    # Linearity: ratio of 1.0 deg to 0.45 deg ~ 1/0.45
    assert abs((norms[1.0] / norms[0.45]) - (1.0 / 0.45)) < 0.05
