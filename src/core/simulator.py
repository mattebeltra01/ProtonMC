import numpy as np
from .particle import Particle

class ProtonSimulator:
    def __init__(self, material=None, material_density=1.0):
        # Permetti di passare un oggetto Material o specificare solo la densità
        if material is not None:
            self.material = material
        else:
            # Usa il Material di default (acqua) se solo la densità è specificata
            from .materials import materials
            self.material = materials["water"]
            self.material.density = material_density

    def create_proton(self, position, direction, energy):
        """
        Crea un oggetto Particle rappresentante un protone

        Parameters:
        -----------
        position : list o array
            Posizione iniziale [x, y, z] in mm
        direction : list o array
            Direzione iniziale [dx, dy, dz] (verrà normalizzata)
        energy : float
            Energia iniziale in MeV

        Returns:
        --------
        particle : Particle
            Oggetto particella configurato come protone
        """
        # Converti in array numpy
        position = np.array(position, dtype=float)
        direction = np.array(direction, dtype=float)

        # Normalizza la direzione
        dir_norm = np.linalg.norm(direction)
        if dir_norm > 0:
            direction = direction / dir_norm

        # Crea e restituisci il protone
        proton = Particle(
            position=position,
            direction=direction,
            energy=energy,
            particle_type="proton",
            mass=938.272,  # Massa del protone in MeV/c²
            charge=1.0     # Carica del protone in unità e
        )

        return proton

    def _calculate_energy_loss(self, energy):
        """Implementa una formula Bethe-Bloch semplificata"""
        # Costanti fisiche
        K = 0.307075  # MeV cm²/g
        z = 1         # carica del protone

        # Ottieni parametri dal materiale
        Z_A = self.material.Z_A_ratio
        I = self.material.I  # potenziale di ionizzazione (eV)

        # Formula semplificata di Bethe-Bloch
        beta_squared = 1 - (1 / (1 + energy/938.272)**2)
        stopping_power = K * Z_A * (z**2 / beta_squared) * (np.log(2*938.272*beta_squared*energy/I) - beta_squared)

        return stopping_power * self.material.density  # MeV/mm

    def _apply_scattering(self, particle, step_size):
        """Applica scattering Coulombiano multiplo"""
        # Parametri di scattering
        X0 = self.material.radiation_length  # Lunghezza di radiazione (cm)

        # Formula di Highland per l'angolo RMS di scattering
        p = np.sqrt(particle.energy * (particle.energy + 2*938.272))  # momento in MeV/c
        step_rad_lengths = (step_size/10) / X0  # conversione da mm a cm
        theta_0 = 13.6 / p * np.sqrt(step_rad_lengths) * (1 + 0.038 * np.log(step_rad_lengths))

        # Applica deviazione random
        phi = 2 * np.pi * np.random.random()
        theta = np.random.normal(0, theta_0)

        # Implementazione semplificata della rotazione
        # Prima converti la direzione in angoli sferici
        dir_norm = np.linalg.norm(particle.direction)
        dir_unit = np.array(particle.direction) / dir_norm

        # Calcola nuova direzione approssimata (semplificata)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        cos_phi = np.cos(phi)
        sin_phi = np.sin(phi)

        # Ruota la direzione (versione semplificata)
        new_dir = np.array([
            dir_unit[0] + sin_theta * cos_phi,
            dir_unit[1] + sin_theta * sin_phi,
            dir_unit[2] * cos_theta
        ])

        # Normalizza e aggiorna
        new_dir = new_dir / np.linalg.norm(new_dir)
        particle.direction = new_dir * dir_norm

    def step(self, particle, step_size=0.1):
        # Verifica se la particella è attiva
        if not particle.alive:
            return False

        # Calcola la perdita di energia
        energy_loss = self._calculate_energy_loss(particle.energy) * step_size

        # Limita la perdita di energia all'energia disponibile
        energy_loss = min(energy_loss, particle.energy)

        # Applica la perdita di energia
        particle.deposit_energy(energy_loss)

        # Applica lo scattering se abilitato
        self._apply_scattering(particle, step_size)

        # Muovi la particella
        particle.move(step_size)

        # Controlla se la particella ha energia residua
        if particle.energy <= 0:
            particle.alive = False
            return False

        return True
