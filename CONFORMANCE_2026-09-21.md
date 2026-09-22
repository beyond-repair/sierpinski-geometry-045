# Conformance — 2026-09-21 synthesis

**Claim level:** 1. Stage 1 freeze untouched.

The following split is **accepted**:

- Kigami 3/5 (energy) and 5/3 (two-corner resistance) apply to harmonic
  extension on the combinatorial PCF gasket. Executed: `KIGAMI_PCF.md`.
- Print-skew \(F\) solves interior Poisson with extensive load
  \(\mathbf{1}_{\mathrm{int}}\) and (for \(\gamma>0\)) metric weights.
  Its generation ratios 2.80, 2.57, 2.48 are not 5/3.
- \(N_n=(3^{n+1}+3)/2=\tfrac{3}{2}(3^n+1)\).
- \(K_n=\theta/\|F\|_n\) is generation-dependent. \(K_4\) as a universal
  angle meter is falsified (0.139, 0.389, 1, 2.48).
- \(\gamma=0\) remains metric-blind after \((5/3)^n\) rescaling.
- Linear odd response for \(|\theta|\lesssim 2^\circ\); even piece \(O(\theta^2)\).
- No coupling of this \(F\) to continuum stress or propulsion.

**Not accepted as proven:** that load \(3^{-n}\) plus \(L_n^{\mathrm{ren}}=(5/3)^n L_n^{\mathrm{combo}}\)
*has* a continuum tilt limit on SG. That pair is the correct *candidate*
problem. The limit of \(F_n[\mu,\theta]/\theta\) is unproven.
Exploratory conductance numbers under measure load still drift:
\(4.08,\,3.81,\,3.26,\,2.70\times 10^{-4}\) at \(n=2..5\), \(\theta=0.45^\circ\).

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```
