# Kigami Laplacian on the gasket — executed limits

**Date:** 2026-09-22  
**Claim level:** 1  
**Not** a Ware derivation. **Not** tilt-F. **Not** thrust.

Companion: [KIGAMI_PCF.md](KIGAMI_PCF.md), [SPECTRUM.md](SPECTRUM.md), [HEAT_KERNEL.md](HEAT_KERNEL.md).

## 1. Two renormalizations

$$
\mathcal{E}_n^{\rm comb}(u)=\sum_{E_n}(u_i-u_j)^2=\tfrac12 u^\top L_n u.
$$

Energy form: \((5/3)^n\mathcal{E}_n^{\rm comb}\).  
Laplacian vs \(\mu(\mathrm{cell})=3^{-n}\): \(5^n L_n\).

## 2. Energy lock, data \((1,0,0)\) on \(V_0\)

\((5/3)^n\mathcal{E}_n^{\rm comb}=1\) exactly at \(n=1\ldots 5\) in this convention. Ratio \(3/5\) exact in float.

## 3. Dirichlet spectral lock

| \(n\) | \(N\) | \(5^n\lambda_{\min}^D\) | raw \(\lambda_{\min}\) ratio |
|------:|------:|------------------------:|------------------------------:|
| 1 | 6 | 10.00000 | — |
| 2 | 15 | 10.96118 | 0.21922 |
| 3 | 42 | 11.16047 | 0.20364 |
| 4 | 123 | 11.20061 | 0.20072 |
| 5 | 366 | 11.20866 | 0.20014 |
| 6 | 1095 | **11.21026** | 0.20003 |

$$
\lambda_1^D\approx 11.210\qquad(n=6).
$$

\(\lambda_{\max}(L_n^D)=6\) at \(n=6\) still. Then \(5^n\cdot 6\to\infty\) (exceptional family).

## 4. Forbidden

\(11.21\neq 0.08\). Heat-trace DSI is not measured ([LOG_PERIODIC.md](LOG_PERIODIC.md)).
