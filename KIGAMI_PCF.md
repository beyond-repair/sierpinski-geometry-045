# PCF gasket, resistance form, and why 5/3 is not F-growth

**Sweep:** 159c  
**Claim level:** 1  
**Not thrust. Not Stage 2.**

## 1. What a PCF fractal is here

The finite gasket graphs \(G_n=(V_n,E_n)\) with identified corners \(V_0=\{c_0,c_1,c_2\}\)
are the standard discrete approximations to the Sierpiński gasket, which is
post-critically finite: the critical set is finite (three points).

Kigami’s harmonic structure is a pair (energy on \(V_0\), renormalization
constant) such that harmonic extension from \(V_n\) to \(V_{n+1}\) is compatible.

## 2. Executed identities on this graph (combinatorial unit edge weights)

Harmonic energy with boundary data \((1,0,0)\) and finest-edge weight 1:

| \(n\) | \(\mathcal{E}_n\) | \(\mathcal{E}_n/\mathcal{E}_{n-1}\) |
|------:|------------------:|-----------------------------------:|
| 0 | 2 | — |
| 1 | 1.2 | **3/5** |
| 2 | 0.72 | **3/5** |
| 3 | 0.432 | **3/5** |
| 4 | 0.2592 | **3/5** |
| 5 | 0.15552 | **3/5** |

Effective resistance between two corners (third floating, unit current):

| \(n\) | \(R_n(c_0,c_1)\) | \(R_n/R_{n-1}\) |
|------:|-----------------:|----------------:|
| 0 | 2/3 | — |
| 1 | 10/9 | **5/3** |
| 2 | 50/27 | **5/3** |
| 3 | 250/81 | **5/3** |
| 4 | 1250/243 | **5/3** |
| 5 | 6250/729 | **5/3** |

These are the Kigami numbers for *this* problem: fixed boundary values,
combinatorial edges, no shear required.

Energy falling by 3/5 and resistance rising by 5/3 are the same fact:
finer graphs with unit edge resistance add series path, so corner-to-corner
resistance grows; the Dirichlet form on the un-rescaled graph therefore
shrinks.

## 3. Continuum-compatible Poisson (not our print-skew default)

Renormalized Laplacian \(L_n^{\mathrm{ren}}=(5/3)^n L_n^{\mathrm{combo}}\)
with self-similar load \(3^{-n}\) on each interior vertex:

| \(n\) | \(\max|u|\) | \(\mathcal{E}_{\mathrm{ren}}\) |
|------:|------------:|-------------------------------:|
| 1 | 0.100000 | 0.10000 |
| 2 | 0.100000 | 0.12000 |
| 3 | 0.100000 | 0.12400 |
| 4 | 0.100000 | 0.12480 |
| 5 | 0.100000 | 0.12496 |

\(\max|u|\) is exactly 1/10 at every computed level. Renormalized energy
is approaching 1/8. That is a discrete Poisson problem *on the resistance
form*. It is not the Sweep-138/159 diagnostic.

## 4. Corrected claims

**Kigami.**  
Use 3/5 (energy) and 5/3 (resistance) only for harmonic extension /
effective resistance on the combinatorial gasket. Do **not** attach them
to \(\|F\|\) from unit-per-vertex Poisson plus metric weights. Observed
\(\|F\|_{n+1}/\|F\|_n\approx 2.80,\,2.57,\,2.48\) is a different sequence.

**\(K_n=\theta/\|F\|_n\).**  
Forbidden as a multi-generation angle meter. Applying \(K_4\) to other
\(n\) yields relative errors 86%, 61%, 0%, 148% at \(n=2,3,4,5\).
Same-generation \(K_n\|F\|_n\equiv\theta\) is an identity.

**Metric blindness.**  
\(\gamma=0\) remains \(F=0\) after \((5/3)^n\) rescaling and after switching
to measure load. Renormalization is a global factor. Combinatorial \(L\)
still does not see shear.

**Measure-normalized conductance tilt (exploratory, not locked).**  
\(\gamma=1\), load \(3^{-n}\), \(\theta=0.45^\circ\):
\(\|F\|=4.081,\,3.809,\,3.265,\,2.699\times10^{-4}\) at \(n=2..5\).
Smaller and slowly decreasing. Not certified as a continuum limit.

## 5. Allowed next PCF derivation

Only this would connect resistance forms to the tilt sensor without
smuggling \(K_n\):

1. Fix the harmonic structure (combo edges, factor 5/3).
2. Put metric dependence in a *perturbation of that structure*, not in a
   replacement Laplacian with per-vertex load.
3. Prove, or disprove, existence of \(\lim_n F_n[\mu,\theta]/\theta\).

Until that limit is shown, report \((n,\gamma,\|F\|,\|F\|/\theta)\).
