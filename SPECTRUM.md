# Combinatorial gasket Laplacian spectrum

**Sweep:** 159d  
**Operator:** graph Laplacian \(L=D-A\) on the finest-only gasket.  
**Not** the Poisson tilt diagnostic. **Not** thrust. **Not** LDOS.

Matches `gasket_graph.py` invariants: \(\lambda_{\max}=6\) for \(n\ge 2\),
\(\mathrm{Tr} L=2E=6\cdot 3^n\).

## Free spectrum (Neumann / whole graph)

One zero eigenvalue at every level (constants).

| \(n\) | \(N\) | \(\lambda_{\max}\) | \(\mathrm{Tr} L\) | \(\mathrm{Tr} L^2\) | mult(\(\lambda=6\)) |
|------:|------:|-------------------:|------------------:|--------------------:|---------------------:|
| 0 | 3 | 3 | 6 | 18 | 0 |
| 1 | 6 | 5.302776 | 18 | 78 | 0 |
| 2 | 15 | 6 | 54 | 258 | 3 |
| 3 | 42 | 6 | 162 | 798 | 12 |
| 4 | 123 | 6 | 486 | 2418 | 39 |
| 5 | 366 | 6 | 1458 | 7278 | 120 |

For \(n\ge 2\),

$$
\mathrm{mult}(\lambda=6)=\frac{3}{2}(3^{n-1}-1).
$$

These are localized high-frequency modes on small cells. They are exceptional
for spectral decimation: they are not preimages under \(z\mapsto z(5-z)\).

Exceptional values present (multiplicities):

| \(n\) | 3 | 5 | 6 |
|------:|--:|--:|--:|
| 2 | 0 | 2 | 3 |
| 3 | 3 | 4 | 12 |
| 4 | 12 | 13 | 39 |
| 5 | 39 | 40 | 120 |

## Dirichlet spectrum (corners grounded)

| \(n\) | dim | \(\lambda_{\min}\) | \(\lambda_{\min}(n)/\lambda_{\min}(n-1)\) |
|------:|----:|-------------------:|------------------------------------------:|
| 1 | 3 | 2 | — |
| 2 | 12 | 0.438447 | 0.219 |
| 3 | 39 | 0.089284 | 0.204 |
| 4 | 120 | 0.017921 | 0.201 |
| 5 | 363 | 0.003587 | 0.200 |

$$
\frac{\lambda_{\min}(L_n^{D})}{\lambda_{\min}(L_{n-1}^{D})}\ \to\ \frac{1}{5}.
$$

This is the discrete spectral-decimation scaling of the bottom of the
Dirichlet spectrum. It is **not** the Kigami energy factor \(3/5\) and
**not** the \(F\)-growth sequence \(2.80,2.57,2.48\).

Renormalized operator \((5/3)^n L_n\) would make the ground state sit near a
constant; that is a different normalization than raw \(L_n\).

## Decimation map (partial)

The quadratic \(R(z)=z(5-z)\) (and its inverse branches
\((5\pm\sqrt{25-4z})/2\)) accounts for a *proper subset* of the spectrum.
Hit rates of a single closed-form map on the whole free spectrum stay in
roughly \(0.4\)–\(0.7\) because of the exceptional localized eigenvalues
above. Do not claim a 100% one-line map on raw `eigvalsh` output.

## What this does not imply

- Spectral dimension \(d_s=2\ln 3/\ln 5\approx 1.365\) is a literature limit
  theorem for the continuum gasket Laplacian. Five finite graphs do not
  prove a Weyl law here.
- Eigenvalues of \(L\) are not print-skew angles and not Ware couplings.
- Dirichlet \(\lambda_{\min}\sim 5^{-n}\) does not restore \(K_n\) as an
  angle meter.

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
```
