import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_trajectory_3d(particles, show=True, save_path=None):
    """
    Visualizza la traiettoria 3D delle particelle

    Parameters:
    -----------
    particles : list
        Lista di oggetti Particle da visualizzare
    show : bool
        Se True, mostra il grafico interattivo
    save_path : str, optional
        Percorso dove salvare l'immagine
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Colori diversi per particelle diverse
    colors = ['b', 'r', 'g', 'c', 'm', 'y']

    for i, p in enumerate(particles):
        if hasattr(p, 'track') and len(p.track) > 0:
            track = np.array(p.track)
            ax.plot(track[:, 0], track[:, 1], track[:, 2],
                    color=colors[i % len(colors)],
                    label=f'Proton {i+1}')

    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('Traiettorie 3D dei protoni')
    ax.legend()

    if save_path:
        plt.savefig(save_path)
        print(f"Grafico salvato come '{save_path}'")

    if show:
        plt.show()
    else:
        plt.close()

def plot_bragg_curve(depths, energy_losses, show=True, save_path=None):
    """
    Visualizza la curva di Bragg

    Parameters:
    -----------
    depths : array-like
        Profondità in mm
    energy_losses : array-like
        Perdita di energia a ciascuna profondità
    show : bool
        Se True, mostra il grafico interattivo
    save_path : str, optional
        Percorso dove salvare l'immagine
    """
    plt.figure(figsize=(10, 6))
    plt.plot(depths, energy_losses)
    plt.xlabel('Profondità (mm)')
    plt.ylabel('Perdita di energia (MeV/mm)')
    plt.title('Curva di Bragg')
    plt.grid(True)

    if save_path:
        plt.savefig(save_path)
        print(f"Grafico salvato come '{save_path}'")

    if show:
        plt.show()
    else:
        plt.close()
