import math

from FEA_1D import *

"""
This script have the function to mesh all the elements of the model
when the user have gave all the nodes
"""

class Mesh:

    def __init__(self, model):
        '''
        Constructor of the class Mesh

        :param model: (Model) Model of the finite element problem
        '''

        # The model is defined
        self.model = model

    def Generate_mesh(self, n_elements=None, length=None):
        '''
        The user have gave the nodes that define the principal structure but this function subdivide the structure
        into small elements.

        The precision of the mesh is defined by the user whith one of this parameters:
            - Indicating the number of elements
            - Indicating the length of the elements

        :param n_elements: (int) Number of elements. It have to be a positive integer
        and greater than the number of nodes minus one
        :param length: (float) Length of the elements.
        :return: None
        '''

        if n_elements is not None and length is not None:
            raise ValueError("The number of elements and the length of the elements cannot be defined at the same time")

        elif n_elements is None and length is None:
            raise ValueError("The number of elements or the length of the elements have to be defined")

        elif n_elements is not None:
            # The mesh is generated with the number of elements
            self._Generate_mesh_n_elements(n_elements)

        else:
            # The mesh is generated with the length of the elements
            self._Generate_mesh_length(length)


    def _Generate_mesh_n_elements(self, n_elements):
        '''
        The mesh is generated with the number of elements.

        This function have to take into account that all the distances between the nodes defined by the user can be
        different, so the length of the elements can be different too.

        :param n_elements: (int) Number of elements
        :return: None
        '''

        # If the number of elements is less than the number of nodes minus one, an error is raised
        if n_elements < self.model.n_nodes - 1:
            raise ValueError("The number of elements have to be greater than the number of nodes minus one")

        # The total length of the distance into nodes is calculated
        self.total_length = 0
        # The length of the distance into nodes is calculated
        for i in range(self.model.n_nodes - 1):
            self.total_length = self.model.nodes[i+1].x_global - self.model.nodes[i].x_global

        # The maximum length of the elements is defined
        element_length = self.total_length / n_elements

        # The mesh is generated with the length of the elements
        self._Generate_mesh_length(element_length)


    def _Generate_mesh_length(self, maximum_length):
        '''
        The mesh is generated indicating the maximum length of the elements that the user want.

        Between two nodes, the nodes defined by the user, the distance will be the same, but never can
        be greater than the length defined by the user.

        :param maximum_length:
        :return:
        '''

        # The number of elements between two nodes is calculated to obtain the same length of the elements
        for i in range(self.model.n_nodes - 1):
            length_between_nodes = self.model.nodes[i + 1].x_global - self.model.nodes[i].x_global

            # The number of elements between two nodes is calculated
            number_element = math.ceil(length_between_nodes / maximum_length)

            # The length of the elements is calculated
            length_element = length_between_nodes / number_element

            # TENGO QUE INDICAR QUE EL PRIMER NODO Y EL ULTIMO NODO YA ESTAN DEFINIDOS, POR LO QUE
            # NO SE PUEDEN AÑADIR MAS NODOS EN ESAS POSICIONES Y SE TIENEN QUE IMPLEMENTAR LOS NODOS INTERMEDIOS ADDECUADAMENTE

            # ES POSIBLE QUE LA MEJOR OPCION ES CREAR UNA FUNCION QUE AÑADA LOS NODOS INTERMEDIOS Y LOS ELEMENTOS
            raise NotImplementedError("The function is not implemented yet")
