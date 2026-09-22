# Claim status — sierpinski-geometry-045

**Classification:** RESEARCH  
**Claim level:** 1  
**Sweep:** 159e (2026-09-22)

Catalog: [INDEX.md](INDEX.md).

## Allowed claims

- Asymmetric Sierpinski-type tetrahedral mesh with design scale factor α = 0.45.
- Graph audit (`gasket_flux_audit.py`): N(2)=15, N(3)=42; symmetric load ⇒ flux 0; α=0.45 is not a spectral thrust threshold; small shear ⇒ linear print-skew diagnostic.
- Conductance / shear (`conductance_shear.py`): γ=1 is 1/ℓ; γ=2 is Sweep-138 1/ℓ²; γ=0 is metric-blind; F∝γ at small θ; rotation and iso-scale Jacobians vanish; buses are a shunt.
- PCF / Kigami (`KIGAMI_PCF.md`): harmonic energy ratio 3/5; two-corner resistance ratio 5/3 on combinatorial unit edges.
- Spectrum (`SPECTRUM.md`): λ_max=6 for n≥2; Tr L=6·3^n; mult(λ=6)=3/2(3^{n-1}-1); Dirichlet λ_min ratios → 1/5.

## Forbidden / UNSUPPORTED

- Electromagnetic fields, LDOS-as-force, thrust, energy extraction.
- α=0.45 as a spectral-dimension critical value or geometric angle.
- d_s/2 < 1/2 (false).
- Kigami 3/5 or 5/3 as the tilt-F growth law.
- K_n=θ/‖F‖_n as a generation-invariant print angle.
- Measure-normalized tilt limit as proven.
- mult(λ=6) as topological-pinch η=0.92.
- Validation of coherence-drive, stress-tensor-modification, or Ware phenomenology by this generator.
- Raising claim level because CI is green.

## Software readiness

Tests: `test_sierpinski_generator.py`, `test_gasket_flux_audit.py`, `test_conductance_shear.py`.  
Releases / tags: none.
