import numpy as np
from scipy.special import roots_laguerre
from numpy.polynomial.legendre import leggauss
import time
import matplotlib.pyplot as plt
from sympy.integrals.quadrature import gauss_legendre


# ====================== Méthodes de quadrature ======================

def gauss_laguerre_integral(f, n):
    """Intégrale ∫_0^∞ e^{-x} f(x) dx"""
    x, w = roots_laguerre(n)
    return np.sum(w * f(x))


def gauss_legendre_integral(f, n, a=-1, b=1):
    """Intégrale ∫_a^b f(x) dx"""
    x, w = leggauss(n)
    t = 0.5 * (x * (b - a) + (a + b))
    return 0.5 * (b - a) * np.sum(w * f(t))


def gauss_chebyshev_integral(f, n):
    """Intégrale ∫_{-1}^1 f(x)/√(1-x²) dx"""
    theta = np.pi * (2 * np.arange(1, n + 1) - 1) / (2 * n)
    x = np.cos(theta)
    w = np.full(n, np.pi / n)
    return np.sum(w * f(x))


def simpson_integral(f, n, a, b):
    """Règle de Simpson composite, n pair"""
    if n % 2 != 0:
        raise ValueError("n doit être pair")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (h / 3) * (y[0] + y[-1] + 4 * np.sum(y[1::2]) + 2 * np.sum(y[2:-1:2]))


# ====================== Spline Quadratique ======================

def calculer_spline_quadratique(x_points, y_points):
    x = np.array(x_points, dtype=float)
    y = np.array(y_points, dtype=float)
    n = len(x) - 1
    h = np.diff(x)
    a = [0.0] * n
    b = [0.0] * n
    c = [0.0] * n

    a[0] = 0.0
    c[0] = y[0]
    b[0] = (y[1] - y[0]) / h[0]

    for i in range(1, n):
        c[i] = y[i]
        b[i] = 2 * a[i - 1] * h[i - 1] + b[i - 1]
        a[i] = (y[i + 1] - y[i] - b[i] * h[i]) / (h[i] ** 2)

    return a, b, c, h


def integrale_spline_quadratique(f, a, b, n_points=20):
    x_pts = np.linspace(a, b, n_points)
    y_pts = f(x_pts)

    a_coeff, b_coeff, c_coeff, h = calculer_spline_quadratique(x_pts, y_pts)

    integrale = 0.0
    for i in range(len(h)):
        integrale += (a_coeff[i] * h[i] ** 3 / 3) + (b_coeff[i] * h[i] ** 2 / 2) + (c_coeff[i] * h[i])

    return integrale


# ====================== Fonction de présentation ======================
familles_methodes = {"lag":"Gauss-Laguerre", "leg":"Gauss-Legendre", "cheb":"Gauss-Chebyshev", "sim":"Simpson", "spline":"Spline Quadratique"}

def presentation(erreurs, durees, titre, methodes=None, n_values=None, use_log=True):

    if methodes is None or n_values is None:
        raise ValueError("methodes et n_values doivent être fournis")

    plt.figure(figsize=(16, 6))

    plt.subplot(1, 2, 1)
    for m in methodes:
        x = np.array(n_values)
        y = np.array(erreurs[m])
        mask = ~np.isnan(y)
        if use_log:
            plt.semilogy(x[mask], y[mask], 'o-', label=familles_methodes[m], linewidth=2, markersize=6)
        else:
            plt.plot(x[mask], y[mask], 'o-', label=familles_methodes[m], linewidth=2, markersize=6)

    plt.title("Erreur (log)")
    plt.xlabel("Nombre de points (n)")
    plt.xticks(n_values)
    plt.ylabel("Erreur absolue (log)")
    plt.legend(fontsize=10)
    plt.grid(True, which="both", ls="--", alpha=0.7)

    plt.subplot(1, 2, 2)
    for m in methodes:
        x = np.array(n_values)
        y = np.array(durees[m])
        mask = ~np.isnan(y)
        plt.plot(x[mask], y[mask], 'o-', label=familles_methodes[m], linewidth=2, markersize=6)

    plt.title("Temps d'exécution")
    plt.xlabel("Nombre de points (n)")
    plt.xticks(n_values)
    plt.ylabel("Durée (secondes)")
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.7)

    plt.suptitle(titre, fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# ====================== Programme principal ======================

if __name__ == "__main__":
    n_values = list(range(2, 22, 2))

    # 1. Gauss-Laguerre
    print("=== 1. Exemple Gauss-Laguerre (∫_0^∞ e^{-x} x² dx = 2) ===")
    f_lag = lambda x: x ** 2
    exact_lag = 2.0

    methodes = ["lag", "leg", "sim", "spline"]
    erreurs = {m: [] for m in methodes}
    durees = {m: [] for m in methodes}

    for n in n_values:

        #Laguerre
        start = time.time()
        approx = gauss_laguerre_integral(f_lag, n)
        durees['lag'].append(time.time() - start)
        erreurs['lag'].append(abs(approx - exact_lag))

        #Legendre
        start = time.time()
        approx = gauss_legendre_integral(f_lag, n, a=0, b=100)
        durees['leg'].append(time.time() - start)
        erreurs['leg'].append(abs(approx - exact_lag))

        #Simpson
        start = time.time()
        approx = simpson_integral(f_lag, n, a=0, b=100)
        durees['sim'].append(time.time() - start)
        erreurs['sim'].append(abs(approx - exact_lag))

        #Spline
        start = time.time()
        approx = integrale_spline_quadratique(f_lag, a=0, b=100, n_points=n)
        durees['spline'].append(time.time() - start)
        erreurs['spline'].append(abs(approx - exact_lag))

    presentation(erreurs, durees, "Gauss-Laguerre - x² sur [0, ∞)", methodes=methodes, n_values=n_values)

    # 2. Gauss-Legendre
    print("\n=== 2. Exemple Gauss-Legendre (∫_{-1}^1 cos(x) dx) ===")
    f_leg = lambda x: np.cos(x)
    exact_leg = 2 * np.sin(1)

    methodes = ["leg", "sim", "spline"]
    erreurs = {m: [] for m in methodes}
    durees = {m: [] for m in methodes}

    for n in n_values:
        #Legendre
        start = time.time()
        approx = gauss_legendre_integral(f_leg, n, -1, 1)
        durees['leg'].append(time.time() - start)
        erreurs['leg'].append(abs(approx - exact_leg))

        #Simpson
        start = time.time()
        approx = simpson_integral(f_leg, n, -1, 1)
        durees['sim'].append(time.time() - start)
        erreurs['sim'].append(abs(approx - exact_leg))

        #Spline
        start = time.time()
        approx = integrale_spline_quadratique(f_leg, -1, 1, n_points=n)
        durees['spline'].append(time.time() - start)
        erreurs['spline'].append(abs(approx - exact_leg))

    presentation(erreurs, durees, "Gauss-Legendre - cos(x) sur [-1,1]", methodes=["leg", "sim", "spline"], n_values=n_values)

    # 3. Gauss-Chebyshev
    print("\n=== 3. Exemple Gauss-Chebyshev (∫_{-1}^1 x^4 / √(1-x²) dx = 3π/8) ===")
    f_cheb = lambda x: x ** 4
    exact_cheb = 3 * np.pi / 8

    methodes = ["cheb", "leg", "sim", "spline"]
    erreurs = {m: [] for m in methodes}
    durees = {m: [] for m in methodes}

    for n in n_values:
        #Chebyshev
        start = time.time()
        approx = gauss_chebyshev_integral(f_cheb, n)
        durees['cheb'].append(time.time() - start)
        erreurs['cheb'].append(abs(approx - exact_cheb))

        f_adapt = lambda x: f_cheb(x) * np.sqrt(1 - x ** 2)

        #Legendre
        start = time.time()
        approx = gauss_legendre_integral(f_adapt, n, -1, 1)
        durees['leg'].append(time.time() - start)
        erreurs['leg'].append(abs(approx - exact_cheb))

        #Simpson
        start = time.time()
        approx = simpson_integral(f_adapt, n, -1, 1)
        durees['sim'].append(time.time() - start)
        erreurs['sim'].append(abs(approx - exact_cheb))

        #Spline
        start = time.time()
        approx = integrale_spline_quadratique(f_adapt, -1, 1, n_points=n)
        durees['spline'].append(time.time() - start)
        erreurs['spline'].append(abs(approx - exact_cheb))

    presentation(erreurs, durees, "Gauss-Chebyshev - x^4 / √(1-x²)", methodes=["leg", "cheb", "sim", "spline"], n_values=n_values)

    # 5. Simpson
    print("\n=== 5. Exemple Simpson (∫_0^π sin(x) dx = 2) ===")
    f_sim = lambda x: np.sin(x)
    exact_sim = 2.0

    methodes = ["leg", "sim", "spline"]
    erreurs = {m: [] for m in methodes}
    durees = {m: [] for m in methodes}

    for n in n_values:
        #Legendre
        start = time.time()
        approx = gauss_legendre_integral(f_sim, n, 0, np.pi)
        durees['leg'].append(time.time() - start)
        erreurs['leg'].append(abs(approx - exact_sim))

        #Simpson
        start = time.time()
        approx = simpson_integral(f_sim, n, a=0, b=np.pi)
        durees['sim'].append(time.time() - start)
        erreurs['sim'].append(abs(approx - exact_sim))

        #spline
        start = time.time()
        approx = integrale_spline_quadratique(f_sim, 0, np.pi, n_points=n)
        durees['spline'].append(time.time() - start)
        erreurs['spline'].append(abs(approx - exact_sim))

    presentation(erreurs, durees, "Simpson - sin(x) sur [0, π]", methodes=["leg", "sim", "spline"], n_values=n_values)

    # 6. Exemple favorable à la Spline - Fonction de Runge
    print("\n=== 6. Exemple favorable à la Spline - Fonction de Runge ===")
    f_spline = lambda x: 1 / (1 + 25 * x ** 2)
    exact_runge = np.pi / 10

    methodes = ["leg", "sim", "spline"]
    erreurs = {m: [] for m in methodes}
    durees = {m: [] for m in methodes}

    for n in n_values:
        #Legendre
        start = time.time()
        approx = gauss_legendre_integral(f_spline, n, -1, 1)
        durees['leg'].append(time.time() - start)
        erreurs['leg'].append(abs(approx - exact_runge))

        #Simpson
        start = time.time()
        approx = simpson_integral(f_spline, n, -1, 1)
        durees['sim'].append(time.time() - start)
        erreurs['sim'].append(abs(approx - exact_runge))

        #Spline
        start = time.time()
        approx = integrale_spline_quadratique(f_spline, -1, 1, n_points=n)
        durees['spline'].append(time.time() - start)
        erreurs['spline'].append(abs(approx - exact_runge))

    presentation(erreurs, durees, "Spline Quadratique - Fonction de Runge 1/(1+25x²) sur [-1,1]", methodes=["leg", "sim", "spline"], n_values=n_values, use_log=False)
    print("\nToutes les comparaisons sont terminées !")
