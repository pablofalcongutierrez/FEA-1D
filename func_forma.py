"""
Script de funciones de forma para elementos finitos en 1D.

Este script contiene dos funciones que calculan las funciones de forma para elementos finitos unidimensionales.
Las funciones de forma son utilizadas en el análisis por elementos finitos para interpolar campos, como el campo de
deformación, dentro de un elemento finito.

Funciones:
----------
- func_forma_1D_LINEAR(chi): Calcula funciones de forma lineales para elementos finitos en 1D.
- func_forma_1D_CUADRATIC(chi): Calcula funciones de forma cuadráticas para elementos finitos en 1D.

"""

import numpy as np



def func_forma_1D_LINEAR(chi):
    """
    Calcula las funciones de forma para elementos finitos lineales en 1D.

    Parameters:
    -----------
    chi : float
        Coordenada natural o local en el elemento finito.

    Returns:
    --------
    np.array
        Arreglo NumPy que contiene las dos funciones de forma lineales (N1 y N2).
    """
    N1 = 1/2 * (1 - chi)
    N2 = 1/2 * (1 + chi)
    return np.array([N1, N2])



def func_derivada_forma_1D_LINEAR(chi):
    """
    Calcula las derivadas de las funciones de forma para elementos finitos lineales en 1D.

    Parameters:
    -----------
    chi : float
        Coordenada natural o local en el elemento finito.

    Returns:
    --------
    np.array
        Arreglo NumPy que contiene las dos derivadas de las funciones de forma lineales (N1 y N2).
    """
    dN1 = -1/2
    dN2 = +1/2
    return np.array([dN1, dN2])



def J_1D_LINEAR(L):
    """
    Calcula el Jacobiano para funciones de forma lineales en 1D.

    Parameters
    ----------
    L : float
        Longitud del elemento finito en coordenadas físicas.

    Returns
    -------
    float
        Valor del Jacobiano.
    """
    return L/2




