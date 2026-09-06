# Claim status — sierpinski-geometry-045

**Classification:** RESEARCH  
**Claim level (CLAIM_VALIDATION.md):** 1 (mathematical / geometric framework)  
**Sweep:** 089 (2026-09-06)

## Allowed claims

- This repository generates an asymmetric Sierpinski-type tetrahedral mesh with design scale factor α = 0.45.
- Recursion depths `n_aft` / `n_fore` are configurable.
- Outputs are vertices, faces, optional ASCII STL, optional barycentric surface samples.

## Forbidden / unsupported claims

- No electromagnetic field solution.
- No LDOS, force, thrust, or energy-extraction prediction.
- Green CI does not raise physics claim level above 1.
- Downstream repositories (coherence-drive, stress-tensor-modification, ware-constant-phenomenology) are not validated by this mesh generator.

## Software readiness (separate from claim level)

- Unit tests: `test_sierpinski_generator.py` (7 passed locally).
- GitHub Actions: `.github/workflows/python-tests.yml` run **34063280255** conclusion **success** (head_sha `c8f81089`).
