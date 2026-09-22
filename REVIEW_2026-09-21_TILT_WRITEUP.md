# Review — geometric-tilt writeup (2026-09-21)

**Claim level:** 1  
**Does not raise thrust flags. Does not unfreeze Stage 1.**

Subject: the Layer-C note on hierarchical / sheared gasket diagnostics
(conductance vs geometric vs combinatorial weights).

## Accepted (deterministic, this operator family)

1. Graph Poisson with grounded corners and unit interior load is the
   published diagnostic, not Maxwell stress.
2. Finest-only gasket: \(N_g=(3^{g+1}+3)/2\), \(E_g=3^{g+1}\).
3. Combinatorial \(\gamma=0\) is metric-blind under this flux definition.
4. Small-shear linear response is odd in \(\theta\). \(0.45^\circ\) is inside
   the linear window and is not a peak.
5. At fixed generation, first-order response satisfies
   \(\|F\|(\gamma)\propto\gamma\) for power weights \(w=\ell^{-\gamma}\).
   Independently recomputed at level 2, \(\theta=0.45^\circ\):

   | \(\gamma\) | \(\|F\|\) | \(\|F\|/\gamma\) |
   |----------:|----------:|----------------:|
   | 0.5 | \(1.836427\times10^{-3}\) | \(3.67285\times10^{-3}\) |
   | 1.0 | \(3.672846\times10^{-3}\) | \(3.67285\times10^{-3}\) |
   | 2.0 | \(7.345633\times10^{-3}\) | \(3.67282\times10^{-3}\) |
   | 3.0 | \(1.101830\times10^{-2}\) | \(3.67277\times10^{-3}\) |

   Hence \(\|F\|_{\gamma=2}/\|F\|_{\gamma=1}=1.99998\) at level 2 and
   \(1.999999\) at level 5. The factor of two is the linear-response
   identity \(F\propto\gamma\) on an equal-rest-length graph, not a new
   physical law and not a proof that frozen tables were “wrong physics.”
   They were different \(\gamma\).

## Rejected

1. **Kigami \(r=3/5\) governs \(\|F\|\) growth.**  
   Observed \(\|F\|_{g+1}/\|F\|_g \approx 2.800,\,2.571,\,2.480\).
   \(5/3\approx 1.667\) does not match. Kigami renormalization is for
   harmonic energy with *fixed boundary values*, not Poisson with a
   unit load per vertex. Different problem.

2. **\(\|F\|/N\) has converged to a continuous limit.**  
   Cond, \(\theta=0.45^\circ\): \(\|F\|/N = 2.449,\,2.449,\,2.150,\,1.792\times 10^{-4}\)
   at \(g=2..5\). A 27% drop from \(g=3\) to \(g=5\) is not a tight envelope.

3. **\(K_g=\theta/\|F\|_g\) yields a resolution-invariant print angle.**  
   Using \(K_4\) on other generations returns
   \(\Theta_{\mathrm{diag}}/\theta \approx 0.139,\,0.389,\,1,\,2.48\)
   at \(g=2,3,4,5\). Errors 86% and 148%.  
   If \(K_g\) is taken from the *same* generation that produced \(\|F\|\),
   then \(\Theta_{\mathrm{diag}}\equiv\theta\) by algebra. That is a
   tautology, not a measurement.

4. **Wheatstone-gasket current difference as a derived tensor law.**  
   Qualitative picture only. Not needed for the locked numbers and not
   a continuum constitutive statement.

5. **Any promotion of \(F\) to thrust, LDOS, or Stage-2 residual force.**

## Software implication

Lock \(\gamma\) explicitly (1 = printed-trace conductance, 2 = Sweep-138
geometric weights). Do not introduce per-generation \(K_g\) as an angle
estimator. Report \(\|F\|\), \(\|F\|/\theta_{\rm rad}\), and generation.

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```
