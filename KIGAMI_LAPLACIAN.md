# Kigami Laplacian on the gasket — executed limits

**Date:** 2026-09-22  
**Claim level:** 1 (discrete → resistance-form analysis)  
**Not** a Ware derivation. **Not** a tilt-F law. **Not** thrust.

Companion: [KIGAMI_PCF.md](KIGAMI_PCF.md), [SPECTRUM.md](SPECTRUM.md).

## 1. Two different renormalizations

Combinatorial graph energy on level \(n\)

$$
\mathcal{E}_n^{\rm comb}(u)=\sum_{\{i,j\}\in E_n}(u_i-u_j)^2=\tfrac12 u^\top L_n u.
$$

| Object | Scaling | Why |
|--------|---------|-----|
| Resistance / energy form | \((5/3)^n \mathcal{E}_n^{\rm comb}\) | Harmonic extensions satisfy \(\mathcal{E}_{n+1}^{\rm comb}/\mathcal{E}_n^{\rm comb}=3/5\) |
| Laplacian vs self-similar measure \(\mu(\text{cell})=3^{-n}\) | \(5^n L_n = 3^n\cdot(5/3)^n L_n\) | energy / measure |

These must not be fused with unit-load tilt growth or with \(W_\star\).

## 2. Energy form (Dirichlet data \((1,0,0)\) on \(V_0\))

Executed, harmonic interior:

| \(n\) | \(N\) | \(\mathcal{E}_n^{\rm comb}\) | \((5/3)^n\mathcal{E}_n^{\rm comb}\) |
|------:|------:|----------------------------:|-----------------------------------:|
| 1 | 6 | 0.60000000 | **1.00000000** |
| 2 | 15 | 0.36000000 | **1.00000000** |
| 3 | 42 | 0.21600000 | **1.00000000** |
| 4 | 123 | 0.12960000 | **1.00000000** |
| 5 | 366 | 0.07776000 | **1.00000000** |

Ratio \(\mathcal{E}_{n+1}^{\rm comb}/\mathcal{E}_n^{\rm comb}=3/5\) exactly (float).  
The resistance-form energy of this boundary triple is the constant \(1\) in the \(\sum(\Delta u)^2\) convention used here.

Two-corner resistance (third floating) remains \(R_n=(2/3)(5/3)^n\) as in `KIGAMI_PCF.md`.

## 3. Dirichlet spectrum of raw \(L_n\), then \(5^n\)

Corners held at zero. First three Dirichlet eigenvalues of \(L_n\), times \(5^n\):

| \(n\) | \(\lambda_{\min}\) | \(5^n\lambda_{\min}\) | \(5^n\lambda_2\) | \(5^n\lambda_3\) | raw ratio \(\lambda_{\min}^{(n)}/\lambda_{\min}^{(n-1)}\) |
|------:|-------------------:|----------------------:|-----------------:|-----------------:|--------------------------------------------------------:|
| 1 | 2.000000 | 10.000000 | 25.000000 | 25.000000 | — |
| 2 | 0.438447 | 10.961180 | 34.549150 | 34.549150 | 0.21922 |
| 3 | 0.089284 | 11.160469 | 36.704730 | 36.704730 | 0.20364 |
| 4 | 0.017921 | 11.200615 | 37.146281 | 37.146281 | 0.20072 |
| 5 | 0.003587 | 11.208655 | 37.235013 | 37.235013 | 0.20014 |

Limits (numerical, \(n\le 5\)):

$$
5^n\lambda_{\min}(L_n^D)\ \to\ \lambda_1^D \approx 11.21,
\qquad
5^n\lambda_2^D=5^n\lambda_3^D\ \to\ \lambda_2^D \approx 37.25.
$$

Raw ratio \(\to 1/5\) is the same fact: the Kigami Dirichlet ground state is finite.

## 4. Exceptional combinatorial eigenvalue \(6\)

\(\lambda_{\max}(L_n)=6\) for \(n\ge 2\) (`SPECTRUM.md`). Then

$$
5^n\cdot 6 \to \infty.
$$

Those modes are *not* a finite continuum eigenvalue. They are the decimation-exceptional / highly localized family with multiplicity \(\frac32(3^{n-1}-1)\). They must not be identified with pinch \(\eta=0.92\) or with \(W_\star\).

Neumann (free) first positive eigenvalue: \(5^n\lambda_2^{\rm free}\) at \(n=5\) is \(\approx 17.94\) and still rising slowly — not claimed as a closed constant at this depth.

## 5. What this does not give

- A continuum tilt diagnostic. Unit-load \(F\) uses a different right-hand side and a different scaling.
- \(W_\star=1/(4\pi)\). Route C already failed; \(5^n\lambda_{\min}\approx 11.21\) is not \(0.08\).
- A Maxwell stress or thrust.

## 6. Reproduction

Harmonic solve on \(L_{\rm int}u=-L_{\rm int,\partial}u_\partial\), energy \(\sum_{\rm edges}(u_i-u_j)^2\), Dirichlet eigendecomposition of \(L_{\rm int}\). Levels 1–5 dense; level 6 optional.
