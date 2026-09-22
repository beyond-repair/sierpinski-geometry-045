# Findings 2026-09-21 — conductance, hierarchical buses, shear sensitivity

**Sweep:** 159  
**Classification:** RESEARCH / claim level 1  
**Does not claim LDOS, thrust, or energy extraction.**  
**Does not unfreeze** [coherence-drive Stage 1](https://github.com/beyond-repair/coherence-drive/blob/main/docs/MATH_THEORY_CLOSURE.md).

Reproduction:

```bash
python3 conductance_shear.py
pytest -q test_conductance_shear.py test_gasket_flux_audit.py
```

## 1. Operators

On the finest-only gasket, edge weight

$$
G_{ij}=\sigma w_{ij}/\ell_{ij}(\theta)
$$

with three controls:

| name | weight |
|------|--------|
| combo | \(G=1\) |
| cond | \(G=1/\ell\) (constant-section printed trace) |
| geom | \(G=1/\ell^2\) (Sweep-138 lock) |

Shear map (print skew): connectivity fixed, \(x\leftarrow x+y\tan\theta\).  
Load: Dirichlet 0 on three corners, unit source on every interior vertex.  
Flux: graph diagnostic \(F=\sum_c I_c(x_c-\bar x)\). **Not** \(\oint T\cdot n\,dA\).

## 2. Locked numbers (finest gasket)

### Global width invariance (cond, fixed vertex load, level 3, \(\theta=0.45^\circ\))

\(w\in\{0.25,1,4\}\) leaves \(\|F\|=1.028398\times 10^{-2}\) and \(\sum|I_c|=39\) unchanged. Voltages scale as \(1/w\).  
A uniformly skinnier high-\(n\) print does **not** change this diagnostic.

### Linear gain at level 2

| operator | \(\|F\|(0.45^\circ)\) | \(\|F\|/\theta_{\rm rad}\) |
|----------|----------------------:|--------------------------:|
| combo | \(\sim 10^{-15}\) | 0 |
| cond | \(3.67285\times 10^{-3}\) | \(0.46764\) |
| geom | \(7.34563\times 10^{-3}\) | \(0.93527\) (Sweep-138) |

Self-similar traces \(w\propto\ell\) (\(\beta=1\)) recover combo and **kill** the sensor.

### Level scan, cond, \(\theta=0.45^\circ\)

| lv | \(N\) | \(\|F\|\) | \(\|F\|/N\) |
|---:|------:|----------:|------------:|
| 2 | 15 | \(3.673\times 10^{-3}\) | \(2.449\times 10^{-4}\) |
| 3 | 42 | \(1.028\times 10^{-2}\) | \(2.449\times 10^{-4}\) |
| 4 | 123 | \(2.644\times 10^{-2}\) | \(2.150\times 10^{-4}\) |
| 5 | 366 | \(6.558\times 10^{-2}\) | \(1.792\times 10^{-4}\) |

Raw \(\|F\|\) is extensive. Do not quote \(0.468\,\mathrm{rad}^{-1}\) as a material constant.

## 3. Hierarchical buses

Coarse triangle sides are retained. \(w(g)=r^g\).

- Generation-0 corner-to-corner sides carry **zero** current (both ends Dirichlet 0).
- \(r=0.5\) (finer thinner) raises \(\|F\|\) modestly; \(r=2\) lowers it (shunt).
- Level 4, \(\theta=0.45^\circ\): \(\|F\|(r=0.5)/\|F\|(r=1)\approx 1.14\). Not an amplifier class.
- Dropping the finest generation makes \(L_{\rm int}\) singular. Coarse buses are not a standalone sensor.
- Hierarchical / finest-only ratio at \(r=1\): 1.076 (lv2), 1.168 (lv3), 1.276 (lv4).

## 4. Shear sensitivity

Jacobian at the identity, level 2, cond:

$$
\left.\partial F/\partial\theta\right|_{0}
=
\begin{cases}
(-0.467654,\,0) & x\text{-shear or }y\text{-shear}\\
(0,\,+0.467654) & y\text{-uniaxial scale}\\
(0,\,0) & \text{rigid rotation or isotropic scale.}
\end{cases}
$$

- Linear channel is odd in \(\theta\). Even remainder is \(O(\theta^2)\).
- \(F_x=c\theta\) to four digits through \(\sim 2^\circ\); 0.45° is inside that window.
- \(\mathrm{cond}(L_{\rm int})\) at lv2: 13.69 (0°) to 13.70 (0.45°). Small skew does not ill-condition the solve.

## 5. Forbidden readings

- Scaling this \(F\) into newtons or into \(\Delta F=W\chi\mathcal{G}\).
- Calling 0.45° or \(r=0.45\) a critical value.
- Treating combo-blindness as “no print defect” on a real resistor network (use cond).
- Fitting \(\beta\) or \(r\) after seeing \(\|F\|\).

## 6. Status words

```
claim_class                 = geometry_diagnostic
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
stage1_freeze               = untouched
```
