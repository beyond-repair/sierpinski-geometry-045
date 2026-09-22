# Claim status — sierpinski-geometry-045

**Classification:** RESEARCH  
**Claim level (CLAIM_VALIDATION.md):** 1 (mathematical / geometric framework)  
**Sweep:** 159 (2026-09-21) — prior Sweep-138 (2026-09-15), Sweep-114 (2026-09-07)

## Allowed claims

- This repository generates an asymmetric Sierpinski-type tetrahedral mesh with design scale factor α = 0.45.
- Recursion depths `n_aft` / `n_fore` are configurable.
- Outputs are vertices, faces, optional ASCII STL, optional barycentric surface samples.
- Graph-level audit (`gasket_flux_audit.py`):
  - gasket vertex counts \(N(2)=15\), \(N(3)=42\);
  - symmetric Dirichlet data ⇒ net flux at machine zero;
  - α = 0.45 is not a flux-generating spectral threshold;
  - small geometric shear with a symmetric interior load produces a flux linear in tilt angle (print-skew diagnostic, not thrust).
- Sweep-159 conductance / shear audit (`conductance_shear.py`):
  - constant-section traces use \(G=1/\ell\); Sweep-138 geometric lock remains \(G=1/\ell^2\);
  - combinatorial / self-similar \(w\propto\ell\) weights are blind to shear under this flux definition;
  - global trace width on a finest-only gasket does not change \(F\) at fixed vertex load;
  - rigid rotation and isotropic scale have vanishing Jacobian;
  - hierarchical buses change \(\|F\|\) by \(O(10\%\text{–}30\%)\), not a new regime.

## Forbidden / UNSUPPORTED claims

The following claims are **UNSUPPORTED**:

- UNSUPPORTED: electromagnetic field solution from this generator.
- UNSUPPORTED: LDOS, force, thrust, or energy-extraction prediction.
- UNSUPPORTED: α = 0.45 as a spectral-dimension critical value that generates net boundary momentum.
- UNSUPPORTED: \(d_s/2 < 1/2\) (false; \(d_s/2 \approx 0.6826\)).
- UNSUPPORTED: static flux on a static mesh as laboratory thrust.
- UNSUPPORTED: raising physics claim level above 1 because CI is green.
- UNSUPPORTED: validation of coherence-drive, stress-tensor-modification, or ware-constant-phenomenology by this mesh generator.
- UNSUPPORTED: generation-dependent width as a thrust amplifier.

See [FALSIFICATION.md](FALSIFICATION.md) and [FINDINGS_2026-09-21_CONDUCTANCE_SHEAR.md](FINDINGS_2026-09-21_CONDUCTANCE_SHEAR.md).

## Software readiness (separate from claim level)

- Unit tests: `test_sierpinski_generator.py`, `test_gasket_flux_audit.py`, `test_conductance_shear.py`.
- GitHub Actions: `.github/workflows/python-tests.yml`
- Releases / tags: none (not queued this sweep).
