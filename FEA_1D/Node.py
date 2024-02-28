import numpy as np

class Node:
    '''
    Class that defines a node in a 1D finite element problem
    '''

    def __init__(self, x_global, id):
        '''
        Constructor of the class Node

        :param x_global:
        :param id:
        '''

        # The global coordinate is defined
        self.x_global = x_global
        self.id_global = id

        # The element to which it belongs is defined
        self.id_elmemto = None

    # Especial method to compare a node with a coordinate to now if the node is already created
    def __eq__(self, other):
        return self.x_global == other


class aux_node:
    """
    Class that defines an auxiliary node. The principal difference with the Node class is that the
    auxiliary node is defined for the construction of a beam.
    """
    def __init__(self, x_global, id_aux):
        """
        Constructor of the class aux_node

        :param x_global: (float) Coordinate of the node
        :param id_aux: (int) Identifier of the node
        """
        self.x_global = x_global
        self.id_aux = id_aux

