# Sierpinski Geometry 0.45 (Coherence Drive)

**© 2026 William B. Ware / Atomic Dream Labs — All Rights Reserved.**

**Status (2026-08-14):** Geometry generator now provided. Electromagnetic / LDOS / force calculations remain future work.

---

## 1. Target Geometry

- Base polyhedron: tetrahedron.
- Scaling factor: exactly **0.45**.
- Recursion asymmetry: aft face carried to depth `n_aft` (default 3); fore faces left at `n_fore` (default 1).
- Intended effect: directed LDOS gradient that peaks on the aft face.

Approximate fractal dimension of the limiting set: \(D\approx 0.868\) (motivates the M2 exponent 0.23).

---

## 2. Generator

```bash
python sierpinski_generator.py --info
python sierpinski_generator.py --stl coherence_drive_sierpinski.stl --n-aft 3 --n-fore 1
python sierpinski_generator.py --samples 3   # also writes surface_samples.npy
```

Outputs:
- `sierpinski045_mesh.npz` — vertices & faces
- optional ASCII STL
- optional surface sample points for downstream evaluators

The script produces **geometry only**. It does not compute fields, LDOS, residual force, or thrust.

---

## 3. Role in the Framework

This geometry is the proposed physical transducer that converts a drive field into a spatially modulated informational stress. It appears in the engineering target, the M2 arguments, and the topological-pinch / momentum-closure hypotheses.

---

## Cross-References

- Integration status: [coherence-drive](https://github.com/beyond-repair/coherence-drive)
- Stress-tensor evaluator: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)
- Canonical mathematics: [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)
