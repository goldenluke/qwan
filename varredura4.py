import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift
from tqdm import tqdm

# ============================================================
# CONFIGURAÇÃO GLOBAL
# ============================================================

N = 192                 # tamanho equilibrado (estável e rápido)
DT = 0.02
STEPS = 4000
Tc = 1.0

a0 = 1.0
b = 1.0
kappa = 1.0

# Faixa refinada perto do ponto crítico
temperatures = np.linspace(0.95, 1.05, 11)

# ============================================================
# LAPLACIANO PERIÓDICO RÁPIDO
# ============================================================

def laplacian(field):
    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4 * field
    )

# ============================================================
# MODELO TDGL ESTOCÁSTICO (MODEL A)
# ============================================================

class TDGL:

    def __init__(self, T):
        self.T = T
        self.x = np.random.normal(0, 0.1, (N, N))
        self.a = a0 * (T - Tc)

    def simulate(self):

        for _ in range(STEPS):

            lap = laplacian(self.x)
            force = -(self.a * self.x + b * self.x**3 - kappa * lap)

            noise = np.sqrt(2 * self.T * DT) * np.random.normal(size=self.x.shape)

            self.x += DT * force + noise

        return self.x

# ============================================================
# FUNÇÃO DE CORRELAÇÃO CORRETA
# ============================================================

def correlation_function(field):

    field = field - np.mean(field)

    F = fft2(field)
    power = np.abs(F)**2
    corr = np.real(ifft2(power))

    corr = fftshift(corr)

    center = N // 2
    corr /= corr[center, center]

    y, x = np.indices((N, N))
    r = np.sqrt((x - center)**2 + (y - center)**2)
    r = r.astype(np.int32)

    radial = np.bincount(r.ravel(), corr.ravel())
    counts = np.bincount(r.ravel())
    radial /= counts

    return radial[:N//2]

# ============================================================
# EXTRAÇÃO ROBUSTA DO COMPRIMENTO DE CORRELAÇÃO ξ
# ============================================================

def extract_xi(radial_corr):

    r = np.arange(len(radial_corr))

    mask = (radial_corr > 0.05) & (radial_corr < 0.9) & (r > 3)

    if np.sum(mask) < 6:
        return np.nan

    r_fit = r[mask]
    c_fit = radial_corr[mask]

    slope, _ = np.polyfit(r_fit, np.log(c_fit), 1)

    if slope >= 0:
        return np.nan

    return -1 / slope

# ============================================================
# VARREDURA EM TEMPERATURA
# ============================================================

xi_values = []

print("Simulando transição crítica...\n")

for T in tqdm(temperatures):

    model = TDGL(T)
    field = model.simulate()

    radial_corr = correlation_function(field)
    xi = extract_xi(radial_corr)

    xi_values.append(xi)

xi_values = np.array(xi_values)

print("\nTemperaturas:", temperatures)
print("ξ:", xi_values)

# ============================================================
# ESTIMATIVA ROBUSTA DO EXPOENTE ν
# ============================================================

reduced_temp = np.abs(temperatures - Tc)

valid = (~np.isnan(xi_values)) & (xi_values > 0) & (reduced_temp > 0)

if np.sum(valid) < 4:
    print("\nNão há pontos suficientes para estimar ν.")
    nu = np.nan
else:
    logt = np.log(reduced_temp[valid])
    logxi = np.log(xi_values[valid])

    coef = np.polyfit(logt, logxi, 1)
    nu = -coef[0]

    print("\nExpoente crítico ν ≈", nu)

# ============================================================
# PLOT LOG-LOG
# ============================================================

plt.figure(figsize=(6,5))
plt.loglog(reduced_temp, xi_values, 'o-')
plt.xlabel("|T - Tc|")
plt.ylabel("ξ")
plt.title(f"ν ≈ {nu:.3f}")
plt.tight_layout()
plt.savefig("critical_exponent_nu.png", dpi=300)
plt.show()