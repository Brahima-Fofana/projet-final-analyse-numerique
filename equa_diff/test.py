import time
import numpy as np
from matplotlib import pyplot as plt
from equa_diff import euler, heun, runge_kunta  # je suppose que tes fichiers s'appellent comme ça


def representation(f, x0, y0, h_list, exact=None):
    for h in h_list:
        N = int(6 / h)

        # --- Euler ---
        start_time = time.perf_counter()
        x_euler, y_euler = euler.euler(f, x0, y0, h, N)
        duration_euler = time.perf_counter() - start_time
        err_max_e = np.max(np.abs(y_euler - exact(x_euler)))
        err_l2_e = np.sqrt(np.mean((y_euler - exact(x_euler)) ** 2))
        print(f"Euler - h = {h}")
        print(f"  Temps : {duration_euler:.6f} s")
        print(f"  Erreur max : {err_max_e:.6e}")
        print(f"  Erreur L2  : {err_l2_e:.6e}")
        print("-" * 50)

        # --- Heun ---
        start_time = time.perf_counter()
        x_heun, y_heun = heun.heun(f, x0, y0, h, N)
        duration_heun = time.perf_counter() - start_time
        err_max_h = np.max(np.abs(y_heun - exact(x_heun)))
        err_l2_h = np.sqrt(np.mean((y_heun - exact(x_heun)) ** 2))
        print(f"Heun - h = {h}")
        print(f"  Temps : {duration_heun:.6f} s")
        print(f"  Erreur max : {err_max_h:.6e}")
        print(f"  Erreur L2  : {err_l2_h:.6e}")
        print("-" * 50)

        # --- Runge-Kutta ---
        start_time = time.perf_counter()
        x_rk, y_rk = runge_kunta.runge_kutta(f, x0, y0, h, N)
        duration_rk = time.perf_counter() - start_time
        err_max_rk = np.max(np.abs(y_rk - exact(x_rk)))
        err_l2_rk = np.sqrt(np.mean((y_rk - exact(x_rk)) ** 2))
        print(f"Runge-Kutta - h = {h}")
        print(f"  Temps : {duration_rk:.6f} s")
        print(f"  Erreur max : {err_max_rk:.6e}")
        print(f"  Erreur L2  : {err_l2_rk:.6e}")
        print("-" * 50)

        # Graphes (un par méthode, ou tous sur le même si tu préfères)
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 3, 1)
        plt.plot(x_euler, y_euler, 'r-o', label=f'Euler h={h}')
        plt.plot(x_euler, exact(x_euler), 'b--', label='Exacte')
        plt.title('Euler')
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 3, 2)
        plt.plot(x_heun, y_heun, 'g-o', label=f'Heun h={h}')
        plt.plot(x_heun, exact(x_heun), 'b--', label='Exacte')
        plt.title('Heun')
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 3, 3)
        plt.plot(x_rk, y_rk, 'm-o', label=f'RK4 h={h}')
        plt.plot(x_rk, exact(x_rk), 'b--', label='Exacte')
        plt.title('Runge-Kutta')
        plt.legend()
        plt.grid(True)

        plt.suptitle(f'Comparaison des méthodes - h = {h}')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    def f(x, y):
        return np.pi * np.cos(np.pi * x) * y


    def exact(x):
        return np.exp(np.sin(np.pi * x))


    x0 = 0
    y0 = 1
    h_list = [0.06, 0.15, 0.3]  # ordre croissant ou décroissant, comme tu veux
    representation(f, x0, y0, h_list, exact=exact)