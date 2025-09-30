#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# --- différences divisées ---
def diff_div(X, Y):
    """Retourne les coefficients a_k de Newton à partir des noeuds X et valeurs Y."""
    X = np.asarray(X, dtype=float)
    T = np.array(Y, dtype=float).copy()
    n = len(X) - 1
    for k in range(1, n + 1):
        T[k:n+1] = (T[k:n+1] - T[k-1:n]) / (X[k:n+1] - X[0:n+1-k])
    return T  # [a0, a1, ..., an]

# --- évaluation emboîtée ---
def newton_eval(X, a, x):
    """Évalue le polynôme de Newton aux points x (scalaire ou vecteur)."""
    X = np.asarray(X, dtype=float)
    a = np.asarray(a, dtype=float)
    p = 0.0
    x = np.asarray(x, dtype=float)
    for k in range(len(a) - 1, -1, -1):
        p = a[k] + (x - X[k]) * p
    return p

# --- construction + tracé ---
def interp_plot(f, a, b, n, nb_points=600, title=None):
    X = np.linspace(a, b, n + 1)
    Y = f(X)
    coeffs = diff_div(X, Y)

    xg = np.linspace(a, b, max(500, nb_points))  # >= 500 points comme demandé
    Pf = newton_eval(X, coeffs, xg)

    plt.figure(figsize=(7, 4))
    plt.plot(xg, f(xg), label="f(x)")
    plt.plot(xg, Pf, "--", label=f"P_n (n={n})")
    plt.scatter(X, Y, s=20, label="noeuds")
    plt.xlabel("x"); plt.ylabel("y"); plt.legend()
    if title: plt.title(title)
    plt.tight_layout()
    plt.show()

# --- fonctions test ---
def f_sin(x): return np.sin(x)
def f_rat(x): return 1.0 / (1.0 + 10.0 * x**2)

if __name__ == "__main__":
    # Exemple 1 : sin sur [0, 2π]
    for n in (10, 20):
        interp_plot(f_sin, 0.0, 2*np.pi, n, title=f"sin sur [0, 2π], n={n}")
    # Exemple 2 : 1/(1+10x^2) sur [-1, 1]
    for n in (10, 20):
        interp_plot(f_rat, -1.0, 1.0, n, title=f"1/(1+10x^2) sur [-1, 1], n={n}")