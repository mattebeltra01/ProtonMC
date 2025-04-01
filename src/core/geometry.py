import numpy as np
from .materials import materials

class Geometry:
    def __init__(self, dimensions, voxel_size):
        """
        Crea una geometria voxellizzata

        Parameters:


----


        dimensions : tuple (nx, ny, nz)
            Numero di voxel in ciascuna direzione
        voxel_size : float
            Dimensione del voxel in mm
        """
        self.voxel_size = voxel_size  # mm
        self.dimensions = dimensions  # (nx, ny, nz)
        # Inizializza con aria
        air_id = 3  # ID per l'aria (potrebbe essere un enum)
        self.materials = np.ones(dimensions, dtype=int) * air_id

        # Dizionario per mappare ID materiali a oggetti Material
        self.material_dict = {
            0: materials["water"],
            1: materials["bone"],
            2: materials["lung"],
            3: materials["air"],
            4: materials["muscle"],
            5: materials["fat"]
        }

    def set_material(self, x_range, y_range, z_range, material_id):
        """Imposta il materiale in una regione specifica"""
        x_min, x_max = x_range
        y_min, y_max = y_range
        z_min, z_max = z_range

        # Converti in indici voxel
        i_min, i_max = int(x_min/self.voxel_size), int(x_max/self.voxel_size)
        j_min, j_max = int(y_min/self.voxel_size), int(y_max/self.voxel_size)
        k_min, k_max = int(z_min/self.voxel_size), int(z_max/self.voxel_size)

        # Applica limiti
        i_min, i_max = max(0, i_min), min(self.dimensions[0], i_max)
        j_min, j_max = max(0, j_min), min(self.dimensions[1], j_max)
        k_min, k_max = max(0, k_min), min(self.dimensions[2], k_max)

        self.materials[i_min:i_max, j_min:j_max, k_min:k_max] = material_id

    def get_material_at(self, position):
        """Restituisce il materiale alla posizione data"""
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
