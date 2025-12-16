import numpy as np
import matplotlib.pyplot as plt
import time


def runge_kutta(f, x0, y0, h, N):
    x = np.zeros(N + 1)
    y = np.zeros(N + 1)
    x[0] = x0
    y[0] = y0
    for n in range(N):
        x[n + 1] = x[n] + h
        k1 = h * f(x[n], y[n])
        k2 = h * f(x[n] + h / 2, y[n] + k1 / 2)
        k3 = h * f(x[n] + h / 2, y[n] + k2 / 2)
        k4 = h * f(x[n] + h, y[n] + k3)
        y[n + 1] = y[n] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x, y


def representation(f, x0, y0, h_list, exact=None):
    for h in h_list:
        N = int(6 / h)

        start_time = time.perf_counter()
        x, y_num = runge_kutta(f, x0, y0, h, N)
        end_time = time.perf_counter()
        duration = end_time - start_time

        y_exact = exact(x)
        erreur_max = np.max(np.abs(y_num - y_exact))
        erreur_l2 = np.sqrt(np.mean((y_num - y_exact) ** 2))

        print(f"Méthode de Runge-Kutta - h = {h}")
        print(f"  Temps d'exécution : {duration:.6f} secondes")
        print(f"  Erreur maximale    : {erreur_max:.6e}")
        print(f"  Erreur L2          : {erreur_l2:.6e}")
        print("-" * 50)

        plt.figure()
        plt.plot(x, y_num, 'r-o', label=f'RK4 h={h}')
        plt.plot(x, y_exact, 'b--', label='Exacte')
        plt.title(f'Méthode de Runge-Kutta (h = {h})')
        plt.xlabel('x')
        plt.ylabel('z(x)')
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    def f(x, y):
        return np.pi * np.cos(np.pi * x) * y


    def exact(x):
        return np.exp(np.sin(np.pi * x))


    x0 = 0
    y0 = 1
    h_list = [0.5, 0.3]  # Pages 154-155
    representation(f, x0, y0, h_list, exact=exact)