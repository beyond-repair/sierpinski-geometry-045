"""Catalog locks. Not a thrust claim. Does not refit constants."""
from gasket_catalog import (
    DS_OVER_2,
    dirichlet_ground,
    format_report,
    harmonic_energy,
    log_periodic,
    mesh_counts,
    two_corner_resistance,
)


def test_mesh_default_counts():
    assert mesh_counts() == (48, 36)


def test_dirichlet_scaled_ground_lock_n5():
    d = dirichlet_ground(5)
    assert abs(d["scaled"] - 11.208655) < 5e-4
    assert d["scaled"] != 0.08


def test_harmonic_energy_renormalizes_to_two():
    e = harmonic_energy(3)
    assert abs((5.0 / 3.0) ** 3 * e - 2.0) < 1e-9


def test_two_corner_resistance_ratio():
    r = two_corner_resistance(2)
    expected = (2.0 / 3.0) * ((5.0 / 3.0) ** 2)
    assert abs(r / expected - 1.0) < 1e-9


def test_log_periodic_preregistered_windows_fail_n5():
    windows = ((0.003, 0.075), (0.004, 0.100), (0.005, 0.125), (0.003, 0.015))
    for t0, t1 in windows:
        row = log_periodic(5, t0, t1)
        assert row["passes"] is False
        assert abs(row["target"] - (-DS_OVER_2)) < 1e-12


def test_quick_report_discloses_dsi_and_not_thrust():
    text = format_report(include_level6=False)
    assert "experimental_validation=false" in text
    assert "log-periodic DSI period established=False" in text
    assert "NOT THRUST" in text
    assert "vertices=48 faces=36" in text
    assert "not a maximum" in text
    assert "generation ratios are not 5/3" in text


def test_level6_ground_and_log_periodic_miss():
    """Headline n=6 lock. Not 0.08. Pre-registered DSI windows fail."""
    d6 = dirichlet_ground(6)
    assert d6["dim"] == 1092
    assert abs(d6["scaled"] - 11.210263758146393) < 1e-5
    assert abs(d6["scaled"] - 0.08) > 1.0
    row = log_periodic(6, 0.003, 0.075)
    assert row["passes"] is False
    assert row["periods"] == 2.0
    assert abs(row["slope"] - (-0.8366667679808816)) < 1e-4
    assert row["rel_miss"] > 0.20
    short = log_periodic(6, 0.003, 0.015)
    assert short["periods"] == 1.0
    assert short["passes"] is False
