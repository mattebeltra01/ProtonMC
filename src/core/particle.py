import numpy as np

class Particle:
    def __init__(self, position, direction, energy, particle_type="proton", mass=938.272, charge=1.0):
        """
        Inizializza un oggetto particella

        Parameters:
        -----------
        position : array-like
            Posizione iniziale [x, y, z] in mm
        direction : array-like
            Direzione iniziale [dx, dy, dz]
        energy : float
            Energia cinetica iniziale in MeV
        particle_type : str
            Tipo di particella (default: "proton")
        mass : float
            Massa della particella in MeV/c²
        charge : float
            Carica della particella in unità di carica elementare
        """
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        self.energy = float(energy)
        self.type = particle_type
        self.mass = float(mass)
        self.charge = float(charge)
        self.alive = True

        # Inizializza la traccia con la posizione iniziale
        self.track = [self.position.copy()]

        # Energia depositata
        self.deposited_energy = 0.0

    def move(self, step_size):
        """
        Muove la particella nella sua direzione attuale

        Parameters:
        -----------
        step_size : float
            Dimensione del passo in mm
        """
        # Calcola lo spostamento
        displacement = self.direction * step_size

        # Aggiorna la posizione
        self.position = self.position + displacement

        # Aggiungi il nuovo punto alla traccia
        self.track.append(self.position.copy())

    def deposit_energy(self, energy):
        """
        Deposita energia, riducendo l'energia della particella

        Parameters:
        -----------
        energy : float
            Energia da depositare in MeV
        """
        # Limita all'energia disponibile
        energy = min(energy, self.energy)

        # Aggiorna energie
        self.energy -= energy
        self.deposited_energy += energy

    def get_momentum(self):
        """
        Calcola il momento della particella

        Returns:
        --------
        momentum : float
            Momento in MeV/c
        """
        return np.sqrt(self.energy * (self.energy + 2 * self.mass))

    def get_beta(self):
        """
        Calcola il fattore beta (v/c) della particella

        Returns:
        --------
        beta : float
            Fattore beta
        """
        return np.sqrt(1 - 1 / (1 + self.energy / self.mass)**2)
