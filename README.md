<div align="center">

# Sierpinski Geometry · 0.45

### The **shape** the rest of the stack talks about — not the force

[![RESEARCH](https://img.shields.io/badge/RESEARCH-claim_level_1-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)

</div>

**Classification:** RESEARCH (Sweep-138). Geometry generator + graph symmetry audit. Claim level 1.

---

## Why this exists

Field solvers need a mesh. Theory needs a fixed scale ratio.  
**0.45** is the locked **design** scale factor for asymmetric aft/fore recursive (Sierpinski-type) structure used across the Coherence Drive *research* line.

It is **not** a spectral-dimension threshold and it does **not** generate net momentum. That claim was executed and rejected. See [FALSIFICATION.md](FALSIFICATION.md).

## Why you need it

| You… | Open this |
|------|-----------|
| Run BEM / surface integrals | Generate STL / mesh inputs |
| Quote “0.45 asymmetry” | Share one generator, not hand-waved CAD |
| Check gasket \(N\) / \(D_3\) flux | `gasket_flux_audit.py` |
| Claim thrust from geometry alone | **Don’t** — this repo is shape + algebra only |

## How it works

```bash
pip install -r requirements.txt
python sierpinski_generator.py --info --n-aft 3 --n-fore 1
python sierpinski_generator.py --stl out.stl
python gasket_flux_audit.py
pytest -q
```

- α = 0.45 exact **design** scale ratio  
- Asymmetric aft/fore recursion depths configurable  
- Graph audit: symmetric source ⇒ zero net flux; tilt ⇒ linear diagnostic  
- **No** field solve, **No** force claim, **No** energy claim

See [CLAIM_STATUS.md](CLAIM_STATUS.md) and [GOVERNANCE.md](GOVERNANCE.md).

## Tests / CI

- `test_sierpinski_generator.py` — mesh invariants, bounds, STL write, samples.
- `test_gasket_flux_audit.py` — vertex counts, symmetry theorem, α-threshold rejection, tilt linearity.
- GitHub Actions: `.github/workflows/python-tests.yml`.

## Downstream / upstream

- Solvers: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)  
- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)  
- Math: [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)
- Governance: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)
