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
