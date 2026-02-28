import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
from numpy.fft import fft2, ifft2, fftshift
from tqdm import tqdm

# ============================================================
# CONFIGURAÇÃO
# ============================================================
N = 128
DT = 0.01
STEPS = 3000
SAVE_EVERY = 10

a0 = 1.0
b = 1.0
kappa = 1.0
Tc = 1.0

temperatures = np.linspace(0.7, 1.3, 15)

# ============================================================
# MODELO TDGL ESTOCÁSTICO
# ============================================================
class TDGL:

    def __init__(self, N, T):
        self.N = N
        self.T = T
        self.x = np.random.normal(0, 0.1, (N, N))
        self.a = a0 * (T - Tc)

    def step(self):
        lap = laplace(self.x)
        force = -(self.a * self.x + b * self.x**3 - kappa * lap)

        noise = np.sqrt(2 * self.T * DT) * np.random.normal(size=self.x.shape)

        self.x += DT * force + noise

    def simulate(self):
        for i in range(STEPS):
            self.step()
        return self.x

# ============================================================
# FUNÇÃO DE CORRELAÇÃO RADIAL
# ============================================================
def correlation_function(field):

    F = fft2(field)
    power = np.abs(F)**2
    corr = fftshift(ifft2(power).real)

    corr /= np.max(corr)

    # média radial
    y, x = np.indices((N, N))
    center = N // 2
    r = np.sqrt((x - center)**2 + (y - center)**2)
    r = r.astype(np.int32)

    radial = np.bincount(r.ravel(), corr.ravel())
    counts = np.bincount(r.ravel())
    radial /= counts

    return radial[:N//2]

# ============================================================
# EXTRAÇÃO DE ξ
# ============================================================
def extract_xi(radial_corr):

    r = np.arange(len(radial_corr))

    mask = radial_corr > 0
    r = r[mask]
    c = radial_corr[mask]

    logc = np.log(c + 1e-8)

    coef = np.polyfit(r[:30], logc[:30], 1)
    slope = coef[0]

    xi = -1 / slope if slope < 0 else np.inf
    return xi

# ============================================================
# VARREDURA EM TEMPERATURA
# ============================================================
xi_values = []

print("Simulando transição crítica...")

for T in tqdm(temperatures):

    model = TDGL(N, T)
    field = model.simulate()

    radial_corr = correlation_function(field)
    xi = extract_xi(radial_corr)

    xi_values.append(xi)

xi_values = np.array(xi_values)

# ============================================================
# ESTIMATIVA DO EXPOENTE CRÍTICO ν
# ============================================================
reduced_temp = np.abs(temperatures - Tc)

mask = reduced_temp > 0.02
logt = np.log(reduced_temp[mask])
logxi = np.log(xi_values[mask])

coef = np.polyfit(logt, logxi, 1)
nu = -coef[0]

print("Expoente crítico ν ≈", nu)

# ============================================================
# PLOT
# ============================================================
plt.figure()
plt.loglog(reduced_temp, xi_values, 'o-')
plt.xlabel("|T - Tc|")
plt.ylabel("ξ")
plt.title(f"Expoente crítico ν ≈ {nu:.3f}")
plt.tight_layout()
plt.savefig("critical_exponent_nu.png", dpi=300)
plt.close()

print("Arquivo salvo: critical_exponent_nu.png")