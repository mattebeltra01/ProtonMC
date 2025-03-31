import numpy as np

class Particle:
    def __init__(self, position, direction, energy):
        """
        Initialize a particle with position, direction, and energy.

        Args:
            position (np.ndarray): 3D position vector [x, y, z] in mm
            direction (np.ndarray): 3D direction vector (normalized)
            energy (float): Particle energy in MeV
        """
        self.position = np.array(position, dtype=float)
        self.direction = self._normalize(np.array(direction, dtype=float))
        self.energy = float(energy)
        self.alive = True
        self.track = [self.position.copy()]

    def _normalize(self, vector):
        """Normalize a vector."""
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise ValueError("Direction vector cannot be zero")
        return vector / norm

    def move(self, step_size):
        """
        Move particle by step_size in current direction.

        Args:
            step_size (float): Distance to move in mm
        """
        self.position += self.direction * step_size
        self.track.append(self.position.copy())

    def deposit_energy(self, energy):
        """
        Deposit energy and check if particle should be terminated.

        Args:
            energy (float): Energy to deposit in MeV
        """
        self.energy -= energy
        if self.energy <= 0:
            self.alive = False
            self.energy = 0
