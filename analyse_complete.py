"""
Script d'analyse complète pour le projet d'analyse numérique
Génère toutes les figures et effectue toutes les analyses comparatives
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import sys

# Configuration LaTeX pour les figures
rc('font', family='serif', size=12)
rc('text', usetex=False)
rc('figure', figsize=(10, 6))

# Import des méthodes d'équations différentielles
from equa_diff import euler, heun, runge_kunta

# Import des méthodes d'intégration
from integral import integral

# Dossier de sauvegarde des figures
FIGURES_DIR = "presentation/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

print("="*80)
print("ANALYSE NUMÉRIQUE COMPLÈTE")
print("="*80)
print()

# =============================================================================
# PARTIE 1 : ÉQUATIONS DIFFÉRENTIELLES
# =============================================================================

print("\n" + "="*80)
print("PARTIE 1 : ANALYSE DES MÉTHODES DE RÉSOLUTION D'ÉQUATIONS DIFFÉRENTIELLES")
print("="*80)

# Problème test : y' = π cos(πx) y, y(0) = 1
# Solution exacte : y(x) = exp(sin(πx))

def f_edo(x, y):
    """Fonction du second membre de l'EDO"""
    return np.pi * np.cos(np.pi * x) * y

def sol_exacte_edo(x):
    """Solution exacte de l'EDO"""
    return np.exp(np.sin(np.pi * x))

# Paramètres de simulation
x0 = 0
y0 = 1
h_values = [0.5, 0.3, 0.15, 0.06]  # Différents pas de temps
x_final = 6

print("\nProblème considéré:")
print("  y' = π cos(πx) y")
print("  y(0) = 1")
print("  Solution exacte: y(x) = exp(sin(πx))")
print(f"  Intervalle: [0, {x_final}]")
print()

# Stockage des résultats pour comparaison
resultats_edo = {
    'Euler': {'temps': [], 'erreur_max': [], 'erreur_l2': [], 'h': []},
    'Heun': {'temps': [], 'erreur_max': [], 'erreur_l2': [], 'h': []},
    'RK4': {'temps': [], 'erreur_max': [], 'erreur_l2': [], 'h': []}
}

# --- 1.1 : Comparaison pour chaque pas de temps ---
for h in h_values:
    N = int(x_final / h)
    print(f"\n--- Pas de temps h = {h} (N = {N}) ---")

    # Euler
    start = time.perf_counter()
    x_euler, y_euler = euler.euler(f_edo, x0, y0, h, N)
    t_euler = time.perf_counter() - start
    y_exact_e = sol_exacte_edo(x_euler)
    err_max_e = np.max(np.abs(y_euler - y_exact_e))
    err_l2_e = np.sqrt(np.mean((y_euler - y_exact_e)**2))

    resultats_edo['Euler']['temps'].append(t_euler)
    resultats_edo['Euler']['erreur_max'].append(err_max_e)
    resultats_edo['Euler']['erreur_l2'].append(err_l2_e)
    resultats_edo['Euler']['h'].append(h)

    print(f"Euler:       temps={t_euler:.6f}s, err_max={err_max_e:.6e}, err_L2={err_l2_e:.6e}")

    # Heun
    start = time.perf_counter()
    x_heun, y_heun = heun.heun(f_edo, x0, y0, h, N)
    t_heun = time.perf_counter() - start
    y_exact_h = sol_exacte_edo(x_heun)
    err_max_h = np.max(np.abs(y_heun - y_exact_h))
    err_l2_h = np.sqrt(np.mean((y_heun - y_exact_h)**2))

    resultats_edo['Heun']['temps'].append(t_heun)
    resultats_edo['Heun']['erreur_max'].append(err_max_h)
    resultats_edo['Heun']['erreur_l2'].append(err_l2_h)
    resultats_edo['Heun']['h'].append(h)

    print(f"Heun:        temps={t_heun:.6f}s, err_max={err_max_h:.6e}, err_L2={err_l2_h:.6e}")

    # Runge-Kutta 4
    start = time.perf_counter()
    x_rk, y_rk = runge_kunta.runge_kutta(f_edo, x0, y0, h, N)
    t_rk = time.perf_counter() - start
    y_exact_rk = sol_exacte_edo(x_rk)
    err_max_rk = np.max(np.abs(y_rk - y_exact_rk))
    err_l2_rk = np.sqrt(np.mean((y_rk - y_exact_rk)**2))

    resultats_edo['RK4']['temps'].append(t_rk)
    resultats_edo['RK4']['erreur_max'].append(err_max_rk)
    resultats_edo['RK4']['erreur_l2'].append(err_l2_rk)
    resultats_edo['RK4']['h'].append(h)

    print(f"Runge-Kutta: temps={t_rk:.6f}s, err_max={err_max_rk:.6e}, err_L2={err_l2_rk:.6e}")

    # Graphique: Comparaison des solutions pour ce pas de temps
    plt.figure(figsize=(14, 5))

    plt.subplot(1, 2, 1)
    plt.plot(x_euler, y_euler, 'r-o', label='Euler', markersize=4, linewidth=1.5)
    plt.plot(x_heun, y_heun, 'g-s', label='Heun', markersize=4, linewidth=1.5)
    plt.plot(x_rk, y_rk, 'm-^', label='Runge-Kutta', markersize=4, linewidth=1.5)
    plt.plot(x_euler, y_exact_e, 'b--', label='Solution exacte', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.title(f'Comparaison des méthodes (h = {h})')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.semilogy(x_euler, np.abs(y_euler - y_exact_e), 'r-o', label='Euler', markersize=4)
    plt.semilogy(x_heun, np.abs(y_heun - y_exact_h), 'g-s', label='Heun', markersize=4)
    plt.semilogy(x_rk, np.abs(y_rk - y_exact_rk), 'm-^', label='Runge-Kutta', markersize=4)
    plt.xlabel('x')
    plt.ylabel('Erreur absolue')
    plt.title(f'Erreur absolue (h = {h})')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/edo_comparaison_h{h:.3f}.pdf', bbox_inches='tight')
    plt.savefig(f'{FIGURES_DIR}/edo_comparaison_h{h:.3f}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  → Figure sauvegardée: edo_comparaison_h{h:.3f}.pdf/png")

# --- 1.2 : Étude de convergence ---
print("\n--- Étude de convergence ---")

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
for methode in ['Euler', 'Heun', 'RK4']:
    h_vals = resultats_edo[methode]['h']
    err_max = resultats_edo[methode]['erreur_max']
    plt.loglog(h_vals, err_max, 'o-', label=methode, linewidth=2, markersize=8)

# Droites de référence pour les ordres de convergence
h_ref = np.array(h_values)
plt.loglog(h_ref, 0.5*h_ref**1, 'k--', alpha=0.5, linewidth=1, label='Ordre 1')
plt.loglog(h_ref, 0.1*h_ref**2, 'k-.', alpha=0.5, linewidth=1, label='Ordre 2')
plt.loglog(h_ref, 0.01*h_ref**4, 'k:', alpha=0.5, linewidth=1, label='Ordre 4')

plt.xlabel('Pas de temps h')
plt.ylabel('Erreur maximale')
plt.title('Convergence des méthodes')
plt.legend()
plt.grid(True, which='both', alpha=0.3)

plt.subplot(1, 2, 2)
for methode in ['Euler', 'Heun', 'RK4']:
    h_vals = resultats_edo[methode]['h']
    temps = resultats_edo[methode]['temps']
    err_max = resultats_edo[methode]['erreur_max']
    plt.loglog(temps, err_max, 'o-', label=methode, linewidth=2, markersize=8)

plt.xlabel('Temps de calcul (s)')
plt.ylabel('Erreur maximale')
plt.title('Efficacité computationnelle')
plt.legend()
plt.grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/edo_convergence.pdf', bbox_inches='tight')
plt.savefig(f'{FIGURES_DIR}/edo_convergence.png', dpi=300, bbox_inches='tight')
plt.close()
print("  → Figure sauvegardée: edo_convergence.pdf/png")

# --- 1.3 : Tableau récapitulatif ---
print("\n--- Tableau récapitulatif des ordres de convergence ---")
print(f"{'Méthode':<15} {'Ordre théorique':<20} {'Ordre observé':<15}")
print("-" * 50)

for methode in ['Euler', 'Heun', 'RK4']:
    h_vals = np.array(resultats_edo[methode]['h'])
    err_max = np.array(resultats_edo[methode]['erreur_max'])

    # Calcul de l'ordre de convergence observé (régression log-log)
    if len(h_vals) > 1:
        log_h = np.log(h_vals)
        log_err = np.log(err_max)
        ordre_obs = np.polyfit(log_h, log_err, 1)[0]
    else:
        ordre_obs = 0

    ordre_theo = {'Euler': 1, 'Heun': 2, 'RK4': 4}[methode]
    print(f"{methode:<15} {ordre_theo:<20} {ordre_obs:<15.2f}")

# =============================================================================
# PARTIE 2 : INTÉGRATION NUMÉRIQUE
# =============================================================================

print("\n" + "="*80)
print("PARTIE 2 : ANALYSE DES MÉTHODES D'INTÉGRATION NUMÉRIQUE")
print("="*80)

# --- 2.1 : Gauss-Laguerre ---
print("\n--- 2.1 : Gauss-Laguerre : ∫_0^∞ e^{-x} x² dx = 2 ---")
f_lag = lambda x: x**2
exact_lag = 2.0
n_vals = range(2, 22, 2)

resultats_lag = {'n': [], 'approx': [], 'erreur': [], 'temps': []}

for n in n_vals:
    start = time.perf_counter()
    approx = integral.gauss_laguerre_integral(f_lag, n)
    t = time.perf_counter() - start
    err = abs(approx - exact_lag)

    resultats_lag['n'].append(n)
    resultats_lag['approx'].append(approx)
    resultats_lag['erreur'].append(err)
    resultats_lag['temps'].append(t)

    print(f"  n={n:2d}: approx={approx:.12f}, err={err:.6e}, temps={t:.6f}s")

# Graphique Gauss-Laguerre
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.semilogy(resultats_lag['n'], resultats_lag['erreur'], 'o-', linewidth=2, markersize=8, color='darkblue')
plt.xlabel('Nombre de points n')
plt.ylabel('Erreur absolue')
plt.title('Gauss-Laguerre : Convergence')
plt.grid(True, which='both', alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(resultats_lag['n'], resultats_lag['temps'], 'o-', linewidth=2, markersize=8, color='darkred')
plt.xlabel('Nombre de points n')
plt.ylabel('Temps de calcul (s)')
plt.title('Gauss-Laguerre : Performance')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/int_gauss_laguerre.pdf', bbox_inches='tight')
plt.savefig(f'{FIGURES_DIR}/int_gauss_laguerre.png', dpi=300, bbox_inches='tight')
plt.close()
print("  → Figure sauvegardée: int_gauss_laguerre.pdf/png")

# --- 2.2 : Gauss-Legendre ---
print("\n--- 2.2 : Gauss-Legendre : ∫_{-1}^1 cos(x) dx = 2sin(1) ---")
f_leg = lambda x: np.cos(x)
exact_leg = 2 * np.sin(1)

resultats_leg = {'n': [], 'approx': [], 'erreur': [], 'temps': []}

for n in n_vals:
    start = time.perf_counter()
    approx = integral.gauss_legendre_integral(f_leg, n, -1, 1)
    t = time.perf_counter() - start
    err = abs(approx - exact_leg)

    resultats_leg['n'].append(n)
    resultats_leg['approx'].append(approx)
    resultats_leg['erreur'].append(err)
    resultats_leg['temps'].append(t)

    print(f"  n={n:2d}: approx={approx:.12f}, err={err:.6e}, temps={t:.6f}s")

# Graphique Gauss-Legendre
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.semilogy(resultats_leg['n'], resultats_leg['erreur'], 'o-', linewidth=2, markersize=8, color='darkgreen')
plt.xlabel('Nombre de points n')
plt.ylabel('Erreur absolue')
plt.title('Gauss-Legendre : Convergence')
plt.grid(True, which='both', alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(resultats_leg['n'], resultats_leg['temps'], 'o-', linewidth=2, markersize=8, color='darkorange')
plt.xlabel('Nombre de points n')
plt.ylabel('Temps de calcul (s)')
plt.title('Gauss-Legendre : Performance')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/int_gauss_legendre.pdf', bbox_inches='tight')
plt.savefig(f'{FIGURES_DIR}/int_gauss_legendre.png', dpi=300, bbox_inches='tight')
plt.close()
print("  → Figure sauvegardée: int_gauss_legendre.pdf/png")

# --- 2.3 : Gauss-Chebyshev ---
print("\n--- 2.3 : Gauss-Chebyshev : ∫_{-1}^1 x^4 / √(1-x²) dx = 3π/8 ---")
f_cheb = lambda x: x**4
exact_cheb = 3 * np.pi / 8

resultats_cheb = {'n': [], 'approx': [], 'erreur': [], 'temps': []}

for n in n_vals:
    start = time.perf_counter()
    approx = integral.gauss_chebyshev_integral(f_cheb, n)
    t = time.perf_counter() - start
    err = abs(approx - exact_cheb)

    resultats_cheb['n'].append(n)
    resultats_cheb['approx'].append(approx)
    resultats_cheb['erreur'].append(err)
    resultats_cheb['temps'].append(t)

    print(f"  n={n:2d}: approx={approx:.12f}, err={err:.6e}, temps={t:.6f}s")

# Graphique Gauss-Chebyshev
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.semilogy(resultats_cheb['n'], resultats_cheb['erreur'], 'o-', linewidth=2, markersize=8, color='purple')
plt.xlabel('Nombre de points n')
plt.ylabel('Erreur absolue')
plt.title('Gauss-Chebyshev : Convergence')
plt.grid(True, which='both', alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(resultats_cheb['n'], resultats_cheb['temps'], 'o-', linewidth=2, markersize=8, color='brown')
plt.xlabel('Nombre de points n')
plt.ylabel('Temps de calcul (s)')
plt.title('Gauss-Chebyshev : Performance')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/int_gauss_chebyshev.pdf', bbox_inches='tight')
plt.savefig(f'{FIGURES_DIR}/int_gauss_chebyshev.png', dpi=300, bbox_inches='tight')
plt.close()
print("  → Figure sauvegardée: int_gauss_chebyshev.pdf/png")

# --- 2.4 : Simpson ---
print("\n--- 2.4 : Simpson : ∫_0^π sin(x) dx = 2 ---")
f_sim = lambda x: np.sin(x)
exact_sim = 2.0

resultats_sim = {'n': [], 'approx': [], 'erreur': [], 'temps': []}

for n in n_vals:
    start = time.perf_counter()
    approx = integral.simpson_integral(f_sim, 0, np.pi, n)
    t = time.perf_counter() - start
    err = abs(approx - exact_sim)

    resultats_sim['n'].append(n)
    resultats_sim['approx'].append(approx)
    resultats_sim['erreur'].append(err)
    resultats_sim['temps'].append(t)

    print(f"  n={n:2d}: approx={approx:.12f}, err={err:.6e}, temps={t:.6f}s")

# Graphique Simpson
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.semilogy(resultats_sim['n'], resultats_sim['erreur'], 'o-', linewidth=2, markersize=8, color='teal')
plt.xlabel('Nombre de points n')
plt.ylabel('Erreur absolue')
plt.title('Simpson : Convergence')
plt.grid(True, which='both', alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(resultats_sim['n'], resultats_sim['temps'], 'o-', linewidth=2, markersize=8, color='olive')
plt.xlabel('Nombre de points n')
plt.ylabel('Temps de calcul (s)')
plt.title('Simpson : Performance')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/int_simpson.pdf', bbox_inches='tight')
plt.savefig(f'{FIGURES_DIR}/int_simpson.png', dpi=300, bbox_inches='tight')
plt.close()
print("  → Figure sauvegardée: int_simpson.pdf/png")

# --- 2.5 : Spline Quadratique ---
print("\n--- 2.5 : Spline Quadratique : ∫_{-1}^1 1/(1+25x²) dx = π/10 (Fonction de Runge) ---")
f_runge = lambda x: 1 / (1 + 25 * x**2)
exact_runge = np.pi / 10

resultats_spline = {'n': [], 'approx': [], 'erreur': [], 'temps': []}

for n in n_vals:
    start = time.perf_counter()
    approx = integral.integrale_spline_quadratique(f_runge, -1, 1, n_points=n)
    t = time.perf_counter() - start
    err = abs(approx - exact_runge)

    resultats_spline['n'].append(n)
    resultats_spline['approx'].append(approx)
    resultats_spline['erreur'].append(err)
    resultats_spline['temps'].append(t)

    print(f"  n={n:2d}: approx={approx:.12f}, err={err:.6e}, temps={t:.6f}s")

# Graphique Spline
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.semilogy(resultats_spline['n'], resultats_spline['erreur'], 'o-', linewidth=2, markersize=8, color='crimson')
plt.xlabel('Nombre de points n')
plt.ylabel('Erreur absolue')
plt.title('Spline Quadratique : Convergence')
plt.grid(True, which='both', alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(resultats_spline['n'], resultats_spline['temps'], 'o-', linewidth=2, markersize=8, color='navy')
plt.xlabel('Nombre de points n')
plt.ylabel('Temps de calcul (s)')
plt.title('Spline Quadratique : Performance')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/int_spline.pdf', bbox_inches='tight')
plt.savefig(f'{FIGURES_DIR}/int_spline.png', dpi=300, bbox_inches='tight')
plt.close()
print("  → Figure sauvegardée: int_spline.pdf/png")

# --- 2.6 : Comparaison globale des méthodes d'intégration ---
print("\n--- 2.6 : Comparaison globale sur cos(x) sur [-1, 1] ---")

resultats_comp = {
    'Gauss-Legendre': {'n': [], 'erreur': [], 'temps': []},
    'Gauss-Chebyshev': {'n': [], 'erreur': [], 'temps': []},
    'Simpson': {'n': [], 'erreur': [], 'temps': []},
    'Spline': {'n': [], 'erreur': [], 'temps': []}
}

f_comp = lambda x: np.cos(x)
exact_comp = 2 * np.sin(1)

for n in n_vals:
    # Gauss-Legendre
    start = time.perf_counter()
    approx = integral.gauss_legendre_integral(f_comp, n, -1, 1)
    t = time.perf_counter() - start
    resultats_comp['Gauss-Legendre']['n'].append(n)
    resultats_comp['Gauss-Legendre']['erreur'].append(abs(approx - exact_comp))
    resultats_comp['Gauss-Legendre']['temps'].append(t)

    # Gauss-Chebyshev (adapter la fonction)
    f_adapt = lambda x: f_comp(x) * np.sqrt(1 - x**2)
    start = time.perf_counter()
    approx = integral.gauss_chebyshev_integral(f_adapt, n)
    t = time.perf_counter() - start
    resultats_comp['Gauss-Chebyshev']['n'].append(n)
    resultats_comp['Gauss-Chebyshev']['erreur'].append(abs(approx - exact_comp))
    resultats_comp['Gauss-Chebyshev']['temps'].append(t)

    # Simpson
    start = time.perf_counter()
    approx = integral.simpson_integral(f_comp, -1, 1, n)
    t = time.perf_counter() - start
    resultats_comp['Simpson']['n'].append(n)
    resultats_comp['Simpson']['erreur'].append(abs(approx - exact_comp))
    resultats_comp['Simpson']['temps'].append(t)

    # Spline
    start = time.perf_counter()
    approx = integral.integrale_spline_quadratique(f_comp, -1, 1, n_points=n)
    t = time.perf_counter() - start
    resultats_comp['Spline']['n'].append(n)
    resultats_comp['Spline']['erreur'].append(abs(approx - exact_comp))
    resultats_comp['Spline']['temps'].append(t)

# Graphique comparatif
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
for methode, color in zip(['Gauss-Legendre', 'Gauss-Chebyshev', 'Simpson', 'Spline'],
                           ['blue', 'green', 'red', 'purple']):
    plt.semilogy(resultats_comp[methode]['n'], resultats_comp[methode]['erreur'],
                 'o-', label=methode, linewidth=2, markersize=6, color=color)
plt.xlabel('Nombre de points n')
plt.ylabel('Erreur absolue')
plt.title('Comparaison : Convergence sur cos(x)')
plt.legend()
plt.grid(True, which='both', alpha=0.3)

plt.subplot(1, 2, 2)
for methode, color in zip(['Gauss-Legendre', 'Gauss-Chebyshev', 'Simpson', 'Spline'],
                           ['blue', 'green', 'red', 'purple']):
    plt.loglog(resultats_comp[methode]['temps'], resultats_comp[methode]['erreur'],
               'o-', label=methode, linewidth=2, markersize=6, color=color)
plt.xlabel('Temps de calcul (s)')
plt.ylabel('Erreur absolue')
plt.title('Comparaison : Efficacité computationnelle')
plt.legend()
plt.grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/int_comparaison_globale.pdf', bbox_inches='tight')
plt.savefig(f'{FIGURES_DIR}/int_comparaison_globale.png', dpi=300, bbox_inches='tight')
plt.close()
print("  → Figure sauvegardée: int_comparaison_globale.pdf/png")

# =============================================================================
# RÉSUMÉ FINAL
# =============================================================================

print("\n" + "="*80)
print("RÉSUMÉ DE L'ANALYSE")
print("="*80)

print("\n--- ÉQUATIONS DIFFÉRENTIELLES ---")
print("\nOrdres de convergence observés :")
for methode in ['Euler', 'Heun', 'RK4']:
    h_vals = np.array(resultats_edo[methode]['h'])
    err_max = np.array(resultats_edo[methode]['erreur_max'])
    if len(h_vals) > 1:
        log_h = np.log(h_vals)
        log_err = np.log(err_max)
        ordre_obs = np.polyfit(log_h, log_err, 1)[0]
    else:
        ordre_obs = 0
    ordre_theo = {'Euler': 1, 'Heun': 2, 'RK4': 4}[methode]
    print(f"  {methode}: ordre théorique = {ordre_theo}, ordre observé = {ordre_obs:.2f}")

print("\nMeilleure méthode (précision) : RK4")
print("Meilleure méthode (efficacité) : Heun (bon compromis)")

print("\n--- INTÉGRATION NUMÉRIQUE ---")
print("\nConvergence spectrale (exponentielle) :")
print("  - Gauss-Laguerre, Gauss-Legendre, Gauss-Chebyshev")
print("\nConvergence algébrique :")
print("  - Simpson (ordre 4)")
print("  - Spline quadratique (ordre 3)")

print("\nMeilleure méthode (précision) : Quadratures de Gauss")
print("Meilleure méthode (robustesse) : Simpson")

print("\n" + "="*80)
print("ANALYSE TERMINÉE")
print(f"Toutes les figures ont été sauvegardées dans : {FIGURES_DIR}/")
print("="*80)

