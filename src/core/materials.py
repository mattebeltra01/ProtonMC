import numpy as np

class Material:
    def __init__(self, name, density, Z_A_ratio, I, radiation_length=36.1):
        """
        Inizializza un materiale

        Parameters:
        -----------
        name : str
            Nome del materiale
        density : float
            Densità in g/cm³
        Z_A_ratio : float
            Rapporto Z/A medio del materiale
        I : float
            Potenziale medio di ionizzazione in eV
        radiation_length : float
            Lunghezza di radiazione in cm
        """
        self.name = name
        self.density = density  # g/cm³
        self.Z_A_ratio = Z_A_ratio  # Z/A
        self.I = I  # eV (potenziale medio di ionizzazione)
        self.radiation_length = radiation_length  # cm (per scattering)

# Definizione di materiali comuni
materials = {
    "water": Material("Water", 1.0, 0.555, 75.0, 36.1),
    "bone": Material("Bone", 1.85, 0.5, 91.9, 9.8),
    "lung": Material("Lung", 0.26, 0.555, 75.0, 38.6),
    "air": Material("Air", 0.0012, 0.499, 85.7, 30420.0),
    "muscle": Material("Muscle", 1.05, 0.55, 75.3, 34.8),
    "fat": Material("Fat", 0.92, 0.558, 73.1, 37.8),
    "brain": Material("Brain", 1.04, 0.553, 73.4, 35.1),
}

class VoxelizedGeometry:
    def __init__(self, dimensions, voxel_size=1.0):
        """
        Inizializza una geometria voxelizzata

        Parameters:
        -----------
        dimensions : tuple
            Numero di voxel in ciascuna direzione (nx, ny, nz)
        voxel_size : float
            Dimensione del voxel in mm
        """
        self.dimensions = dimensions
        self.voxel_size = voxel_size

        # Inizializza array di materiali (default: aria)
        self.materials = np.zeros(dimensions, dtype=int)

        # Dizionario ID -> materiale
        self.material_dict = {
            0: materials["air"],
            1: materials["water"],
            2: materials["bone"],
            3: materials["air"],
        }

    def set_material(self, material_id, i_min, i_max, j_min, j_max, k_min, k_max):
        """
        Imposta un materiale in una regione specifica

        Parameters:
        -----------
        material_id : int
            ID del materiale da impostare
        i_min, i_max, j_min, j_max, k_min, k_max : int
            Limiti della regione in cui impostare il materiale
        """
        self.materials[i_min:i_max, j_min:j_max, k_min:k_max] = material_id

    def get_material_at(self, position):
        """
        Restituisce il materiale alla posizione data

        Parameters:
        -----------
        position : array-like
            Posizione [x, y, z] in mm

        Returns:
        --------
        material : Material
            Materiale alla posizione specificata
        """
        x, y, z = position

        # Converti in indici voxel
        i = int(x / self.voxel_size)
        j = int(y / self.voxel_size)
        k = int(z / self.voxel_size)

        # Verifica se è dentro i limiti
        if (0 <= i < self.dimensions[0] and
            0 <= j < self.dimensions[1] and
            0 <= k < self.dimensions[2]):
            material_id = self.materials[i, j, k]
            return self.material_dict[material_id]
        else:
            # Fuori dai limiti, restituisci aria
            return self.material_dict[3]  # aria
