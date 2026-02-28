import numpy as np
import matplotlib
matplotlib.use('Agg')  # essential for WSL/server environments
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import gaussian_filter, laplace

# ================================================================
# 1. MODEL PARAMETERS
# ================================================================
N = 64
DT = 0.05              # smaller for numerical stability
L_ONSAGER = 0.5
ALPHA = 0.2
BETA = 0.6
GAMMA = 0.1

FRAMES = 150

# ================================================================
# 2. QWAN VARIATIONAL ENGINE
# ================================================================
class QWANEngine:
    def __init__(self, size):
        self.size = size
        self.x = np.random.uniform(0.4, 0.6, (size, size))
        self.E = np.zeros((size, size))
        self.create_environment()
        self.history = {'phi': [], 'G': [], 'H': [], 'I': [], 'A': []}

    def create_environment(self):
        for _ in range(5):
            r = np.random.randint(5, self.size // 2)
            y, x = np.ogrid[-self.size//2:self.size//2,
                           -self.size//2:self.size//2]
            mask = x*x + y*y <= r*r
            self.E[mask] += 0.2
        self.E = np.clip(self.E, 0, 1)

    # ------------------------------------------------------------
    # Correct variational dynamics
    # ------------------------------------------------------------
    def step(self):

        # Local mean (configurational freedom)
        local_mean = gaussian_filter(self.x, sigma=1.5)

        # Functional derivatives
        dG = (self.x - 0.5)
        dH = 2 * (self.x - local_mean)
        lap = laplace(self.x)

        # Variational force (δΦ/δx)
        variational_force = (
            -GAMMA * dG
            + ALPHA * dH
            + 2 * BETA * lap
        )

        # Environmental forcing
        A_force = 0.1 * (self.E - self.x)

        # Onsager-type evolution
        self.x += DT * (L_ONSAGER * variational_force + A_force)
        self.x = np.clip(self.x, 0, 1)

        # --------------------------------------------------------
        # Metric monitoring
        # --------------------------------------------------------
        G_field = 0.5 * (self.x - 0.5)**2
        H_field = (self.x - local_mean)**2
        dx, dy = np.gradient(self.x)
        I_field = dx**2 + dy**2
        Phi_field = GAMMA*G_field - ALPHA*H_field + BETA*I_field

        self.history['phi'].append(np.mean(Phi_field))
        self.history['G'].append(np.mean(G_field))
        self.history['H'].append(np.mean(H_field))
        self.history['I'].append(np.mean(I_field))
        self.history['A'].append(
            np.corrcoef(self.x.flat, self.E.flat)[0, 1]
        )

# ================================================================
# 3. VISUALIZATION SETUP
# ================================================================
print("Starting variational QWAN biophysical engine...")
engine = QWANEngine(N)

fig = plt.figure(figsize=(12, 6), facecolor='black')
grid = plt.GridSpec(2, 2, wspace=0.3, hspace=0.3)

# Main field
ax_main = fig.add_subplot(grid[:, 0])
im = ax_main.imshow(engine.x, cmap='magma', interpolation='lanczos')
ax_main.set_title("QWAN Biophysical Field (Variational)", color='white')
ax_main.axis('off')

# Energy metrics
ax_metrics = fig.add_subplot(grid[0, 1])
ax_metrics.set_title("Onsager Dynamics (Φ, H, I)", color='white', fontsize=10)
line_phi, = ax_metrics.plot([], [], 'w-', label='Φ')
line_h,   = ax_metrics.plot([], [], 'c--', label='H')
line_i,   = ax_metrics.plot([], [], 'y--', label='I')
ax_metrics.set_facecolor('#111111')
ax_metrics.tick_params(colors='white')
ax_metrics.legend(facecolor='#111111', edgecolor='white')

# Environmental correlation
ax_env = fig.add_subplot(grid[1, 1])
ax_env.set_title("Environmental Correlation", color='white', fontsize=10)
line_a, = ax_env.plot([], [], 'm-', label='Adaptability')
ax_env.set_facecolor('#111111')
ax_env.tick_params(colors='white')
ax_env.legend(facecolor='#111111', edgecolor='white')

# ================================================================
# 4. UPDATE LOOP
# ================================================================
def update(frame):
    if frame % 10 == 0:
        print(f"Processing frame {frame}/{FRAMES}...")

    engine.step()
    im.set_array(engine.x)

    t = range(len(engine.history['phi']))

    line_phi.set_data(t, engine.history['phi'])
    line_h.set_data(t, engine.history['H'])
    line_i.set_data(t, engine.history['I'])
    line_a.set_data(t, engine.history['A'])

    for ax in [ax_metrics, ax_env]:
        ax.relim()
        ax.autoscale_view()

    return im, line_phi, line_h, line_i, line_a

ani = FuncAnimation(
    fig,
    update,
    frames=FRAMES,
    interval=50,
    blit=True
)

# ================================================================
# 5. SAVING
# ================================================================
output_file = "qwan_variational.gif"
print(f"Rendering simulation to {output_file}...")
ani.save(output_file, writer="pillow", fps=20)

print("Completed.")
