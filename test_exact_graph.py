"""Exact recursive gasket validation. Convention lock, not a force claim."""
from gasket_graph import EXPECTED, graph_invariants
from gasket_flux_audit import odd_even_force


def test_exact_invariants_s2_s4():
    for level, exp in EXPECTED.items():
        got = graph_invariants(level)
        assert got["N"] == exp["N"]
        assert got["E"] == exp["E"]
        assert got["Delta"] == exp["Delta"]
        assert abs(got["lambda_max"] - exp["lambda_max"]) < 1e-8
        assert abs(got["TrL"] - exp["TrL"]) < 1e-8
        assert abs(got["TrL2"] - exp["TrL2"]) < 1e-6
        assert abs(got["TrL3"] - exp["TrL3"]) < 1e-6
        assert got["n_zero"] == 1


def test_pm_tilt_odd_linear_even_x_vanishes():
    th = 0.45
    odd, even = odd_even_force(2, th)
    odd1, even1 = odd_even_force(2, 1.0)
    assert abs(even[0]) < 1e-12
    ratio = abs(odd1[0] / odd[0])
    assert abs(ratio - (1.0 / 0.45)) < 0.05
    assert abs(even1[1]) > abs(even[1])
