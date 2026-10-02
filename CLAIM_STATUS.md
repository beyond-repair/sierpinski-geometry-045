# Claim status — sierpinski-geometry-045

**Classification:** RESEARCH  
**Claim level:** 1  
**Status:** RUNNABLE SKETCH — NOT A COMPLETE PRODUCT (Claim-0). Unverified as physics.  
**Sweep:** 159e / 159g (2026-09-22) + Claim-0 stranger path (2026-10-02)

```text
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```

Catalog: [INDEX.md](INDEX.md).

## Allowed claims

- Asymmetric Sierpinski-type tetrahedral mesh with design scale factor α = 0.45.
- Default generator (α=0.45, n_aft=3, n_fore=1): **48 vertices, 36 faces**; edge mean ≈ 0.220761 (geometry only).
- Graph audit (`gasket_flux_audit.py` / `gasket_graph.py`): N(2)=15, N(3)=42, N(4)=123; E=3^(n+1); λ_max=6 for n≥2; symmetric load ⇒ flux machine-zero; α=0.45 is **not** a spectral thrust threshold (asymmetric \|\|F\|\| at 0.45 ≈ 1.165909 is below α=0.25 ≈ 1.320925); small shear ⇒ linear print-skew diagnostic.
- Conductance / shear (`conductance_shear.py`): γ=1 is 1/ℓ; γ=2 is Sweep-138 1/ℓ²; γ=0 is metric-blind; level-2 θ=0.45° locks cond≈0.00367285, geom≈0.00734563; F∝γ at small θ; rotation and iso-scale Jacobians vanish; buses are a shunt; cond level-scan ratios ≈2.80/2.57/2.48 are **not** 5/3.
- PCF / Kigami (`KIGAMI_PCF.md`, `gasket_catalog.py`): harmonic edge-sum ratio 3/5 and `(5/3)^n E_n = 2` (not 1); half-sum reading is 1; two-corner resistance ratio 5/3 on combinatorial unit edges.
- Spectrum (`SPECTRUM.md`): λ_max=6 for n≥2; Tr L=6·3^n; mult(λ=6)=3/2(3^{n-1}-1); Dirichlet λ_min ratios → 1/5; 5^6 λ_min^D ≈ 11.210 (lock continues).
- DSI / log-periodic (`LOG_PERIODIC.md`): period log 5 is a literature/hypothesis form; on these graphs at n≤6 it is **NOT ESTABLISHED**. Pre-registered two-period n=6 windows fail (slope −0.837…−0.934 vs target −0.683; A(τ) monotone).

## Forbidden / UNSUPPORTED

- Electromagnetic fields, LDOS-as-force, thrust, energy extraction.
- α=0.45 as a spectral-dimension critical value or geometric angle.
- d_s/2 < 1/2 (false; d_s/2 ≈ 0.682606).
- Kigami 3/5 or 5/3 as the tilt-F growth law.
- K_n=θ/‖F‖_n as a generation-invariant print angle.
- Measure-normalized tilt limit as proven.
- mult(λ=6) as topological-pinch η=0.92.
- Log-periodic amplitude/phase of ψ as measured; use as W_★.
- Validation of coherence-drive, stress-tensor-modification, or Ware phenomenology by this generator.
- Raising claim level because CI is green.
- Refitting α=0.45 or spectral locks to force a pass.

## Software readiness

Stranger path: `pip install -r requirements.txt && pip install -e .`, then
`sierpinski-geometry-045` / `python report.py` / flat scripts / `pytest -q`.

Tests: `test_sierpinski_generator.py`, `test_gasket_flux_audit.py`,
`test_conductance_shear.py`, `test_exact_graph.py`, `test_gasket_catalog.py`, `test_docs.py`.  
Releases / tags: none.
