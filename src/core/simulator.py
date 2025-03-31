from .particle import Particle
import numpy as np

class ProtonSimulator:
    def __init__(self, material_density=1.0):
        """
        Initialize the proton simulator.

        Args:
            material_density (float): Density of material in g/cm³
        """
        self.material_density = material_density
        self.particles = []

    def create_proton(self, position, direction, energy):
        """
        Create a new proton and add it to simulation.

        Args:
            position (list): Initial position [x, y, z]
            direction (list): Initial direction vector
            energy (float): Initial energy in MeV
        """
        proton = Particle(position, direction, energy)
        self.particles.append(proton)
        return proton

    def step(self, particle, step_size=0.1):
        """
        Perform one simulation step for a particle.

        Args:
            particle (Particle): Particle to simulate
            step_size (float): Step size in mm
        """
        if not particle.alive:
            return

        # Simple energy loss model (Bethe-Bloch approximation)
        # This is a very simplified model for now
        energy_loss = self._calculate_energy_loss(particle.energy) * step_size
        particle.deposit_energy(energy_loss)
        particle.move(step_size)

    def _calculate_energy_loss(self, energy):
        """
        Simplified energy loss calculation.

        Args:
            energy (float): Current particle energy in MeV

        Returns:
            float: Energy loss per mm
        """
        # Simplified constant energy loss (will be improved later)
        return 0.2 * self.material_density  # MeV/mm
