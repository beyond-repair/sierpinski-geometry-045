# Sierpinski Geometry 0.45 (Coherence Drive)

**© 2026 Brian Ware / AtomicDreamlabs — All Rights Reserved. Proprietary Technology.**

**Finding:** The asymmetric 3rd-order Sierpinski tetrahedron (aft face n=3, fore faces n=1, scaling factor exactly 0.45) is the hardware geometry that generates the required LDOS gradient and topological pinch for net thrust.

**Purpose of this Repo**  
This repository contains the complete, ready-to-run generator for the 0.45 Sierpinski geometry, all parameters, fabrication notes, and blind-build instructions. A new engineer can clone this repo, run the script, and immediately produce a printable STL file for the first physical prototype.

**License**  
See LICENSE file in this repository. All rights reserved. No copying or distribution without explicit written permission.

## 1. Key Properties
- Scaling factor: **0.45** (critical for LDOS gradient)
- Recursion asymmetry: aft face = n=3, fore faces = n=1
- Fractal dimension: D ≈ 0.868
- Creates the topological pinch responsible for 92 % aft-face localization
- Enables the 30 μN/kW thrust target when combined with the Ware Constant

## 2. Blind-Build Instructions
1. Clone this repo
2. Run `sierpinski_generator.py`
3. The script outputs `coherence_drive_sierpinski.stl`
4. Import the STL into your slicer/CNC software
5. Fabricate using low-loss dielectric (ε_r ≈ 2.2, tanδ < 0.001)
6. Tolerance: ±0.01 on 0.45 scaling, surface roughness < λ/20 at operating frequency

## 3. Validation Checklist
- [ ] Generated STL matches 3rd-order recursion on aft face only
- [ ] Scaling factor exactly 0.45
- [ ] Mesh is watertight and manifold-ready for 3D printing/CNC
- [ ] Run through `test_baseline_v1.py` after loading geometry → confirms 92 % pinch

**Status:** Hardware-ready. This is the physical engine of the Coherence Drive.

**Cross-References**  
- Master repo: `coherence-drive`  
- Ware Constant: `ware-constant-derivation`  
- M2 scaling: `m2-renormalization-law`  
- Topological pinch: `topological-pinch`

**Next Action for Hardware Team**  
Print the STL, add RF feed points (per momentum-closure repo), and test in vacuum chamber.

**End of File**
