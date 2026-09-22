# Log-periodic oscillations — search on this gasket

**Date:** 2026-09-22  
**Status:** Expected by DSI; **not measured** at levels \(n\le 6\).

Companion: [HEAT_KERNEL.md](HEAT_KERNEL.md).

## 1. Required form

$$
Z(\tau)=\tau^{-d_s/2}\,\psi(\log\tau),
\qquad
\psi(\theta+\log 5)=\psi(\theta),
\qquad
T_{\log}=\log 5\approx 1.609438.
$$

## 2. Pre-registered n=6 test

Criteria fixed before the run: (i) slope within a few percent of \(-d_s/2\approx -0.683\); (ii) at least two periods of \(\log 5\); (iii) no fit to \(0.08\).

Level 6: \(N=1095\), \(N_{\rm int}=1092\), \(\lambda_{\max}(L^D)=6\),
\(5^6\lambda_{\min}^D=11.21026\) (continues the Dirichlet lock).

| window | periods | slope | target | \(A\) rel. std | \(A\) endpoints |
|--------|---------|------:|-------:|---------------:|-----------------|
| \([0.003,0.075]\) | 2 | \(-0.837\) | \(-0.683\) | 0.145 | \(0.168\to 0.095\) |
| \([0.004,0.100]\) | 2 | \(-0.885\) | \(-0.683\) | 0.186 | \(0.165\to 0.078\) |
| \([0.005,0.125]\) | 2 | \(-0.934\) | \(-0.683\) | 0.225 | \(0.163\to 0.064\) |
| \([0.003,0.015]\) | 1 | \(-0.749\) | \(-0.683\) | 0.032 | \(0.168\to 0.149\) |

Two-period windows fail (i): slope is 22–37% too steep and \(A(\tau)\) is monotone.  
The one-period short window is closer to the target slope but fails (ii) by construction.

n=4,5 FFT bins near \(\log 5\) remain window harmonics (see prior revision).

## 3. Claim status

| Claim | Status |
|-------|--------|
| DSI period \(\log 5\) on the limit kernel | Literature / hypothesis |
| Period measured on these graphs, \(n\le 6\) | **Not established** |
| Amplitude / phase of \(\psi\) | Unknown |
| Use as \(W_\star\) or thrust | Forbidden |

Freeze line on heat-kernel log-periodicity remains **unresolved**.

Further depth will not be treated as a detection unless (i)+(ii) pass on a window declared before looking at \(A(\tau)\).

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```
