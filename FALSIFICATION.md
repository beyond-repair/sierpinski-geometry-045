# α = 0.45 flux-threshold falsification — Sweep-138

**Date:** 2026-09-15  
**Status:** RESEARCH / claim level 1  
**Repo role:** geometry generator + graph-level symmetry audit  
**Does not claim thrust, LDOS, or energy extraction.**

## 1. What was tested

A circulating claim that the design scale

$$\alpha = 0.45$$

is a *spectral-dimension threshold* that **generates net boundary momentum** on a Sierpiński gasket (sometimes written \(d_s^{\rm eff}/2 < 1/2\)).

The only falsifiable piece of that claim is a linear-algebra statement about a discrete fractional Laplacian on the gasket graph. That statement was executed.

Reproduction:

```bash
python3 gasket_flux_audit.py
pytest -q test_gasket_flux_audit.py test_sierpinski_generator.py
```

## 2. Locked graph facts (deterministic)

Sierpiński gasket vertex counts (corner-identified copies):

| level | \(N\) |
|------:|------:|
| 0 | 3 |
| 1 | 6 |
| 2 | 15 |
| 3 | 42 |
| 4 | 123 |

A comment that “level 3 gives \(N=15\)” is **false**. Level 2 gives \(N=15\); level 3 gives \(N=42\).

Sierpiński spectral dimension (literature, not fitted here):

$$
d_s = \frac{2\ln 3}{\ln 5} \approx 1.36512,\qquad \frac{d_s}{2} \approx 0.68256.
$$

The inequality \(d_s/2 < 1/2\) is arithmetically **false** (\(0.68256 > 0.5\)).

## 3. Spectral / source tests (combinatorial \(L^\alpha\), level 2)

Dirichlet data on the three corners. Net vector flux is the current leaving each corner, weighted by corner position relative to the centroid.

| excitation | \(\alpha\) | \(\|F\|\) |
|------------|-----------:|----------:|
| corners \((1,-0.5,0)\) | 0.45 | \(1.1659\times 10^{0}\) |
| corners \((1,1,1)\) | 0.45 | \(\sim 10^{-15}\) (machine zero) |

Same asymmetric data, \(\alpha\) sweep (combinatorial operator):

| \(\alpha\) | \(\|F\|\) |
|----------:|----------:|
| 0.25 | 1.321 |
| **0.45** | **1.166** |
| 0.6826 | 1.005 |
| 1.00 | 0.825 |
| 2.00 | 0.534 |

Verdict:

- Nonzero flux under *asymmetric* Dirichlet data is the trivial action of a linear operator on an asymmetric vector.
- Symmetric Dirichlet data produces **zero** net flux to machine precision. No spontaneous \(D_3\) breaking.
- \(\alpha = 0.45\) is **not** a maximum and **not** a critical point of \(\|F\|(\alpha)\) on this operator.
- Exact \(\|F\|(\alpha)\) values depend on discretization (combinatorial vs geometric weights, level, source convention). The *absence* of a 0.45 threshold does not.

These numbers are **not** the C++ table from an external notebook. They are the lock for *this* script. Qualitative agreement with that notebook is recorded; numerical identity is not claimed.

## 4. Geometric tilt tests (weighted Laplacian, symmetric load)

Connectivity stays the printed lattice. Coordinates take a one-sided shear \(x \leftarrow x + y\tan\theta\). Operator weights are \(1/\ell_{ij}^2\). Excitation is Dirichlet 0 on the three corners and unit load on every interior vertex (symmetric source).

| \(\theta\) (deg) | \(\|F\|\) | \(\|F\| / \theta_{\rm rad}\) |
|----------------:|----------:|--------------------------:|
| 0.00 | 0 | — |
| 0.10 | 0.001632 | 0.935 |
| **0.45** | **0.007346** | 0.935 |
| 1.00 | 0.016321 | 0.935 |
| 2.00 | 0.032626 | 0.935 |
| 5.00 | 0.081270 | 0.931 |

Verdict:

- Zero tilt \(\Rightarrow\) zero flux. The symmetry theorem holds.
- Response is linear in small tilt. \(0.45^\circ\) has **no** special status; it is one point on a line through the origin.
- Allowed reading: a static flux diagnostic for *print skew* (strain-gauge analogue).
- Forbidden reading: net thrust or momentum generation by a static field on a static object.

## 5. What survives elsewhere (not certified by this repo)

These items are **out of scope** here. They are not promoted by this lock.

- Spectral decimation pole structure of the gasket Laplacian (Strichartz / Kigami).
- Log-periodic heat-kernel oscillations on fractals with discrete scale invariance.
- Proposed Casimir / AFM signatures of that log-periodicity.

Those belong in a fractal-QFT or Casimir-geometry satellite if one is opened. They do **not** restore the 0.45 thrust threshold.

Schwarzschild–Ware / Coherence Drive propulsion claims remain **UNSUPPORTED** and are logically separable from gasket graph algebra.

## 6. Forbidden moves

- Treat \(\alpha = 0.45\) as an empirically fitted physical law or a spectral critical value.
- Quote net flux from an asymmetric source as “generated momentum.”
- Promote \(\|F\|\sim 10^{-3}\) at \(0.45^\circ\) tilt to laboratory thrust.
- Use \(d_s/2 < 1/2\) as a written inequality.
- Raise claim level because CI is green.

## 7. Allowed next derivation

Only these elevate a *geometry* claim, and none of them become a force claim without a mesh-converged evaluator in [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification):

1. Level-4 / level-5 tilt sensitivity with edge-length-weighted Laplacians (resistor/capacitor print analogue).
2. Finite-size crossover of any log-periodic observable — still not thrust.
3. Keep \(\alpha = 0.45\) as the **design scale factor** of `generate_asymmetric_sierpinski`.
