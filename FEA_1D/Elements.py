import numpy as np
from enum import Enum



class element_1D_LINEAR:

    def __init__(self, n1, n2, E, A, n_x, id):
        '''
        Linear element in 1D

        :param x1: Coordinate of node 1
        :param x2: Coordinate of node 2
        :param E: Elasticity module
        :param A: Area
        :param n_x: Distributed force
        '''

        # Nodes that form the element
        self.n1 = n1
        self.n2 = n2

        # Geometry
        self.x1 = n1.x
        self.x2 = n2.x
        self.L = self.x2 - self.x1

        # Properties of the node
        self.E = E
        self.A = A

        # Distributed forces
        self.n_x = n_x

        # Node identifier
        self.id = id

    def delta_element(self, delta):
        '''
        Vector of the displacements of the element

        :param delta: (np.array) Displacement of the nodes
        :return: (np.array) Displacement of the element
        '''

        return np.array([delta[self.n1.id_global], delta[self.n2.id_global]])

    def chi_in_x(self, x):
        '''
        Coordinates transformation from x to chi

        With this, the displacement can be obtained at any point of the element when requested from
        the model with the global coordinates.

        :param x: (float) Coordinate in x
        :return: (float) Coordinate in chi
        '''

        return 2 * (x - self.x1) / self.L - 1


    def _J(self):
        '''
        Jacobian of the linear element

        :return: (float) Jacobian
        '''

        return self.L/2

    def _N(self, chi):
        '''
        Matrix of the shape functions in natural coordinates

        :return: (np.array) Matrix of shape functions
        '''

        N1 = 1/2 * (1 - chi)
        N2 = 1/2 * (1 + chi)
        return np.array([[N1, N2]])

    def _B(self):
        '''
        Matrix of the derivatives of the shape functions in natural coordinates

        :return:
        '''

        dN1 = -1/2
        dN2 = 1/2
        return 1 / self._J() * np.array([[dN1, dN2]])


    def _epsilon(self, _delta):
        """
        Vector of the deformations of the element

        :param _delta: Vector of the displacements of the node
        :return: (np.array) Vector of deformations
        """

        return self._B() @ _delta


    def _sigma(self, _delta):
        '''
        Matrix of the stresses of the displacements of the element

        :param _delta: Vector of the displacements of the node
        :return: (np.array) Vector of stresses
        '''

        return self._epsilon(_delta) * self.E


    def _F(self, _delta):
        '''
        Vector of forces of the nodes

        :param _delta: Vector of the displacements of the node
        :return: (np.array) Vector of forces
        '''

        return self._sigma(_delta) * self.A


    def _D(self):
        '''
        Elastic matrix, for 1D it becomes a scalar

        :return: (np.array) Elastic matrix
        '''

        return np.array([[self.E]])


    def _K(self):
        '''
        Stiffness matrix

        :return: (np.array) Stiffness matrix
        '''


        k = lambda chi: self._B().T @ self._D() @ self._B() * self._J() * self.A

        K = 1 * k(1/np.sqrt(3)) + 1 * k(-1/np.sqrt(3))
        return K


    def _f(self):
        '''
        Vector of loads of the element

        :return: (np.array) Vector of loads
        '''

        f = lambda chi: self._J() * self._N(chi).T * self.n_x

        return 1 * f(1/np.sqrt(3)) + 1 * f(-1/np.sqrt(3))


    def u(self, delta, chi):
        '''
        Displacement in chi coordinate

        :param _delta: (np.array) Displacement of the nodes of the element
        :param chi: (float) Coordinate in chi
        :return: (np.array) Displacement
        '''

        print("delta total:")
        print(delta)
        print()

        # The vector of displacements of the nodes of the element is obtained
        delta_element = self.delta_element(delta)

        if -1 <= chi <= 1:
            return self._N(chi) @ delta_element

        else:
            return 0

    def info(self):
        '''
        Information element

        :return: None
        '''
        print("Element information")
        print("Node 1: ", self.n1.id_global)
        print("Node 2: ", self.n2.id_global)
        print("Longitud: ", self.L)
        print("x1: ", round(self.x1, 2), "mm")
        print("x2: ", round(self.x2, 2), "mm")


class Element(Enum):
    '''
    Type of element according to the shape functions
    '''

    LINEAR = 1
    CUADRATIC = 2



