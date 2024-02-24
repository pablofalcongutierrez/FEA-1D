from Nodo import *
from Elementos import *
class Modelo:
    def __init__(self):
        self.nodos = {}
        self.elementos = {}

        self.n_nodos = 0
        self.n_elementos = 0

        # Se indicara el nodo que esté articulado
        self.articulaciones = []

        # Matriz de rigidez global
        self.K_G = None

        # Vector de cargas global
        self.f_G = None


    def Add_nodo(self, x):
        '''
        Se define un nodo
        :param x:
        :return:
        '''
        # Se actualiza el número de nodos
        self.n_nodos += 1

        # Se crea el nodo y se almacena
        n = Nodo(x, self.n_nodos)
        self.nodos[self.n_nodos] = n


    def Add_elemento(self, tipo_Elemento, nodos_elemento, E, A, n_x):
        '''
        Se añade un elemento al modelo

        :param tipo_Elemento: (Elemento) Tipo de elemento
            - Elemento.LINEAL
            - Elemento.CUADRATICO
        :param nodos_elemento: (list) Nodos del elemento. Se introduce el id global de los nodos
        :param E: (float) Módulo de elasticidad
        :param A: (float) Área de la sección transversal
        :param n_x: (float) Vector de cargas distribuidas
        :return: None
        '''
        # Se actualiza el número de nodos
        self.n_elementos += 1

        # Tipo de elemento lineal
        if Elemento.LINEAL == tipo_Elemento:

            # Se obtienen los nodos globales del elemento
            id_global_n1 = nodos_elemento[0]
            id_global_n2 = nodos_elemento[1]

            # Se obtiene la clase nodo asociada a los nodos
            n1 = self.nodos[id_global_n1]
            n2 = self.nodos[id_global_n2]

            # Se crea el elemento
            e = element_1D_LINEAR(n1, n2, E, A, n_x, self.n_elementos)

            # Se añade el elemento al diccionario
            self.elementos[self.n_elementos] = e

        # Tipo de elemento cuadrático
        elif Elemento.CUADRATICO == tipo_Elemento:
            raise NotImplementedError("Método no implementado para elementos cuadráticos.")


    def Add_articulacion(self, id_nodo):
        '''
        Se añade una articulación al modelo
        :param id_nodo: (int) Id del nodo
        :return: None
        '''

        # Se comprueba que el nodo exista
        if id_nodo not in self.nodos:
            raise ValueError("El nodo no existe")

        else:
            # Se comprueba que el nodo no esté ya articulado
            if id_nodo in self.articulaciones:
                raise ValueError("El nodo ya está articulado")

        # Se añade el nodo a la lista de articulaciones
        self.articulaciones.append(id_nodo)


    def Ensambla_K_G(self):
        '''
        Se ensambla la matriz de rigidez global de un probelema de elementos finitos 1D
        :return:
        '''

        # Se crea la matriz de rigidez global
        self.K_G = np.zeros((self.n_nodos, self.n_nodos))

        # Se recorren los elementos
        for id, e in self.elementos.items():
            # Se obtiene la matriz de rigidez del elemento
            K_e = e._K()


            # Se ensambla la matriz de rigidez global
            self.K_G[e.n1.id_global-1, e.n1.id_global-1] += K_e[0,0]
            self.K_G[e.n1.id_global-1, e.n2.id_global-1] += K_e[0,1]
            self.K_G[e.n2.id_global-1, e.n1.id_global-1] += K_e[1,0]
            self.K_G[e.n2.id_global-1, e.n2.id_global-1] += K_e[1,1]

    def Ensambla_f_G(self):
        '''
        Se ensambla el vector de cargas global de un problema de elementos finitos 1D

        :return:
        '''

        # Se crea el vector de cargas global
        self.f_G = np.zeros((self.n_nodos, 1))

        # Se recorren los elementos
        for id, e in self.elementos.items():
            # Se obtiene el vector de cargas del elemento
            f_e = e._f()

            # Se ensambla el vector de cargas global
            self.f_G[e.n1.id_global-1] += f_e[0]
            self.f_G[e.n2.id_global-1] += f_e[1]

    def info(self):
        print("Informacion modelo")
        print("Número de nodos: ", self.n_nodos)
        print("Número de elementos: ", self.n_elementos)
        print("Articulaciones: ", self.articulaciones)
        print()