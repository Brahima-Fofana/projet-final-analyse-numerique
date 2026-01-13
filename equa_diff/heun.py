import numpy as np
import matplotlib.pyplot as plt
import time


def heun(f, x0, y0, h, nb_max_point):
    x = np.zeros(nb_max_point + 1)
    y = np.zeros(nb_max_point + 1)
    x[0] = x0
    y[0] = y0
    for n in range(nb_max_point):
        x[n + 1] = x[n] + h
        k1 = f(x[n], y[n])
        k2 = f(x[n] + h / 2, y[n] + (h / 2) * k1)
        y[n + 1] = y[n] + h * k2
    return x, y


def representation(f, x0, y0, h_list, exact=None, x_max=6):
    for h in h_list:
        nb_max_point = int((x_max - x0) / h)

        # Mesure du temps
        start_time = time.perf_counter()
        x, y = heun(f, x0, y0, h, nb_max_point)
        end_time = time.perf_counter()
        duration = end_time - start_time

        #Solution Exacte
        y_exact = exact(x)

        # Calcul des erreurs
        erreur_max = np.max(np.abs(y - y_exact))
        erreur_l2 = np.sqrt(np.mean((y - y_exact) ** 2))

        # Affichage dans la console
        print(f"Méthode d'Euler - h = {h}")
        print(f"  Temps d'exécution : {duration:.6f} secondes")
        print(f"  Erreur maximale    : {erreur_max:.6e}")
        print(f"  Erreur moyenne          : {erreur_l2:.6e}")
        print("-" * 50)

        x_exacte_lisse = np.linspace(x0, x_max, 100)
        y_exacte_lisse = exact(x_exacte_lisse)

        # Graphe
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'r-o', label=f'Heun h={h}')
        plt.plot(x_exacte_lisse, y_exacte_lisse, 'b--', label='Solution Exacte')
        plt.title(f'Méthode d\'Heun (h = {h})')
        plt.xlabel('x')
        plt.ylabel('z(x)')
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    def f(x, z):
        return np.pi * np.cos(np.pi * x) * z


    def exact(x):
        return np.exp(np.sin(np.pi * x))


    x0 = 0
    y0 = 1
    h_list = [0.3, 0.15, 0.06]  # Pages 93-95
    representation(f, x0, y0, h_list, exact=exact)