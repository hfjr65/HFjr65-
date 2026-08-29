import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import cKDTree

# ------------------------------------------------------------
# 1. PARAMETRE (Prøv f.eks. N_PARTICLES = 500 eller 1000!)
# ------------------------------------------------------------
N_PARTICLES = 600          # Mye høyere antall takket være KDTree!
BOX_SIZE = 25.0            # Større boks for plass til svermen
SPEED = 0.12               # Partiklenes fart

# Radiuser for krefter
R_REPULSION = 0.6          # Frastøtning (unngå kollisjon)
R_ALIGNMENT = 2.0          # Retningsjustering (Vicsek)
R_ATTRACTION = 4.0         # Tiltrekning (holde sammen i sverm)

# Vektingsfaktorer for oppførsel
W_REPULSION = 1.5
W_ALIGNMENT = 1.0
W_ATTRACTION = 0.5
NOISE = 0.15               # Støy/termisk fluktuasjon

# Lagringsvalg (Sett til True hvis du vil lagre fil)
SAVE_ANIMATION = False
FILE_FORMAT = 'mp4'        # 'mp4' (krever ffmpeg) eller 'gif' (krever pillow)

# ------------------------------------------------------------
# 2. INITIALISERING
# ------------------------------------------------------------
positions = np.random.rand(N_PARTICLES, 2) * BOX_SIZE
angles = (np.random.rand(N_PARTICLES) - 0.5) * 2 * np.pi
order_history = []

def compute_order(angles):
    """Beregner polar orden (0 = uorden, 1 = full orden)."""
    return np.hypot(np.mean(np.cos(angles)), np.mean(np.sin(angles)))

# ------------------------------------------------------------
# 3. FIGUR OG OPPSETT
# ------------------------------------------------------------
fig, (ax_main, ax_hist) = plt.subplots(1, 2, figsize=(12, 5.5), gridspec_kw={'width_ratios': [2, 1]})
fig.patch.set_facecolor('#f0f0f0')

ax_main.set_xlim(0, BOX_SIZE)
ax_main.set_ylim(0, BOX_SIZE)
ax_main.set_aspect('equal')
ax_main.set_title(f'Boids-sverm med KDTree (N={N_PARTICLES})', fontsize=12, fontweight='bold')

scatter = ax_main.scatter(
    positions[:, 0], positions[:, 1], 
    s=20, c=angles, cmap='hsv', vmin=-np.pi, vmax=np.pi, 
    edgecolors='none', alpha=0.85
)

order_text = ax_main.text(
    0.5, BOX_SIZE - 1.2, 'Makro-orden: 0.000', 
    fontsize=11, ha='center', bbox=dict(facecolor='white', alpha=0.85, edgecolor='none')
)

ax_hist.set_title('Makro-observables over tid', fontsize=11)
ax_hist.set_ylim(0, 1)
ax_hist.set_xlim(0, 200)
ax_hist.set_xlabel('Tid (steg)')
ax_hist.set_ylabel('Orden (Polar alignment)')
ax_hist.grid(True, alpha=0.3)
line, = ax_hist.plot([], [], color='#1f77b4', linewidth=2)

# ------------------------------------------------------------
# 4. LYNRASK WEKTORISERT UPDATE (cKDTree)
# ------------------------------------------------------------
def update(frame):
    global positions, angles, order_history

    # Bygg KDTree for lynrask søk i naboskap
    tree = cKDTree(positions, boxsize=BOX_SIZE)
    
    # Finn naboer innenfor største interaksjonsradius (R_ATTRACTION)
    neighbors_list = tree.query_ball_point(positions, r=R_ATTRACTION)
    
    new_angles = np.zeros(N_PARTICLES)

    for i, idxs in enumerate(neighbors_list):
        # Fjern seg selv fra nabolisten
        idxs = [idx for idx in idxs if idx != i]
        
        if not idxs:
            # Ingen naboer -> fortsett i samme retning + litt støy
            new_angles[i] = angles[i] + (np.random.rand() - 0.5) * NOISE
            continue

        # Beregn minimale avstandsvektorer med periodiske grenser (Torus)
        delta = positions[idxs] - positions[i]
        delta = delta - BOX_SIZE * np.round(delta / BOX_SIZE)
        dists = np.hypot(delta[:, 0], delta[:, 1])

        # Vektorer for de tre boids-reglene:
        v_rep = np.zeros(2)
        v_align = np.zeros(2)
        v_att = np.zeros(2)

        # 1. Frastøtning (Repulsion)
        rep_mask = dists < R_REPULSION
        if np.any(rep_mask):
            # skyv unna: omvendt proporsjonal med avstand
            v_rep = -np.sum(delta[rep_mask] / (dists[rep_mask, None]**2 + 1e-5), axis=0)

        # 2. Alignment (Vicsek)
        align_mask = dists < R_ALIGNMENT
        if np.any(align_mask):
            v_align = np.array([
                np.mean(np.cos(angles[idxs][align_mask])),
                np.mean(np.sin(angles[idxs][align_mask]))
            ])

        # 3. Tiltrekning (Attraction)
        att_mask = dists < R_ATTRACTION
        if np.any(att_mask):
            # Beveg deg mot tyngdepunktet til naboene
            v_att = np.mean(delta[att_mask], axis=0)

        # Kombiner kreftene med vekting
        desired_dir = (
            W_REPULSION * v_rep + 
            W_ALIGNMENT * v_align + 
            W_ATTRACTION * v_att
        )

        if np.linalg.norm(desired_dir) > 0:
            target_angle = np.arctan2(desired_dir[1], desired_dir[0])
        else:
            target_angle = angles[i]

        # Legg til støy
        noise_angle = (np.random.rand() - 0.5) * NOISE
        new_angles[i] = target_angle + noise_angle

    angles = new_angles

    # Oppdater posisjoner
    positions[:, 0] += np.cos(angles) * SPEED
    positions[:, 1] += np.sin(angles) * SPEED
    positions %= BOX_SIZE

    # Oppdater grafikk
    scatter.set_offsets(positions)
    scatter.set_array(angles)

    current_order = compute_order(angles)
    order_history.append(current_order)
    if len(order_history) > 200:
        order_history.pop(0)

    order_text.set_text(f'Makro-orden: {current_order:.3f}')
    line.set_data(range(len(order_history)), order_history)

    return scatter, order_text, line

# ------------------------------------------------------------
# 5. KJØRING / EKSPORTERING
# ------------------------------------------------------------
ani = FuncAnimation(fig, update, frames=300, interval=25, blit=False)
plt.tight_layout()

if SAVE_ANIMATION:
    print("Lagrer animasjon... Vennligst vent.")
    if FILE_FORMAT == 'mp4':
        # Krever: pip install ffmpeg-python eller ffmpeg installert på systemet
        ani.save('boids_swarm.mp4', writer='ffmpeg', fps=30, dpi=150)
        print("Lagret som 'boids_swarm.mp4'")
    elif FILE_FORMAT == 'gif':
        # Krever: pip install pillow
        ani.save('boids_swarm.gif', writer='pillow', fps=25, dpi=100)
        print("Lagret som 'boids_swarm.gif'")
else:
    plt.show()
