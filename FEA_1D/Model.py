import math

from FEA_1D import *
from FEA_1D.Beam import Beam

class Model:
    def __init__(self):
        self.nodes = {}
        self.elements = {}
        self.aux_nodes = {}
        self.beams = {}

        # Se incializan a cero el número de componentes del modelo
        self.n_nodes = 0
        self.n_aux_nodes = 0
        self.n_elements = 0
        self.n_beams = 0

        # Se indicara el nodo que esté articulado
        self.list_joints = []

        # Matriz de rigidez global
        self.K_G = None

        # Vector de cargas global
        self.f_G = None

        # Parameter of the model that indicates if the model is solved
        self.solved = False


    def add_node(self, x):
        '''
        A node is defined by its position in space

        :param x: (float) Position in space in coordinate x
        :return:
        '''
        # The number of nodes is updated
        self.n_nodes += 1

        # A node is created and stored
        n = Node(x, self.n_nodes)
        self.nodes[self.n_nodes] = n

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False


    def add_aux_node(self, x):
        '''
        An auxiliary node is defined by its position in space

        :param x: (float) Position in space in coordinate x
        :return:
        '''
        # The number of nodes is updated
        self.n_aux_nodes += 1

        # A node is created and stored
        n = aux_node(x, self.n_aux_nodes)
        self.aux_nodes[self.n_aux_nodes] = n

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False


    def add_beam(self, aux_nodes, material, section, n_x):
        """
        A beam is added to the model

        :param aux_nodes: (list) List of nodes of the beam. This will be auxiliary nodes.
        :param material: (Material) Material of the beam
        :param section: (Section) Section of the beam
        :param n: (float) Load per unit length
        :return: None
        """

        # The global nodes of the element are obtained
        id_global_n1 = aux_nodes[0]
        id_global_n2 = aux_nodes[1]

        # The node class associated with the nodes is obtained
        n1 = self.aux_nodes[id_global_n1]
        n2 = self.aux_nodes[id_global_n2]

        self.n_beams += 1

        # A beam is created and stored
        b = Beam([n1, n2], material, section, n_x)
        self.beams[self.n_beams] = b

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False


    def add_elemento(self, tipo_Elemento, nodos_elemento, E, A, n_x):
        '''
        An element is added to the model


        :param tipo_Elemento: (Elemento) Type of element
            - Element.LINEAL
            - Element.CUADRATICO
        :param nodos_elemento: (list) Nodes of the element. The global id of the nodes is entered
        :param E: (float) Elasticity module
        :param A: (float) Cross-sectional area
        :param n_x: (float) Vector of distributed loads
        :return: None
        '''
        # The number of nodes is updated
        self.n_elements += 1

        # Type of linear element
        if Element.LINEAR == tipo_Elemento:

            # The global nodes of the element are obtained
            id_global_n1 = nodos_elemento[0]
            id_global_n2 = nodos_elemento[1]

            # The node class associated with the nodes is obtained
            n1 = self.nodes[id_global_n1]
            n2 = self.nodes[id_global_n2]

            # The element is created
            e = element_1D_LINEAR(n1, n2, E, A, n_x, self.n_elements)

            # The element is added to the dictionary
            self.elements[self.n_elements] = e

        # Type of quadratic element
        elif Element.CUADRATIC == tipo_Elemento:
            raise NotImplementedError("Unimplemented method for quadratic elements.")

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False



    def add_articulacion(self, id_node):
        '''
        A joint is added to the model
        
        :param id_node: (int) Id of the node
        :return: None
        '''
        # It is checked that the node exists
        if id_node not in self.nodes:
            raise ValueError("The node does not exist")

        else:
            # It is checked that the node is not already articulated
            if id_node in self.list_joints:
                raise ValueError("The node is already articulated")
        
        # The node is added to the list of joints
        self.list_joints.append(id_node)

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False


    def mesh(self, maximum_length):
        '''
        The model is meshed

        :param maximum_length: (float) Maximum length of the elements
        :return: None
        '''
        # The elements are traversed
        for id, beam in self.beams.items():

            # The element is meshed
            distance = abs(beam.nodes[1].x_global - beam.nodes[0].x_global)

            # The number of elements between two auxiliary nodes is calculated
            n_elements = math.ceil(distance / maximum_length)

            length_element = distance / n_elements

            # Add intermediate nodes
            self._Add_intermediate_nodes(beam.nodes[0], length_element, n_elements)

            # Define the elements of the model
            for i in range(1, n_elements+1):
                n1 = self.nodes[i]
                n2 = self.nodes[i + 1]

                self.add_elemento(Element.LINEAR, [n1.id_global, n2.id_global], beam.material.E, beam.section.A, beam.n_x)

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False


    def _Add_intermediate_nodes(self, n1, length_element, n_elements):
        '''
        Intermediate nodes are added between two nodes

        :param n1: (Node) Node 1. Initial node
        :param n2: (Node) Node 2. Final node
        :param length_element: (float) Length of the element
        :param n_elements: (int) Number of elements
        :return: None
        '''



        # The nodes are created <-> 1 node more than the number of elements
        for i in range(n_elements + 1):
            x = n1.x_global + i * length_element

            # If the node already exists, it is not added
            if self.bool_created_node(x):
                pass
            else:
                self.add_node(x)


    def bool_created_node(self, x):
        '''
        Check if a node is created

        :param x: (float) Position in space in coordinate x
        :return: (bool) True if the node is created
        '''

        for id, node in self.nodes.items():
            if node == x:
                return True

        return False





    def Assemble_K_G(self):
        '''
        The global stiffness matrix of a 1D finite element problem is assembled
        :return:
        '''
        
        # The global stiffness matrix is created
        self.K_G = np.zeros((self.n_nodes, self.n_nodes))
        
        # The elements are traversed
        for id, e in self.elements.items():
            
            # The stiffness matrix of the element is obtained
            K_e = e._K()

            # The global stiffness matrix is assembled
            self.K_G[e.n1.id_global-1, e.n1.id_global-1] += K_e[0,0]
            self.K_G[e.n1.id_global-1, e.n2.id_global-1] += K_e[0,1]
            self.K_G[e.n2.id_global-1, e.n1.id_global-1] += K_e[1,0]
            self.K_G[e.n2.id_global-1, e.n2.id_global-1] += K_e[1,1]

    def Assemble_f_G(self):
        '''
        The global load vector of a 1D finite element problem is assembled

        :return:
        '''

        # The global load vector is created
        self.f_G = np.zeros((self.n_nodes, 1))

        # The elements are traversed
        for id, e in self.elements.items():
            
            # The load vector of the element is obtained
            f_e = e._f()
            
            # The global load vector is assembled
            self.f_G[e.n1.id_global-1] += f_e[0]
            self.f_G[e.n2.id_global-1] += f_e[1]


    def Boundary_Conditions(self):
        '''
        The boundary conditions of the model are imposed in:
            - The global stiffness matrix
            - The global load vector
            
        :return: None
        '''
        # A copy of the global stiffness matrix is created so as not to modify the original (cc = boundary conditions)
        self.K_G_cc = self.K_G.copy()
        
        # A copy of the global load vector is created so as not to modify the original (cc = boundary conditions)
        self.f_G_cc = self.f_G.copy()
        
        # The joints are traversed
        for joint_node in self.list_joints:
            # The boundary conditions are imposed K_G
            self.K_G_cc[joint_node-1, :] = 0
            self.K_G_cc[:, joint_node-1] = 0
            self.K_G_cc[joint_node-1, joint_node-1] = 1

            # The boundary conditions are imposed f_G
            self.f_G_cc[joint_node-1] = 0


    def _delta_G(self):
        '''
        The displacements are calculated
        
        :return:
        '''
        # The global stiffness matrix with boundary conditions is calculated
        self.Boundary_Conditions()

        # The displacements are calculated
        self.delta = np.linalg.solve(self.K_G_cc, self.f_G_cc)


        return self.delta


    def calculate_delta(self, x):
        '''
        Displacement at a point x
        
        :param x: (float) Position x
        :return: (float) Displacement
        '''
        
        # The displacements are calculated
        delta = 0
        delta_G = self._delta_G()
        _delta_e = np.zeros((2, 1))
        for id, e in self.elements.items():

            chi_element = e.chi_in_x(x)

            # Desplazamientos de los nodos de cada elemento
            _delta_e[0] = delta_G[e.n1.id_global-1]
            _delta_e[1] = delta_G[e.n2.id_global-1]

            delta += e.u(_delta_e, chi_element)

        return delta


    def _sigma_G(self, delta_G):
        '''
        The stresses are calculated
        
        :param delta_G: (np.array) Displacements
        :return: (np.array) Stresses
        '''
        
        # A vector of stresses is created
        sigma = np.zeros((self.n_elements, 1))

        # The elements are traversed
        for id, e in self.elements.items():
            
            # The stresses are calculated
            sigma[id-1] = e._sigma(delta_G)

        return sigma


    def info(self):
        """
        Information of the model

        :return:
        """

        print("Model information")
        print("Number of nodes: ", self.n_nodes)
        print("Number of elements: ", self.n_elements)
        print("Number of beams: ", self.n_beams)
        print("Number of joints: ", len(self.list_joints))
        print("Solved: ", self.solved)