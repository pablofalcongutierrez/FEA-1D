"""
Script donde se definen las matrices de rigidez elementales.

Funciones:
----------
- matriz_rigidez_elemental_1D_LINEAL(E, A, L): Calcula la matriz de rigidez para un elemento finito lineal en 1D.
"""


import numpy as np
from enum import Enum



class element_1D_LINEAR:

    def __init__(self, n1, n2, E, A, n_x, id):
        '''

        :param x1: Coordenada nodo 1
        :param x2: Coordenada nodo 2
        :param E: Módulo de elasticidad
        :param A: Área
        :param n_x: Fuerza distribuida
        '''
        # Nodos que forman el elemento
        self.n1 = n1
        self.n2 = n2

        # Geometría
        self.x1 = n1.x_global
        self.x2 = n2.x_global
        self.L = self.x2 - self.x1

        # Propiedades del nodo
        self.E = E
        self.A = A

        # Fuerzas distribuidas
        self.n_x = n_x

        # Identificador del elemento
        self.id = id

    def _J(self):
        '''
        Jacobiano asciado al elemento lineal
        :return:
        '''

        return self.L/2

    def _N(self, chi):
        '''
        Matriz de las funciones de forma en coordenadas naturales
        :return:
        '''

        N1 = 1/2 * (1 - chi)
        N2 = 1/2 * (1 + chi)
        return np.array([[N1, N2]])

    def _B(self):
        '''
        Matriz de las derivadas de las funciones de forma en coordenadas naturales
        :return:
        '''

        dN1 = -1/2
        dN2 = 1/2
        return 1 / self._J() * np.array([[dN1, dN2]])


    def _epsilon(self, _delta):
        """
        Vector de las deformaciones del elemento

        :param _delta: Vector de los desplazamientos del nodo
        :return:
        """

        return self._B() @ _delta


    def _sigma(self, _delta):
        '''
        Matriz de tensiones de los desplazamientos del elemento

        :param _delta: Vector de los desplazamientos del elemento
        :return:
        '''

        return self._epsilon(_delta) * self.E


    def _F(self, _delta):
        '''
        Vector de fuerzas de los nodos

        :param _delta: Vector de los desplazamientos del elemento
        :return:
        '''

        return self._sigma(_delta) * self.A


    def _D(self):
        '''
        Matriz elástica, para 1D se convierte en un escalar

        :return:
        '''

        return np.array([[self.E]])


    def _K(self):
        '''
        Matriz de rigidez

        :return:
        '''


        k = lambda chi: self._B().T @ self._D() @ self._B() * self._J() * self.A

        K = 1 * k(1/np.sqrt(3)) + 1 * k(-1/np.sqrt(3))
        return K


    def _f(self):
        '''
        Vector de cargas del elemento

        :return:
        '''

        # Es por el jacobiano porque d/dx = d/dchi * dchi/dx
        f = lambda chi: self._J() * self._N(chi).T * self.n_x

        return 1 * f(1/np.sqrt(3)) + 1 * f(-1/np.sqrt(3))


    def u(self, _delta, chi):
        '''
        Desplazamiento en coordenada chi

        :return:
        '''

        return self._N(chi) @ _delta


class Elemento(Enum):
    '''
    Tipo de elemento segun la función de forma
    '''

    LINEAL = 1
    CUADRATICO = 2

# # Geometría
# x1 = 0                                                                  # mm
# x2 = 100                                                                # mm
#
# # Propiedades
# E = 200e3                                                               # MPa
# A = 1000                                                   # mm2
#
# # Esfuerzos
# n_x = 1000                                                             # N/mm
#
# # Se define el elemento
# e = element_1D_LINEAR(x1, x2, E, A, n_x, 1)
#
#
# # Calculo de la matriz de rigidez y del vector de cargas
# K = e._K()
# f = e._f()
#
# # Se imponen las condiciones de contorno
# K[0,0] = 1
# K[1,0] = 0
# K[0,1] = 0
#
# f[0] = 0
# # f[1] = 100e3
# # Imprimir los vectores
# print('K')
# print(K)
#
# print()
# print('K inversa')
# print(np.linalg.inv(K))
#
# print()
# print('f')
# print(f)
#
# # Cálculo de las deformaciones
# delta = np.linalg.inv(K) @ f
# print()
# print(e._epsilon(delta))
#
# chi = 1
# print()
# print('Posición:', chi)
#
# print()
# print('Desplazamiento:')
# print(e.u(delta, chi))
#
# print()
# print('Deformacion:')
# print(e._epsilon(delta))
#
# print()
# print('Tensión:')
# print(e._sigma(delta))
# print()
#
#
# a = np.array([[1,0],[0,10]])
# print(a)
# print(np.linalg.inv(a))

