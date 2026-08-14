#!/usr/bin/env python3
"""
sierpinski_generator.py
-----------------------
Generate the 0.45-scaled asymmetric Sierpinski tetrahedron used as the
Coherence Drive geometric transducer.

Asymmetry rule (design intent):
  - Aft face (vertex 3 opposite) is recursed to depth n_aft (default 3)
  - Fore faces remain at depth n_fore (default 1)

Scaling factor α = 0.45 is exact.

Outputs:
  - vertices (Nx3), faces (Mx3) as NumPy arrays
  - optional ASCII STL
  - optional surface sampling points for downstream LDOS / stress proxies

This script produces geometry only. It does not compute electromagnetic
fields, LDOS, force, or thrust.
"""

from __future__ import annotations
import argparse
import numpy as np
from pathlib import Path
from typing import List, Tuple

# Regular tetrahedron vertices (centered, edge length ~√2)
_BASE_VERTICES = np.array([
    [1.0,  1.0,  1.0],
    [1.0, -1.0, -1.0],
    [-1.0, 1.0, -1.0],
    [-1.0, -1.0, 1.0],
], dtype=float)
_BASE_VERTICES -= _BASE_VERTICES.mean(axis=0)
_BASE_VERTICES /= np.linalg.norm(_BASE_VERTICES[0] - _BASE_VERTICES[1])  # unit edge


def _midpoint(a: np.ndarray, b: np.ndarray, alpha: float = 0.45) -> np.ndarray:
    """Point dividing segment a→b at fraction alpha from a."""
    return (1.0 - alpha) * a + alpha * b


def _subdivide_face(
    v0: np.ndarray,
    v1: np.ndarray,
    v2: np.ndarray,
    depth: int,
    alpha: float,
    vertices: List[np.ndarray],
    faces: List[Tuple[int, int, int]],
    vertex_index: dict,
) -> None:
    """Recursive face subdivision with fixed scaling alpha."""
    def idx(v: np.ndarray) -> int:
        key = tuple(np.round(v, decimals=10))
        if key not in vertex_index:
            vertex_index[key] = len(vertices)
            vertices.append(v.copy())
        return vertex_index[key]

    i0, i1, i2 = idx(v0), idx(v1), idx(v2)

    if depth <= 0:
        faces.append((i0, i1, i2))
        return

    # Three edge points at fraction alpha
    m01 = _midpoint(v0, v1, alpha)
    m12 = _midpoint(v1, v2, alpha)
    m20 = _midpoint(v2, v0, alpha)

    # Four child faces (Sierpinski: keep corners, omit center)
    _subdivide_face(v0, m01, m20, depth - 1, alpha, vertices, faces, vertex_index)
    _subdivide_face(v1, m12, m01, depth - 1, alpha, vertices, faces, vertex_index)
    _subdivide_face(v2, m20, m12, depth - 1, alpha, vertices, faces, vertex_index)
    # Center triangle is omitted → classic Sierpinski gasket on the face


def generate_asymmetric_sierpinski(
    alpha: float = 0.45,
    n_aft: int = 3,
    n_fore: int = 1,
    aft_vertex: int = 3,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build the asymmetric tetrahedron.

    Parameters
    ----------
    alpha : float
        Exact scaling factor (design value 0.45).
    n_aft : int
        Recursion depth on the aft face (opposite aft_vertex).
    n_fore : int
        Recursion depth on the three fore faces.
    aft_vertex : int
        Index of the vertex that defines the aft direction (0..3).

    Returns
    -------
    vertices : (N, 3) float array
    faces : (M, 3) int array
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must lie in (0, 1)")
    if n_aft < 0 or n_fore < 0:
        raise ValueError("depths must be non-negative")

    base = _BASE_VERTICES.copy()
    vertices: List[np.ndarray] = []
    faces: List[Tuple[int, int, int]] = []
    vertex_index: dict = {}

    # Four faces of the tetrahedron; face i is the one opposite vertex i
    face_indices = [
        (1, 2, 3),  # opposite 0
        (0, 2, 3),  # opposite 1
        (0, 1, 3),  # opposite 2
        (0, 1, 2),  # opposite 3  ← default aft face
    ]

    for opp, (a, b, c) in enumerate(face_indices):
        depth = n_aft if opp == aft_vertex else n_fore
        _subdivide_face(
            base[a], base[b], base[c],
            depth, alpha, vertices, faces, vertex_index
        )

    V = np.array(vertices, dtype=float)
    F = np.array(faces, dtype=int)
    return V, F


def write_ascii_stl(path: Path, vertices: np.ndarray, faces: np.ndarray, name: str = "sierpinski045") -> None:
    """Write a minimal ASCII STL."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"solid {name}\n")
        for i0, i1, i2 in faces:
            v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]
            n = np.cross(v1 - v0, v2 - v0)
            norm = np.linalg.norm(n)
            if norm > 0:
                n /= norm
            else:
                n = np.array([0.0, 0.0, 1.0])
            fh.write(f"  facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n")
            fh.write("    outer loop\n")
            for v in (v0, v1, v2):
                fh.write(f"      vertex {v[0]:.6e} {v[1]:.6e} {v[2]:.6e}\n")
            fh.write("    endloop\n")
            fh.write("  endfacet\n")
        fh.write(f"endsolid {name}\n")


def surface_sample_points(
    vertices: np.ndarray,
    faces: np.ndarray,
    n_per_face: int = 4,
) -> np.ndarray:
    """
    Return barycentric sample points on each triangular face.
    Useful as a lightweight proxy input for downstream field evaluators.
    """
    pts = []
    # simple uniform barycentric grid
    bary = []
    for i in range(n_per_face + 1):
        for j in range(n_per_face + 1 - i):
            k = n_per_face - i - j
            bary.append((i / n_per_face, j / n_per_face, k / n_per_face))
    bary = np.array(bary)

    for i0, i1, i2 in faces:
        v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]
        for a, b, c in bary:
            pts.append(a * v0 + b * v1 + c * v2)
    return np.array(pts)


def main():
    parser = argparse.ArgumentParser(description="0.45 asymmetric Sierpinski tetrahedron generator")
    parser.add_argument("--alpha", type=float, default=0.45, help="scaling factor (design=0.45)")
    parser.add_argument("--n-aft", type=int, default=3, help="recursion depth on aft face")
    parser.add_argument("--n-fore", type=int, default=1, help="recursion depth on fore faces")
    parser.add_argument("--stl", type=str, default="", help="output STL path (optional)")
    parser.add_argument("--samples", type=int, default=0, help="if >0, also write surface sample points")
    parser.add_argument("--info", action="store_true", help="print mesh statistics")
    args = parser.parse_args()

    V, F = generate_asymmetric_sierpinski(
        alpha=args.alpha, n_aft=args.n_aft, n_fore=args.n_fore
    )

    if args.info or not args.stl:
        edge_lengths = []
        for i0, i1, i2 in F:
            edge_lengths.extend([
                np.linalg.norm(V[i0] - V[i1]),
                np.linalg.norm(V[i1] - V[i2]),
                np.linalg.norm(V[i2] - V[i0]),
            ])
        print(f"Vertices : {len(V)}")
        print(f"Faces    : {len(F)}")
        print(f"Alpha    : {args.alpha}")
        print(f"Depths   : aft={args.n_aft}, fore={args.n_fore}")
        print(f"Edge len : mean={np.mean(edge_lengths):.6f}, std={np.std(edge_lengths):.6f}")

    if args.stl:
        out = Path(args.stl)
        write_ascii_stl(out, V, F)
        print(f"Wrote STL → {out.resolve()}")

    if args.samples > 0:
        pts = surface_sample_points(V, F, n_per_face=args.samples)
        np.save("surface_samples.npy", pts)
        print(f"Wrote {len(pts)} surface samples → surface_samples.npy")

    # Always save the raw mesh for downstream use
    np.savez("sierpinski045_mesh.npz", vertices=V, faces=F)
    print("Wrote mesh → sierpinski045_mesh.npz")


if __name__ == "__main__":
    main()
