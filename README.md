# HFjr65™ — Computational Physics & Visualization Pipeline

This repository contains two major computational/visualization projects:

## 1. Holographic Lattice Pipeline
**Emergent Bulk Geometry and Einstein–RG Correspondence from Lattice Entanglement**

A complete, self-contained Python numerical pipeline that reconstructs an emergent radial bulk geometry from the entanglement entropy of one-dimensional free fermionic lattice models (Ising and Kitaev chains).

### Features
- Exact Bogoliubov–de Gennes (BdG) diagonalisation
- Von Neumann entropy computation
- Direct Ryu–Takayanagi (RT) formula inversion
- Bootstrap uncertainty propagation
- Correlation length extraction & numerical beta function
- Ricci scalar & holonomy integral computation

### Quick Start
```bash
python holographic_pipeline/pipeline.py
```

### Requirements
- Python 3.8+
- NumPy, SciPy, Matplotlib

---

## 2. Boids Swarm Visualization
**High-Performance Collective Behavior Simulation**

A fast, scalable Boids swarm simulation using `cKDTree` for efficient neighbor searches. Supports up to 1000+ particles with real-time visualization.

### Features
- **Efficient spatial partitioning** using scipy's cKDTree (O(log N) neighbor search)
- **Three fundamental rules**: Separation (repulsion), Alignment, Cohesion (attraction)
- **Real-time visualization** with order parameter tracking
- **Periodic boundary conditions** (toroidal topology)
- **Export options**: MP4 or GIF animation
- **Customizable parameters**: particle count, speeds, interaction radii, weights

### Quick Start
```bash
python boids/swarm.py
```

To save animation:
```python
SAVE_ANIMATION = True
FILE_FORMAT = 'mp4'  # or 'gif'
```

### Parameters
```python
N_PARTICLES = 600              # Number of particles (try 500-1000)
BOX_SIZE = 25.0                # Simulation domain size
SPEED = 0.12                   # Particle velocity

R_REPULSION = 0.6              # Separation radius
R_ALIGNMENT = 2.0              # Alignment radius (Vicsek)
R_ATTRACTION = 4.0             # Cohesion radius

W_REPULSION = 1.5              # Separation weight
W_ALIGNMENT = 1.0              # Alignment weight
W_ATTRACTION = 0.5             # Cohesion weight
NOISE = 0.15                   # Random perturbation
```

### Performance
- **600 particles**: ~25-30 fps (real-time)
- **1000 particles**: ~15-20 fps (smooth)
- Uses **vectorized NumPy operations** and **cKDTree** for maximum efficiency

### Visualization
- Left panel: Swarm animation (color-coded by heading angle, HSV colormap)
- Right panel: Macroscopic order parameter history (polar alignment)

### Export Options
- **MP4**: Requires ffmpeg (`pip install ffmpeg-python` + system ffmpeg)
- **GIF**: Requires pillow (`pip install pillow`)

---

## Installation

```bash
git clone https://github.com/hfjr65/HFjr65-.git
cd HFjr65-
pip install -r requirements.txt
```

## Usage

### Run Holographic Pipeline
```bash
python holographic_pipeline/pipeline.py
```

Output files:
- `holographic_pipeline_results.png` — Six-panel analysis figure

### Run Boids Swarm
```bash
python boids/swarm.py
```

### Run Stress Tests
```bash
pip install psutil
python stress_test.py
```

---

## Stress Test Suite

Comprehensive performance and stability testing:
- **Particle count scaling** (100-5000 particles)
- **Interaction radius sensitivity**
- **cKDTree vs naive algorithm comparison**
- **Long-run stability test** (500 frames)
- **Memory leak detection**

Outputs visual report: `stress_test_results.png`

---

## Citation & License

Both projects are released under the **MIT License**.

If you use or build upon this code, please reference:
- **Holographic Pipeline**: HFjr65™, "Emergent Bulk Geometry, Holonomy and Einstein–RG Correspondence from Entanglement in Free Fermionic Chains" (2026)
- **Boids Swarm**: HFjr65™ Collective Behavior Simulation Suite (2026)
- **Stress Tests**: HFjr65™ Performance Analysis Suite (2026)

---

## Author

**Håkon Fløstad Jr. (HFjr65™)**

GitHub: [@hfjr65](https://github.com/hfjr65)
