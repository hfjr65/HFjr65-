# Boids Swarm Visualization

High-performance collective behavior simulation using efficient spatial partitioning.

## Quick Start

```bash
python swarm.py
```

## Parameters

### System Size
- **N_PARTICLES**: Number of particles (600 default, try 500-1000)
- **BOX_SIZE**: Size of simulation domain (25.0 default)
- **SPEED**: Velocity magnitude (0.12 default)

### Interaction Radii
- **R_REPULSION**: Separation distance threshold (0.6)
- **R_ALIGNMENT**: Alignment/orientation radius (2.0)
- **R_ATTRACTION**: Cohesion/attraction radius (4.0)

### Behavior Weights
- **W_REPULSION**: Separation force strength (1.5)
- **W_ALIGNMENT**: Alignment force strength (1.0)
- **W_ATTRACTION**: Cohesion force strength (0.5)
- **NOISE**: Random perturbation (0.15)

## Features

✅ **Efficient neighbor search** using scipy's cKDTree  
✅ **Toroidal topology** with periodic boundary conditions  
✅ **Real-time visualization** with order parameter tracking  
✅ **Export to MP4 or GIF**  
✅ **Fully customizable parameters**  

## Performance

- 600 particles: ~25-30 fps
- 1000 particles: ~15-20 fps

## Visualization

**Left panel**: Swarm animation (color = heading angle, HSV colormap)  
**Right panel**: Macroscopic order parameter (polar alignment) vs. time

## Export

To save animation, set in swarm.py:

```python
SAVE_ANIMATION = True
FILE_FORMAT = 'mp4'  # or 'gif'
```

MP4 requires ffmpeg installed on your system.
