# Claim status — sierpinski-geometry-045

**Classification:** RESEARCH  
**Claim level (CLAIM_VALIDATION.md):** 1 (mathematical / geometric framework)  
**Sweep:** 114 (2026-09-07) — prior lock Sweep-089

## Allowed claims

- This repository generates an asymmetric Sierpinski-type tetrahedral mesh with design scale factor α = 0.45.
- Recursion depths `n_aft` / `n_fore` are configurable.
- Outputs are vertices, faces, optional ASCII STL, optional barycentric surface samples.

## Forbidden / UNSUPPORTED claims

The following claims are **UNSUPPORTED**:

- UNSUPPORTED: electromagnetic field solution from this generator.
- UNSUPPORTED: LDOS, force, thrust, or energy-extraction prediction.
- UNSUPPORTED: raising physics claim level above 1 because CI is green.
- UNSUPPORTED: validation of coherence-drive, stress-tensor-modification, or ware-constant-phenomenology by this mesh generator.

## Software readiness (separate from claim level)

- Unit tests: `test_sierpinski_generator.py`.
- GitHub Actions: `.github/workflows/python-tests.yml`
  - run **34063280255** conclusion **success** (head_sha `c8f81089`)
  - run **34063349923** conclusion **success** (head_sha `bea3705c`)
- Releases / tags: none (not queued this sweep).
