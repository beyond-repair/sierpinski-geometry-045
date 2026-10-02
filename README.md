<div align="center">

# Sierpinski Geometry · 0.45

### The **shape** the rest of the stack talks about — not the force

[![RESEARCH](https://img.shields.io/badge/RESEARCH-claim_level_1-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)

</div>

**Classification:** RESEARCH (Sweep-159e / Claim-0). Geometry generator + graph algebra. Claim level 1.

Lock catalog: [INDEX.md](INDEX.md). Runnable printout: `gasket_catalog.py` / `sierpinski-geometry-045`.

---

## Status of this tree

**RUNNABLE SKETCH — NOT A COMPLETE PRODUCT** (Claim-0 / RESEARCH).

Strangers can clone, install, generate the default α=0.45 asymmetric tetrahedron mesh, and run gasket flux / conductance / spectrum audits. This is **not** a field solve, **not** a force claim, and **not** a DSI period detection. No constant is refit.

```text
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```

## Why this exists

Field solvers need a mesh. Theory needs a fixed scale ratio.  
**0.45** is the locked **design** scale factor for asymmetric aft/fore recursive (Sierpinski-type) structure used across the Coherence Drive *research* line.

It is **not** a spectral-dimension threshold and it does **not** generate net momentum. See [FALSIFICATION.md](FALSIFICATION.md).

There is nothing to configure. No environment variables and no secrets. Depths, `alpha`, and graph level are command-line arguments. Defaults are the design values (`alpha=0.45`, aft depth 3, fore depth 1).

## Why you need it

| You… | Open this |
|------|-----------|
| Run BEM / surface integrals | Generate STL / mesh inputs |
| Quote “0.45 asymmetry” | Share one generator, not hand-waved CAD |
| Check gasket N / D₃ flux | `gasket_flux_audit.py` |
| Check printed-trace / shear diagnostics | `conductance_shear.py` |
| Reproduce spectrum, energy, resistance, heat trace, log-periodic miss | `gasket_catalog.py` |
| Quote 3/5, 5/3, 1/5, or tilt growth | [INDEX.md](INDEX.md) |
| Claim thrust from geometry alone | **Don’t** |

## Install, run, and test

Python 3.10+ (CI uses 3.11). No compile step. Nothing is downloaded at runtime.

```bash
git clone https://github.com/beyond-repair/sierpinski-geometry-045.git
cd sierpinski-geometry-045
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
sierpinski-geometry-045 --quick
python report.py --quick
python gasket_catalog.py --quick
python sierpinski_generator.py --info --n-aft 3 --n-fore 1 --no-save
python gasket_flux_audit.py
python conductance_shear.py
pytest -q
```

`sierpinski-geometry-045`, `python report.py`, and `python gasket_catalog.py` print the same Claim-0 catalog. Omit `--quick` to include the n=6 Dirichlet / log-periodic windows (~10–30 s). That scaled ground is about **11.210264**, not 0.08.

Drop `--no-save` on the generator to write `sierpinski045_mesh.npz`. Optional STL: `--stl out.stl`. Flat scripts still work from the repository root after `pip install -r requirements.txt` alone.

| Command | What passes | What it does not say |
|---------|-------------|----------------------|
| `sierpinski-geometry-045 [--quick]` | Mesh 48/36; flux α-sweep (0.45 not max); cond ratios ≠ 5/3; energy/R locks; heat-trace; DSI `established=False` | Thrust, BEM, W_★, or a measured log-5 period |
| `python sierpinski_generator.py --info …` | vertices/faces/edge stats; optional STL / npz | A physical transducer force |
| `python gasket_flux_audit.py` | N/E table; symmetric cancel; α-sweep; tilt line | Spectral thrust threshold at 0.45 |
| `python conductance_shear.py` | cond/geom locks; ratios ≠ 5/3; rotation blindness | Print-angle invariant or propulsion |
| `pytest -q` | Generator + flux + shear + exact-graph + catalog + docs locks | Product physics CI |

## What the code prints (not a fit)

These are outputs of `gasket_catalog.py`, not targets that were tuned:

- Default mesh: **48 vertices, 36 faces**. Face count is `3**n_aft + 3*(3**n_fore)` because the middle triangle is omitted.
- Symmetric Dirichlet data, `α=0.45`, level 2: `||F||` is machine zero (about `10^{-15}`).
- Asymmetric corners `(1,-0.5,0)`: `||F||(0.45) ≈ 1.165909`, which is **below** `||F||(0.25) ≈ 1.320925`. **0.45 is not a peak.**
- Conductance (`γ=1`) level scan at `0.45°`: generation ratios **2.800003, 2.571432, 2.480003**, not 5/3.
- `K_4` applied to other levels returns **0.138889, 0.388888, 1, 2.480003**. Not an angle meter.
- Harmonic edge-sum with data `(1,0,0)`: `(5/3)^n E_n = 2`, not 1. The half-sum reading is 1. See [KIGAMI_LAPLACIAN.md](KIGAMI_LAPLACIAN.md).
- Two-corner resistance grows by exactly **5/3** per level, starting at 2/3.
- Free `λ_max` is **5.302776 at n=1** (not 6) and **6 for n≥2**.
- Dirichlet `5^n λ_min` through n=6 approaches **11.210264**, not 0.08. The n=5 ratio to the previous ground state is **0.200144**, not exactly 1/5.
- Renormalized Poisson energy at n=5 is **0.124960**, not exactly 1/8, and the limit is not claimed.
- Pre-registered log-periodic windows at n=6 fail: two-period slopes about **-0.837, -0.884, -0.933** versus target **-0.682606**, and the amplitude is monotone. DSI period is **NOT ESTABLISHED**.

`d_s/2 ≈ 0.682606`, which is not less than 1/2, not 0.45, and not 0.08.

UNSUPPORTED: thrust, EM fields, LDOS-as-force, energy extraction, α=0.45 as a spectral-dimension threshold, Kigami 3/5 or 5/3 as the tilt-F growth law, mult(λ=6) as pinch η=0.92.

Four recurrences live on four problems (energy, resistance, Dirichlet spectrum, unit-load tilt). Do not fuse them.  
**No** field solve, **No** force claim, **No** energy claim.

## Tests / CI

- `test_sierpinski_generator.py`
- `test_gasket_flux_audit.py`
- `test_conductance_shear.py`
- `test_exact_graph.py`
- `test_gasket_catalog.py` (includes one level-6 eigen-solve and the DSI miss)
- `test_docs.py`
- GitHub Actions: `.github/workflows/python-tests.yml` (unchanged by this Claim-0 pass; a green run is not a higher claim level)

## Downstream / upstream

- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)
- Spectrum consumer: [m2-renormalization-law](https://github.com/beyond-repair/m2-renormalization-law)
- Pinch hypothesis: [topological-pinch](https://github.com/beyond-repair/topological-pinch)
- Solvers: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)
- Governance: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)
