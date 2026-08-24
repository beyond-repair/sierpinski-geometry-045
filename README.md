<div align="center">

# Sierpinski Geometry · 0.45

### The **shape** the rest of the stack talks about — not the force

[![RESEARCH](https://img.shields.io/badge/geometry_only-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)

</div>

---

## Why this exists

Field solvers need a mesh. Theory needs a fixed scale ratio.  
**0.45** is the locked geometric scale factor for asymmetric aft/fore recursive (Sierpinski-type) structure used across the Coherence Drive research line.

## Why you need it

| You… | Open this |
|------|-----------|
| Run BEM / surface integrals | Generate STL / mesh inputs |
| Quote “0.45 asymmetry” | Share one generator, not hand-waved CAD |
| Claim thrust from geometry alone | **Don’t** — this repo is shape only |

## How it works

```bash
python sierpinski_generator.py --info --n-aft 3 --n-fore 1
python sierpinski_generator.py --stl out.stl
```

- \(\alpha = 0.45\) exact scale ratio  
- Asymmetric aft/fore recursion depths configurable  
- **No** field solve, **no** force claim, **no** energy claim

## Downstream / upstream

- Solvers: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)  
- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)  
- Math: [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)
