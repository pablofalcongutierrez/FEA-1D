"""
Script donde se definen las matrices de rigidez elementales.

Funciones:
----------
- matriz_rigidez_elemental_1D_LINEAL(E, A, L): Calcula la matriz de rigidez para un elemento finito lineal en 1D.
"""

from func_forma import *
import numpy as np


def matriz_rigidez_elemental_1D_LINEAL(E:float, A, L):
    """
    Calcula la matriz de rigidez para un elemento finito lineal en 1D.

    Parameters:
    -----------
    E : float
        Módulo de elasticidad del material.
    A : float
        Área transversal del elemento.
    L : float
        Longitud del elemento finito en coordenadas físicas.

    Returns:
    --------
    np.array
        Matriz de rigidez elemental para el elemento finito lineal en 1D.
    """

    k_e = np.zeros([2,2])

    for i in range(2):

        for j in range(2):


            f = lambda chi, i, j: func_derivada_forma_1D_LINEAR(chi)[i] * E * A * func_derivada_forma_1D_LINEAR(chi)[j] * J_1D_LINEAR(L)

            k_e[i,j] = f(1/np.sqrt(3), i, j) + f(-1/np.sqrt(3), i, j)

    return k_e



matriz_rigidez_elemental_1D_LINEAL(10,2,5)


