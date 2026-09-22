# Log-periodic oscillations — search on this gasket

**Date:** 2026-09-22  
**Status:** Expected by DSI; **not measured** at levels \(n\le 5\).

Companion: [HEAT_KERNEL.md](HEAT_KERNEL.md).

## 1. What the literature requires

On the infinite gasket the killed/free heat kernel admits the form

$$
Z(\tau)=\tau^{-d_s/2}\,\psi(\log\tau),
\qquad
\psi(\theta+\log 5)=\psi(\theta),
$$

with \(d_s=2\log 3/\log 5\). The period in logarithmic time is

$$
T_{\log}=\log 5\approx 1.609438
$$

because Kigami time rescales by \(5\) under one graph refinement. This is discrete scale invariance of the *limit* object, not a theorem about \(Z_n(\tau)\) at \(n\le 5\).

## 2. What was computed

Dirichlet traces \(Z_n(\tau)=\mathrm{Tr}\exp(-\tau 5^n L_n^D)\) on a fine log-grid, \(n=4,5\).

Amplitude proxy \(A(\tau)=Z(\tau)\,\tau^{d_s/2}\) is **not** constant on any window that includes the spectral-gap tail (\(\lambda_1^D\approx 11.21\)). Global power-law fits over \(\tau\in[10^{-2.2},10^{-0.15}]\) give slope \(\approx -1.66\), not \(-d_s/2\approx -0.683\). FFT peaks of those residuals are dominated by the **window length** (\(\approx 4.82\) in log-\(\tau\)) and its harmonics.

A bin at period \(1.6069\) vs \(\log 5=1.6094\) appears as the *third* harmonic of that window. It is not a detection.

Restricted short-time windows:

| window | log-span | fit slope | amp rel. std |
|--------|----------|-----------|--------------|
| \([0.004,0.020]\) | \(1.609=\log 5\) | \(-0.768\) | 0.041 |
| \([0.006,0.040]\) | 1.90 | \(-0.821\) | 0.077 |
| \([0.010,0.080]\) | 2.08 | \(-0.923\) | 0.143 |

The first window has log-span exactly \(\log 5\), so an FFT peak at \(\log 5\) is automatic. Relative oscillation of \(A(\tau)\) is only 4% there and is a smooth drift (slope still \(-0.77\), not \(-0.68\)), not a resolved periodic \(\psi\).

Weyl counting \(N(\Lambda)=\#\{5^n\lambda_k^D<\Lambda\}\) at \(n=5\) has slope \(0.72\) vs \(d_s/2=0.68\). Residual std \(0.14\) in \(\log N\) is not a period measurement.

## 3. Claim status

| Claim | Status |
|-------|--------|
| DSI period \(\log 5\) in the *continuum* kernel | Literature / hypothesis for the limit object |
| Period measured on these graphs | **Not established** |
| Amplitude / phase of \(\psi\) | Unknown |
| Log-periodic factor as \(W_\star\) or thrust | Forbidden |

Freeze line “log-periodic amplitude on a heat kernel” remains **unresolved**.

## 4. What would count as a measurement

1. A window where the fitted slope is within a few percent of \(-d_s/2\).  
2. At least two full periods of \(\log 5\) inside that window.  
3. The same phase of \(A(\tau)\tau^{0}\) at levels \(n\) and \(n+1\) after the time map \(\tau\mapsto 5\tau\).  
4. Pre-registered: no fitting of the oscillation to \(0.08\).

Level 5 does not meet (1)+(2) simultaneously.

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```
