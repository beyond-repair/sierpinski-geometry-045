# Claim status — sierpinski-geometry-045

**Classification:** RESEARCH  
**Claim level (CLAIM_VALIDATION.md):** 1 (mathematical / geometric framework)  
**Sweep:** 138 (2026-09-15) — prior lock Sweep-114 (2026-09-07)

## Allowed claims

- This repository generates an asymmetric Sierpinski-type tetrahedral mesh with design scale factor α = 0.45.
- Recursion depths `n_aft` / `n_fore` are configurable.
- Outputs are vertices, faces, optional ASCII STL, optional barycentric surface samples.
- Graph-level audit (`gasket_flux_audit.py`):
  - gasket vertex counts \(N(2)=15\), \(N(3)=42\);
  - symmetric Dirichlet data ⇒ net flux at machine zero;
  - α = 0.45 is not a flux-generating spectral threshold;
  - small geometric shear with a symmetric interior load produces a flux linear in tilt angle (print-skew diagnostic, not thrust).

## Forbidden / UNSUPPORTED claims

The following claims are **UNSUPPORTED**:

- UNSUPPORTED: electromagnetic field solution from this generator.
- UNSUPPORTED: LDOS, force, thrust, or energy-extraction prediction.
- UNSUPPORTED: α = 0.45 as a spectral-dimension critical value that generates net boundary momentum.
- UNSUPPORTED: \(d_s/2 < 1/2\) (false; \(d_s/2 \approx 0.6826\)).
- UNSUPPORTED: static flux on a static mesh as laboratory thrust.
- UNSUPPORTED: raising physics claim level above 1 because CI is green.
- UNSUPPORTED: validation of coherence-drive, stress-tensor-modification, or ware-constant-phenomenology by this mesh generator.

See [FALSIFICATION.md](FALSIFICATION.md).

## Software readiness (separate from claim level)

- Unit tests: `test_sierpinski_generator.py`, `test_gasket_flux_audit.py`.
- GitHub Actions: `.github/workflows/python-tests.yml`
  - prior: run **34063280255** conclusion **success** (head_sha `c8f81089`)
  - prior: run **34063349923** conclusion **success** (head_sha `bea3705c`)
- Releases / tags: none (not queued this sweep).
