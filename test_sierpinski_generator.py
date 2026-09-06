"""Unit tests for geometry-only generator. No physics claims."""
import numpy as np
import pytest

from sierpinski_generator import (
    generate_asymmetric_sierpinski,
    write_ascii_stl,
    surface_sample_points,
    _BASE_VERTICES,
)


def test_base_tetrahedron_unit_edge():
    d = np.linalg.norm(_BASE_VERTICES[0] - _BASE_VERTICES[1])
    assert abs(d - 1.0) < 1e-12


def test_default_mesh_nonempty():
    V, F = generate_asymmetric_sierpinski()
    assert V.shape[1] == 3
    assert F.shape[1] == 3
    assert len(V) > 4
    assert len(F) > 4
    assert F.max() < len(V)
    assert F.min() >= 0


def test_alpha_bounds():
    with pytest.raises(ValueError):
        generate_asymmetric_sierpinski(alpha=0.0)
    with pytest.raises(ValueError):
        generate_asymmetric_sierpinski(alpha=1.0)
    with pytest.raises(ValueError):
        generate_asymmetric_sierpinski(n_aft=-1)


def test_deeper_aft_more_faces_than_symmetric_shallow():
    V1, F1 = generate_asymmetric_sierpinski(n_aft=1, n_fore=1)
    V3, F3 = generate_asymmetric_sierpinski(n_aft=3, n_fore=1)
    assert len(F3) > len(F1)
    assert len(V3) > len(V1)


def test_depth_zero_four_faces():
    V, F = generate_asymmetric_sierpinski(n_aft=0, n_fore=0)
    assert len(F) == 4
    assert len(V) == 4


def test_stl_roundtrip(tmp_path):
    V, F = generate_asymmetric_sierpinski(n_aft=1, n_fore=0)
    p = tmp_path / "out.stl"
    write_ascii_stl(p, V, F)
    text = p.read_text()
    assert text.startswith("solid ")
    assert "endsolid" in text
    assert text.count("facet normal") == len(F)


def test_surface_samples_shape():
    V, F = generate_asymmetric_sierpinski(n_aft=1, n_fore=0)
    pts = surface_sample_points(V, F, n_per_face=2)
    assert pts.ndim == 2 and pts.shape[1] == 3
    assert len(pts) == len(F) * 6  # bary grid for n=2: 6 points
