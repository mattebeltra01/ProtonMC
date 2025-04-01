# ProtonMC

A Monte Carlo simulator for proton interactions in Python, designed to model and analyze particle physics phenomena.

## Overview

ProtonMC simulates proton interactions with matter, providing tools for:

- Particle tracking in 3D space
- Energy deposition calculation using Bethe-Bloch formula
- Multiple Coulomb scattering simulation
- Material definition and properties
- Visualization of trajectories and Bragg curves

## Project Structure

ProtonMC/
├── src/
│   ├── core/
│   │   ├── simulator.py     # Main simulation engine
│   │   ├── particle.py      # Particle class definition
│   │   └── materials.py     # Material properties
│   └── utils/
│       └── visualization.py # Visualization tools
├── examples/
│   └── simple_simulation.py # Example simulation
├── tests/                   # Test files
├── docs/                    # Documentation
└── data/                    # Data files and resources

## Getting Started

### Prerequisites

- Python 3.x
- NumPy
- Matplotlib

pip install numpy matplotlib

### Installation

1. Clone the repository:
      git clone https://github.com/mattebeltra01/ProtonMC.git
   ```

2. Navigate to project directory:
   ```bash
   cd ProtonMC
   ```

### Usage

Basic simulation example:
python
from src.core.simulator import ProtonSimulator
from src.utils.visualization import plot_trajectory_3d, plot_bragg_curve

# Create a water simulator
simulator = ProtonSimulator(material_density=1.0)  # g/cm³

# Create a 100 MeV proton
proton = simulator.create_proton(
    position=[0, 0, 0],    # starting position (mm)
    direction=[0, 0, 1],   # direction along z-axis
    energy=100.0           # initial energy (MeV)
)

# Run simulation
depths = []
energy_losses = []
for i in range(1000):
    depth = proton.position[2]
    energy_loss = simulator._calculate_energy_loss(proton.energy)
    
    depths.append(depth)
    energy_losses.append(energy_loss)
    
    if not simulator.step(proton, step_size=0.1):
        break

# Visualize results
plot_trajectory_3d([proton], save_path="trajectory_3d.png")
plot_bragg_curve(depths, energy_losses, save_path="bragg_curve.png")
```

## Features Implemented

- [x] 3D particle tracking with position and direction
- [x] Energy loss calculations using Bethe-Bloch approximation
- [x] Multiple Coulomb scattering using Highland formula
- [x] Basic material definitions with customizable properties
- [x] Visualization tools for trajectories and Bragg curves

## Features in Development

- [ ] Nuclear interactions
- [ ] Voxelized geometry support
- [ ] Dose calculation
- [ ] Parallelized simulation
- [ ] Expanded material database

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project maintained by Matteo Beltrami

GitHub: [@mattebeltra01](https://github.com/mattebeltra01)
