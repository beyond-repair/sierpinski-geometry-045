# Fractal heat kernel on the gasket — 2026-09-22

**Claim level:** 1  
Not thrust. Not \(W_\star\). Complements [KIGAMI_LAPLACIAN.md](KIGAMI_LAPLACIAN.md).

## 1. Operators

Combinatorial semigroup: \(p_n(t)=e^{-t L_n}\).  
Kigami-scaled Dirichlet semigroup: \(P_n(\tau)=\exp(-\tau\, 5^n L_n^D)\).

Continuum identification: graph time and Kigami time are related by \(t=\tau\,5^n\) on level \(n\).

On-diagonal kernel / trace:

$$
Z_n(\tau)=\mathrm{Tr}\,P_n(\tau)=\sum_k e^{-\tau\,5^n\lambda_k(L_n^D)}.
$$

Return probability on the raw graph:

$$
\bar p_n(t)=\frac1{N}\mathrm{Tr}\,e^{-t L_n}.
$$

## 2. Dimensions (exact, standard SG)

$$
d_s=\frac{2\log 3}{\log 5}\approx 1.365212,
\qquad
\frac{d_s}{2}\approx 0.682606,
\qquad
d_w=\frac{\log 5}{\log 2}\approx 2.321928.
$$

Hausdorff dimension \(d_f=\log 3/\log 2\approx 1.58496\) and the Einstein relation \(d_w=2 d_f/d_s\) hold for this gasket.  
\(d_s/2<1/2\) is false (already in FALSIFICATION.md).

Sub-Gaussian bound (literature form, not re-proved here):

$$
p_\tau(x,y)\ \le\ C\,\tau^{-d_s/2}\exp\Bigl(-c\bigl(d(x,y)^{d_w}/\tau\bigr)^{1/(d_w-1)}\Bigr).
$$

## 3. Executed traces

Dirichlet Kigami trace (corners killed):

| \(n\) | \(Z(0.01)\) | \(Z(0.03)\) | \(Z(0.10)\) |
|------:|------------:|------------:|------------:|
| 2 | 4.970 | 1.698 | 0.398 |
| 3 | 3.853 | 1.483 | 0.379 |
| 4 | 3.657 | 1.457 | 0.375 |
| 5 | 3.628 | 1.453 | 0.374 |

At fixed small \(\tau\), \(Z_n(\tau)\) is stabilizing in \(n\). That is the killed continuum trace starting to exist. Large \(\tau\) is the ground-state tail \(e^{-\tau\lambda_1^D}\) with \(\lambda_1^D\approx 11.21\).

Local log-log slope of \(Z_5(\tau)\):

| \(\tau\) mid | \(d\log Z/d\log\tau\) |
|-------------:|----------------------:|
| 0.004–0.016 | \(-0.74\) to \(-0.83\) |
| 0.025–0.06 | \(-0.87\) to \(-1.18\) |
| \(\ge 0.16\) | steeper (ground-state cutoff) |

Target continuum short-time slope \(-d_s/2\approx -0.683\). The computed window is in the right ballpark and already contaminated by Dirichlet killing plus finite \(n\). It is **not** a high-precision measurement of \(d_s\).

Raw-graph return probability \(\bar p_n(t)\) at \(n=5\) has mid-window slopes \(-0.66\) to \(-0.75\), closer to \(-d_s/2\), then flattens toward the spectral gap.

## 4. Spatial inhomogeneity

Level 4, Kigami time \(\tau=0.1\), combinatorial kernel at \(t=\tau 5^4\):

- mean on-diagonal \(\approx 0.0109\)
- corner mean \(\approx 0.0061\)
- interior mean \(\approx 0.0110\)

Corners are colder. A single number “LDOS heat” is not defined until the region is named (same rule as pinch \(\eta\)).

## 5. Log-periodic oscillations

True SG heat kernels are expected to have log-periodic oscillations in \(\tau\) with period related to \(5^{k}\) (discrete scale invariance). Levels \(\le 5\) do **not** resolve a stable periodic component. The freeze item “log-periodic amplitude on a heat kernel” remains **unresolved** as a measurement.

## 6. Forbidden promotions

- \(Z(\tau)\) or \(\bar p(t)\) is not \(F_n\) and not thrust.
- \(d_s/2\approx 0.683\) is not \(W_\star\) and not \(\alpha=0.45\).
- Short-time slope \(\approx -0.7\) is not a derivation of \(0.08\).

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```
