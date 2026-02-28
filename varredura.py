import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, laplace
from tqdm import tqdm

# ============================================================
# CONFIGURAÇÃO
# ============================================================
N = 64
DT = 0.05
L_ONSAGER = 0.5
GAMMA = 0.1
STEPS = 600   # mais tempo para convergência

alpha_values = np.linspace(0.0, 2.0, 40)
beta_values  = np.linspace(0.0, 2.0, 40)

# ============================================================
# MOTOR VARIACIONAL PURO (SEM AMBIENTE)
# ============================================================
class QWANEngine:
    def __init__(self, size, alpha, beta):
        self.size = size
        self.alpha = alpha
        self.beta = beta
        self.x = np.random.uniform(0.4, 0.6, (size, size))

    def step(self):

        local_mean = gaussian_filter(self.x, sigma=1.5)

        dG = (self.x - 0.5)
        dH = 2 * (self.x - local_mean)
        lap = laplace(self.x)

        variational_force = (
            -GAMMA * dG
            + self.alpha * dH
            + 2 * self.beta * lap
        )

        self.x += DT * (L_ONSAGER * variational_force)
        self.x = np.clip(self.x, 0, 1)

    def compute_metrics(self):

        local_mean = gaussian_filter(self.x, sigma=1.5)

        G_field = 0.5 * (self.x - 0.5)**2
        H_field = (self.x - local_mean)**2
        dx, dy = np.gradient(self.x)
        I_field = dx**2 + dy**2
        Phi_field = GAMMA*G_field - self.alpha*H_field + self.beta*I_field

        variance_global = np.var(self.x)
        grad_norm = np.mean(I_field)

        return (
            np.mean(Phi_field),
            np.mean(H_field),
            np.mean(I_field),
            variance_global,
            grad_norm
        )

# ============================================================
# VARREDURA PARAMÉTRICA
# ============================================================
phi_map = np.zeros((len(alpha_values), len(beta_values)))
var_map = np.zeros_like(phi_map)
grad_map = np.zeros_like(phi_map)

print("Executando varredura paramétrica...")

for i, alpha in enumerate(tqdm(alpha_values)):
    for j, beta in enumerate(beta_values):

        engine = QWANEngine(N, alpha, beta)

        for _ in range(STEPS):
            engine.step()

        phi, H, I, var_global, grad_norm = engine.compute_metrics()

        phi_map[i, j] = phi
        var_map[i, j] = var_global
        grad_map[i, j] = grad_norm

print("Varredura concluída.")

# ============================================================
# MAPAS CONTÍNUOS
# ============================================================
def plot_heatmap(data, title, filename):
    plt.figure(figsize=(7,6))
    plt.imshow(
        data,
        origin="lower",
        extent=[
            beta_values.min(),
            beta_values.max(),
            alpha_values.min(),
            alpha_values.max()
        ],
        aspect="auto"
    )
    plt.colorbar()
    plt.xlabel("BETA (Coerência)")
    plt.ylabel("ALPHA (Liberdade)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

plot_heatmap(phi_map, "Energia Final Φ", "phi_map.png")
plot_heatmap(var_map, "Variância Global", "variance_map.png")
plot_heatmap(grad_map, "Norma do Gradiente", "gradient_map.png")

print("Mapas salvos:")
print(" - phi_map.png")
print(" - variance_map.png")
print(" - gradient_map.png")