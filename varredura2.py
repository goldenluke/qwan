import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, laplace
from numpy.fft import fft2, fftshift
from tqdm import tqdm

# ============================================================
# CONFIGURAÇÃO GLOBAL
# ============================================================
N = 64
DT = 0.03
L = 0.5
GAMMA = 1.0
ETA = 3.0         # intensidade do feedback adaptativo
STEPS = 800

alpha_values = np.linspace(0.0, 3.0, 40)
beta_values  = np.linspace(0.0, 3.0, 40)

# ============================================================
# MOTOR LANDUA-GINZBURG ADAPTATIVO
# ============================================================
class QWANCritical:
    def __init__(self, size, alpha0, beta):
        self.size = size
        self.alpha0 = alpha0
        self.beta = beta
        self.x = np.random.uniform(-0.1, 0.1, (size, size))

    def step(self):

        local_mean = gaussian_filter(self.x, sigma=1.5)

        # Potencial duplo poço
        dG = self.x * (self.x**2 - 1)

        # Feedback adaptativo
        variance = np.var(self.x)
        alpha_eff = self.alpha0 * (1 + ETA * variance)

        dH = 2 * (self.x - local_mean)
        lap = laplace(self.x)

        force = (
            -GAMMA * dG
            + alpha_eff * dH
            + 2 * self.beta * lap
        )

        self.x += DT * L * force

    def metrics(self):

        variance = np.var(self.x)
        magnetization = np.mean(self.x)
        grad = np.mean(np.gradient(self.x)[0]**2 +
                       np.gradient(self.x)[1]**2)

        return variance, magnetization, grad

    def power_spectrum(self):

        F = fftshift(np.abs(fft2(self.x))**2)
        return F

# ============================================================
# VARREDURA + MEDIDAS CRÍTICAS
# ============================================================
variance_map = np.zeros((len(alpha_values), len(beta_values)))
mag_map = np.zeros_like(variance_map)

print("Executando varredura crítica...")

for i, alpha in enumerate(tqdm(alpha_values)):
    for j, beta in enumerate(beta_values):

        model = QWANCritical(N, alpha, beta)

        for _ in range(STEPS):
            model.step()

        var, mag, grad = model.metrics()

        variance_map[i,j] = var
        mag_map[i,j] = abs(mag)

print("Concluído.")

# ============================================================
# MAPA DE TRANSIÇÃO (MAGNETIZAÇÃO)
# ============================================================
plt.figure(figsize=(7,6))
plt.imshow(
    mag_map,
    origin="lower",
    extent=[
        beta_values.min(),
        beta_values.max(),
        alpha_values.min(),
        alpha_values.max()
    ],
    aspect="auto"
)
plt.colorbar(label="|Magnetização|")
plt.xlabel("BETA")
plt.ylabel("ALPHA")
plt.title("Transição de Fase (Duplo Poço)")
plt.tight_layout()
plt.savefig("critical_transition.png", dpi=300)
plt.close()

# ============================================================
# ESTIMATIVA DO EXPOENTE CRÍTICO β (numérico)
# ============================================================
# Escolhemos beta fixo intermediário
beta_fixed_index = len(beta_values)//2
mag_slice = mag_map[:, beta_fixed_index]

# Aproximação log-log perto da transição
alpha_crit = alpha_values[np.argmax(np.gradient(mag_slice))]

mask = alpha_values > alpha_crit
x_fit = alpha_values[mask] - alpha_crit
y_fit = mag_slice[mask]

x_fit = x_fit[x_fit > 1e-3]
y_fit = y_fit[:len(x_fit)]

logx = np.log(x_fit)
logy = np.log(y_fit + 1e-8)

coef = np.polyfit(logx, logy, 1)
beta_exponent = coef[0]

print("Expoente crítico aproximado β ≈", beta_exponent)

# ============================================================
# ANÁLISE ESPECTRAL
# ============================================================
model = QWANCritical(N, alpha_values[-1], beta_values[0])

for _ in range(STEPS):
    model.step()

spectrum = model.power_spectrum()

plt.figure(figsize=(6,6))
plt.imshow(np.log(spectrum+1e-8), cmap="magma")
plt.colorbar(label="Log Power Spectrum")
plt.title("Espectro de Fourier")
plt.tight_layout()
plt.savefig("fourier_spectrum.png", dpi=300)
plt.close()

print("Arquivos gerados:")
print("- critical_transition.png")
print("- fourier_spectrum.png")