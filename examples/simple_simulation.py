import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Aggiungi la directory principale al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ora puoi importare i moduli da src
from src.utils.visualization import plot_trajectory_3d, plot_bragg_curve
from src.core.simulator import ProtonSimulator
from src.core.materials import materials

def main():
    # Crea un'istanza del simulatore con acqua come materiale
    simulator = ProtonSimulator(material=materials["water"])

    # Parametri di simulazione
    initial_position = [0, 0, 0]  # mm
    initial_direction = [0, 0, 1]  # direzione lungo z
    initial_energy = 100.0        # MeV
    num_steps = 1000
    step_size = 0.1               # mm

    # Crea un protone
    proton = simulator.create_proton(
        position=initial_position,
        direction=initial_direction,
        energy=initial_energy
    )

    # Array per i dati
    depths = []
    energies = []

    # Esegui la simulazione
    print("Inizia simulazione...")
    for i in range(num_steps):
        # Salva i dati
        depths.append(proton.position[2])
        energies.append(proton.energy)

        # Esegui uno step
        if not simulator.step(proton, step_size):
            print(f"Protone fermato dopo {i+1} passi")
            break

    # Calcola la perdita di energia
    energy_losses = np.abs(np.diff(energies)) / step_size  # MeV/mm

    # Visualizza i risultati
    plot_bragg_curve(depths[:-1], energy_losses, save_path="bragg_curve.png")
    plot_trajectory_3d([proton], save_path="trajectory_3d.png")

    # Statistiche finali
    print(f"Range del protone: {depths[-1]:.2f} mm")
    print(f"Energia iniziale: {initial_energy:.2f} MeV")
    print(f"Passi totali: {len(depths)}")

if __name__ == "__main__":
    main()
