import numpy as np
import matplotlib
matplotlib.use('Agg')  # essencial para WSL/servidor
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import gaussian_filter, laplace

# ================================================================
# 1. PARÂMETROS DO MODELO
# ================================================================
N = 64
DT = 0.05              # menor para estabilidade numérica
L_ONSAGER = 0.5
ALPHA = 0.2
BETA = 0.6
GAMMA = 0.1

FRAMES = 150

# ================================================================
# 2. MOTOR VARIACIONAL QWAN
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
    # Dinâmica variacional correta
    # ------------------------------------------------------------
    def step(self):

        # Média local (liberdade configuracional)
        local_mean = gaussian_filter(self.x, sigma=1.5)

        # Derivadas funcionais
        dG = (self.x - 0.5)
        dH = 2 * (self.x - local_mean)
        lap = laplace(self.x)

        # Força variacional (δΦ/δx)
        variational_force = (
            -GAMMA * dG
            + ALPHA * dH
            + 2 * BETA * lap
        )

        # Forçamento ambiental
        A_force = 0.1 * (self.E - self.x)

        # Evolução tipo Onsager
        self.x += DT * (L_ONSAGER * variational_force + A_force)
        self.x = np.clip(self.x, 0, 1)

        # --------------------------------------------------------
        # Monitoramento das métricas
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
# 3. CONFIGURAÇÃO DA VISUALIZAÇÃO
# ================================================================
print("Iniciando motor biofísico QWAN variacional...")
engine = QWANEngine(N)

fig = plt.figure(figsize=(12, 6), facecolor='black')
grid = plt.GridSpec(2, 2, wspace=0.3, hspace=0.3)

# Campo principal
ax_main = fig.add_subplot(grid[:, 0])
im = ax_main.imshow(engine.x, cmap='magma', interpolation='lanczos')
ax_main.set_title("Campo Biofísico QWAN (Variacional)", color='white')
ax_main.axis('off')

# Métricas energéticas
ax_metrics = fig.add_subplot(grid[0, 1])
ax_metrics.set_title("Dinâmica de Onsager (Φ, H, I)", color='white', fontsize=10)
line_phi, = ax_metrics.plot([], [], 'w-', label='Φ')
line_h,   = ax_metrics.plot([], [], 'c--', label='H')
line_i,   = ax_metrics.plot([], [], 'y--', label='I')
ax_metrics.set_facecolor('#111111')
ax_metrics.tick_params(colors='white')
ax_metrics.legend(facecolor='#111111', edgecolor='white')

# Correlação com ambiente
ax_env = fig.add_subplot(grid[1, 1])
ax_env.set_title("Correlação com Ambiente", color='white', fontsize=10)
line_a, = ax_env.plot([], [], 'm-', label='Adaptabilidade')
ax_env.set_facecolor('#111111')
ax_env.tick_params(colors='white')
ax_env.legend(facecolor='#111111', edgecolor='white')

# ================================================================
# 4. LOOP DE ATUALIZAÇÃO
# ================================================================
def update(frame):
    if frame % 10 == 0:
        print(f"Processando frame {frame}/{FRAMES}...")

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
# 5. SALVAMENTO
# ================================================================
output_file = "qwan_variacional.gif"
print(f"Renderizando simulação em {output_file}...")
ani.save(output_file, writer="pillow", fps=20)

print("Concluído.")