import numpy as np
from scipy import integrate


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

if __name__ == "__main__":
    print("==" * 50)
    print("Test spline")

    fct = lambda x : 1/x**3
    resultat = integrale_spline_quadratique(fct, 1, 20)
    print(f"Resultat spline : {resultat}")

    I, err = integrate.quad(fct, 1, 20)
    print(f"Resultat exacte : {I}")

    print(f"Erreur absolue : {np.abs(resultat - I):5f}")



