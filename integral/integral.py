import numpy as np
from scipy.special import roots_laguerre
from numpy.polynomial.legendre import leggauss
import time
import matplotlib.pyplot as plt


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


def simpson_integral(f, a, b, n):
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

def presentation(erreurs, durees, titre):
    n_values = sorted(erreurs.keys())
    methodes = ["Gauss-Laguerre", "Gauss-Legendre", "Gauss-Chebyshev", "Simpson", "Spline Quadratique"]

    plt.figure(figsize=(16, 6))

    plt.subplot(1, 2, 1)
    for i, methode in enumerate(methodes):
        errs = [erreurs[n][i] for n in n_values]
        plt.semilogy(n_values, errs, 'o-', label=methode, linewidth=2, markersize=6)
    plt.title("Erreur absolue")
    plt.xlabel("n (ou nombre de points)")
    plt.ylabel("Erreur absolue (log)")
    plt.legend(fontsize=10)
    plt.grid(True, which="both", ls="--", alpha=0.7)

    plt.subplot(1, 2, 2)
    for i, methode in enumerate(methodes):
        tps = [durees[n][i] for n in n_values]
        plt.plot(n_values, tps, 'o-', label=methode, linewidth=2, markersize=6)
    plt.title("Temps d'exécution")
    plt.xlabel("n (ou nombre de points)")
    plt.ylabel("Durée (secondes)")
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.7)

    plt.suptitle(titre, fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# ====================== Programme principal ======================

if __name__ == "__main__":
    n_values = range(2, 22, 2)

    # 1. Gauss-Laguerre
    print("=== 1. Exemple Gauss-Laguerre (∫_0^∞ e^{-x} x² dx = 2) ===")
    f_lag = lambda x: x ** 2
    exact_lag = 2.0
    erreurs, durees = {}, {}
    for n in n_values:
        erreurs[n] = []
        durees[n] = []
        start = time.time()
        approx = gauss_laguerre_integral(f_lag, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_lag))
        erreurs[n].extend([np.nan] * 4)
        durees[n].extend([np.nan] * 4)
    presentation(erreurs, durees, "Gauss-Laguerre - x² sur [0, ∞)")

    # 2. Gauss-Legendre
    print("\n=== 2. Exemple Gauss-Legendre (∫_{-1}^1 cos(x) dx) ===")
    f_leg = lambda x: np.cos(x)
    exact_leg = 2 * np.sin(1)
    erreurs, durees = {}, {}
    for n in n_values:
        erreurs[n] = [np.nan]
        durees[n] = [np.nan]
        start = time.time()
        approx = gauss_legendre_integral(f_leg, n, -1, 1)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_leg))
        f_adapt = lambda x: np.cos(x) * np.sqrt(1 - x ** 2)
        start = time.time()
        approx = gauss_chebyshev_integral(f_adapt, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_leg))
        start = time.time()
        approx = simpson_integral(f_leg, -1, 1, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_leg))
        start = time.time()
        approx = integrale_spline_quadratique(f_leg, -1, 1, n_points=n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_leg))
    presentation(erreurs, durees, "Gauss-Legendre - cos(x) sur [-1,1]")

    # 3. Gauss-Chebyshev
    print("\n=== 3. Exemple Gauss-Chebyshev (∫_{-1}^1 x^4 / √(1-x²) dx = 3π/8) ===")
    f_cheb = lambda x: x ** 4
    exact_cheb = 3 * np.pi / 8
    erreurs, durees = {}, {}
    for n in n_values:
        erreurs[n] = [np.nan]
        durees[n] = [np.nan]
        start = time.time()
        approx = gauss_legendre_integral(f_cheb, n, -1, 1)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_cheb))
        start = time.time()
        approx = gauss_chebyshev_integral(f_cheb, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_cheb))
        start = time.time()
        approx = simpson_integral(lambda x: f_cheb(x) / np.sqrt(1 - x ** 2 + 1e-12), -1, 1, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_cheb))
        start = time.time()
        approx = integrale_spline_quadratique(lambda x: f_cheb(x) / np.sqrt(1 - x ** 2 + 1e-12), -1, 1, n_points=n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_cheb))
    presentation(erreurs, durees, "Gauss-Chebyshev - x^4 / √(1-x²)")

    # 4. NOUVEL EXEMPLE : Combinaison Gauss-Laguerre + Gauss-Chebyshev
    print("\n=== 4. Combinaison Gauss-Laguerre & Gauss-Chebyshev : ∫_{-1}^1 e^{-x} / √(1-x²) dx ===")
    f_comb = lambda x: np.exp(-x)
    # Fonction adaptée pour Chebyshev : le poids 1/√(1-x²) est déjà inclus
    f_cheb_comb = lambda x: np.exp(-x)

    # On utilise Gauss-Chebyshev comme référence très précise (convergence spectrale)
    ref_approx = gauss_chebyshev_integral(f_cheb_comb, 100)  # n très grand pour référence

    erreurs, durees = {}, {}
    for n in n_values:
        erreurs[n] = [np.nan]  # Laguerre non applicable
        durees[n] = [np.nan]

        # Legendre
        start = time.time()
        approx = gauss_legendre_integral(f_comb, n, -1, 1)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - ref_approx))

        # Chebyshev (optimal ici)
        start = time.time()
        approx = gauss_chebyshev_integral(f_cheb_comb, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - ref_approx))

        # Simpson
        start = time.time()
        approx = simpson_integral(lambda x: f_comb(x) / np.sqrt(1 - x ** 2 + 1e-12), -1, 1, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - ref_approx))

        # Spline
        start = time.time()
        approx = integrale_spline_quadratique(lambda x: f_comb(x) / np.sqrt(1 - x ** 2 + 1e-12), -1, 1, n_points=n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - ref_approx))

    presentation(erreurs, durees, "Combinaison Laguerre-Chebyshev : ∫ e^{-x} / √(1-x²) dx sur [-1,1]")

    # 5. Simpson
    print("\n=== 5. Exemple Simpson (∫_0^π sin(x) dx = 2) ===")
    f_sim = lambda x: np.sin(x)
    exact_sim = 2.0
    erreurs, durees = {}, {}
    for n in n_values:
        erreurs[n] = [np.nan]
        durees[n] = [np.nan]
        start = time.time()
        approx = gauss_legendre_integral(f_sim, n, 0, np.pi)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_sim))
        erreurs[n].append(np.nan)
        durees[n].append(np.nan)
        start = time.time()
        approx = simpson_integral(f_sim, 0, np.pi, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_sim))
        start = time.time()
        approx = integrale_spline_quadratique(f_sim, 0, np.pi, n_points=n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_sim))
    presentation(erreurs, durees, "Simpson - sin(x) sur [0, π]")

    # 6. Exemple favorable à la Spline - Fonction de Runge
    print("\n=== 6. Exemple favorable à la Spline - Fonction de Runge ===")
    f_runge = lambda x: 1 / (1 + 25 * x ** 2)
    exact_runge = np.pi / 10
    erreurs, durees = {}, {}
    for n in n_values:
        erreurs[n] = [np.nan]
        durees[n] = [np.nan]
        start = time.time()
        approx = gauss_legendre_integral(f_runge, n, -1, 1)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_runge))
        f_adapt_runge = lambda x: f_runge(x) * np.sqrt(1 - x ** 2)
        start = time.time()
        approx = gauss_chebyshev_integral(f_adapt_runge, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_runge))
        start = time.time()
        approx = simpson_integral(f_runge, -1, 1, n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_runge))
        start = time.time()
        approx = integrale_spline_quadratique(f_runge, -1, 1, n_points=n)
        durees[n].append(time.time() - start)
        erreurs[n].append(abs(approx - exact_runge))
    presentation(erreurs, durees, "Spline Quadratique - Fonction de Runge 1/(1+25x²) sur [-1,1]")

    print("\nToutes les comparaisons sont terminées !")