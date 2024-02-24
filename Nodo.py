import numpy as np

class Nodo:
    '''
    Clase que define un nodo en un problema de elementos finitos 1D
    '''
    def __init__(self, x_global, id):
        self.x_global = x_global
        self.id_global = id

        # Se define a que elmento pertenece
        self.id_elmemto = None


    def info(self):
        print("Informacion nodo")
