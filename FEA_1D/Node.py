import numpy as np

class Node:
    '''
    Class that defines a node in a 1D finite element problem
    '''

    def __init__(self, x, id, F=None, u=None):
        '''
        Constructor of the class Node

        :param x: (float) Coordinate of the node
        :param id: (int) Identifier of the node
        :param F: (float) Force in the node. It is None by default
        :param u: (float) displacement in the node. It is None by default
        '''

        # The global coordinate is defined
        self.x = x
        self.id_global = id
        self.F = F
        self.u = u


    # Especial method to compare a node with a coordinate to now if the node is already created
    def __eq__(self, other):
        return self.x == other


    # It is necessary to define the method __copy__ to copy the properties of the node
    # It will be used when the user wants to copy the properties of an axuliary node to a normal node
    def __copy__(self):
        # Create a new instance of the class with the same properties
        new_instance = type(self)(self.x, self.id_global, self.F, self.u)
        return new_instance

