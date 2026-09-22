"""Locks for Sweep-159 conductance / shear diagnostics. Not a thrust claim."""
import math

import numpy as np

from conductance_shear import force, rotate


def test_zero_tilt_machine_zero():
    for mode in ("combo", "cond", "geom"):
        assert np.linalg.norm(force(2, 0.0, mode)) < 1e-12


def test_combo_blind_to_shear():
    assert np.linalg.norm(force(2, 0.45, "combo")) < 1e-12


def test_cond_and_geom_locks():
    n_cond = float(np.linalg.norm(force(2, 0.45, "cond")))
    n_geom = float(np.linalg.norm(force(2, 0.45, "geom")))
    assert abs(n_cond - 0.00367285) < 5e-6
    assert abs(n_geom - 0.00734563) < 5e-6
    assert abs(n_geom / n_cond - 2.0) < 0.01


def test_cond_linear_small_angle():
    a = float(np.linalg.norm(force(2, 0.45, "cond")))
    b = float(np.linalg.norm(force(2, 1.0, "cond")))
    assert abs((b / a) - (1.0 / 0.45)) < 0.01


def test_rotation_blind():
    assert np.linalg.norm(force(2, 0.45, "cond", deform=rotate)) < 1e-12


def test_odd_even_x_shear():
    fp = force(2, 0.45, "cond")
    fm = force(2, -0.45, "cond")
    odd = 0.5 * (fp - fm)
    even = 0.5 * (fp + fm)
    assert abs(odd[0] + 0.00367284) < 5e-6
    assert abs(odd[1]) < 1e-12
    assert abs(even[0]) < 1e-12
    assert abs(even[1]) < 2e-5


def test_jacobian_matches_c():
    fp = force(2, 0.45, "cond")
    fm = force(2, -0.45, "cond")
    dFx = (fp[0] - fm[0]) / (2.0 * math.radians(0.45))
    assert abs(dFx + 0.46764) < 5e-4
