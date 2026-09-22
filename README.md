<div align="center">

# Sierpinski Geometry · 0.45

### The **shape** the rest of the stack talks about — not the force

[![RESEARCH](https://img.shields.io/badge/RESEARCH-claim_level_1-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)

</div>

**Classification:** RESEARCH (Sweep-159e). Geometry generator + graph algebra. Claim level 1.

Lock catalog: [INDEX.md](INDEX.md).

---

## Why this exists

Field solvers need a mesh. Theory needs a fixed scale ratio.  
**0.45** is the locked **design** scale factor for asymmetric aft/fore recursive (Sierpinski-type) structure used across the Coherence Drive *research* line.

It is **not** a spectral-dimension threshold and it does **not** generate net momentum. See [FALSIFICATION.md](FALSIFICATION.md).

## Why you need it

| You… | Open this |
|------|-----------|
| Run BEM / surface integrals | Generate STL / mesh inputs |
| Quote “0.45 asymmetry” | Share one generator, not hand-waved CAD |
| Check gasket N / D_3 flux | `gasket_flux_audit.py` |
| Check printed-trace / shear diagnostics | `conductance_shear.py` |
| Quote 3/5, 5/3, 1/5, or tilt growth | [INDEX.md](INDEX.md) |
| Claim thrust from geometry alone | **Don’t** |

## How it works

```bash
pip install -r requirements.txt
python sierpinski_generator.py --info --n-aft 3 --n-fore 1
python gasket_flux_audit.py
python conductance_shear.py
pytest -q
```

Four recurrences live on four problems (energy, resistance, Dirichlet spectrum, unit-load tilt). Do not fuse them.  
**No** field solve, **No** force claim, **No** energy claim.

## Tests / CI

- `test_sierpinski_generator.py`
- `test_gasket_flux_audit.py`
- `test_conductance_shear.py`
- GitHub Actions: `.github/workflows/python-tests.yml`

## Downstream / upstream

- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)
- Spectrum consumer: [m2-renormalization-law](https://github.com/beyond-repair/m2-renormalization-law)
- Solvers: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)
- Governance: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)
