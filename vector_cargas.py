"""
Script para calcular el vector de cargas nodales en elementos finitos 1D.

Funciones:
----------
- vector_cargas_nodales_1D_LINEAL(F, L): Calcula el vector de cargas nodales para un elemento finito lineal en 1D.
"""

from func_forma import *
import numpy as np


def vector_cargas_nodales_1D_LINEAL(n, L):
    """
    Calcula el vector de cargas nodales para un elemento finito lineal en 1D.

    Parameters:
    -----------

    L: float
        Longitud del elemento finito en coordenadas físicas.

    n: float
        Fuerza por unidad de longitud.

    Returns:
    --------
    np.array
        Vector de cargas nodales para el elemento finito lineal en 1D.
    """

    # Inicializa el vector de cargas nodales
    f = np.zeros(2)

    # Itera sobre los índices i del vector de cargas nodales
    for j in range(2):

        # De momento las fuerzas puntuales solo se implementan como fuerzas puntuales
        # SE MULTIPLICA POR EL JACOBIANO PORQUE ESTA EN COORDENADAS NATURALES
        # func_f_ext = lambda chi, j: F_list[0] * func_derivada_forma_1D_LINEAR(chi)[j] * J_1D_LINEAR(L)
        #
        # # Se evalua entre 1 y -1
        # f_e[j] = func_f_ext(1, j) + func_f_ext(-1, j)

        func_f_int = lambda chi, i: n * func_derivada_forma_1D_LINEAR(chi)[j] * J_1D_LINEAR(L)

        # Se evalua en + 1/sqrt(3) - 1/sqrt(3)
        f[j] = func_f_int(1/np.sqrt(3), j) + func_f_int(-1/np.sqrt(3), j)

    return f


# Ejemplo de uso
vector_cargas = vector_cargas_nodales_1D_LINEAL(10, 1)
print("Vector de cargas nodales:")
print(vector_cargas)
