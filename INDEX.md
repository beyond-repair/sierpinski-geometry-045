# Lock catalog — sierpinski-geometry-045

**Sweep:** 159e (2026-09-22)  
**Claim level:** 1  
**Not thrust. Not LDOS. Not Stage 2.**

Read in this order.

| File | What it locks |
|------|----------------|
| [CLAIM_STATUS.md](CLAIM_STATUS.md) | Allowed / forbidden claims |
| [FALSIFICATION.md](FALSIFICATION.md) | α=0.45 is not a flux threshold; tilt is linear |
| [ZERO_POINT_FOUR_FIVE.md](ZERO_POINT_FOUR_FIVE.md) | Three different 0.45s |
| [FINDINGS_2026-09-21_CONDUCTANCE_SHEAR.md](FINDINGS_2026-09-21_CONDUCTANCE_SHEAR.md) | γ=1 vs γ=2, buses, shear Jacobian |
| [REVIEW_2026-09-21_TILT_WRITEUP.md](REVIEW_2026-09-21_TILT_WRITEUP.md) | F∝γ accepted; Kigami-as-F and K_n rejected |
| [KIGAMI_PCF.md](KIGAMI_PCF.md) | Energy 3/5, resistance 5/3 |
| [SPECTRUM.md](SPECTRUM.md) | λ_max=6, mult(6), Dirichlet λ_min → 1/5 |
| [CONFORMANCE_2026-09-21.md](CONFORMANCE_2026-09-21.md) | Problem split accepted; measure-tilt limit unproven |
| [GOVERNANCE.md](GOVERNANCE.md) | Mutation policy |

## Four recurrences (do not fuse)

| Object | Factor |
|--------|--------|
| Harmonic energy Ē_n | 3/5 |
| Two-corner resistance R_n | 5/3 |
| Dirichlet λ_min of raw L_n | → 1/5 |
| Unit-load tilt ‖F‖ | 2.80, 2.57, 2.48 (n=2	o5) |

## Reproduction

```bash
python3 gasket_flux_audit.py
python3 conductance_shear.py
pytest -q
```

Index of the chain: [coherence-drive PORTFOLIO_MATH](https://github.com/beyond-repair/coherence-drive/blob/main/docs/PORTFOLIO_MATH_2026-09-21.md).
