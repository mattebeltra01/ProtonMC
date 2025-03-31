from ProtonMC.src.core.simulator import ProtonSimulator
import numpy as np
import matplotlib.pyplot as plt

def run_simple_simulation():
    # Create simulator instance
    sim = ProtonSimulator(material_density=1.0)

    # Create a proton with 100 MeV energy
    proton = sim.create_proton(
        position=[0, 0, 0],
        direction=[0, 0, 1],
        energy=100.0
    )

    # Run simulation until particle stops
    while proton.alive:
        sim.step(proton)

    # Plot trajectory
    track = np.array(proton.track)
    plt.figure(figsize=(10, 6))
    plt.plot(track[:, 2], track[:, 1], 'b-', label='Proton track')
    plt.xlabel('z (mm)')
    plt.ylabel('y (mm)')
    plt.title('Proton Track')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_simple_simulation()
