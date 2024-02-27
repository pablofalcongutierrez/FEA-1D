from FEA_1D import *

class Model:
    def __init__(self):
        self.nodes = {}
        self.elements = {}

        self.n_nodes = 0
        self.n_elements = 0

        # Se indicara el nodo que esté articulado
        self.list_joints = []

        # Matriz de rigidez global
        self.K_G = None

        # Vector de cargas global
        self.f_G = None


    def Add_node(self, x):
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


    def Add_elemento(self, tipo_Elemento, nodos_elemento, E, A, n_x):
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



    def Add_articulacion(self, id_node):
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
        '''
        General information of the created model
        
        :return:
        '''
        
        print("Model information")
        print("Number of nodes: ", self.n_nodes)
        # All the noder are printed
        for id, n in self.nodes.items():
            print("\t- Node ", id, ": ", n.x_global)
        print("Number of elements: ", self.n_elements)
        print("Number of joints: ", self.list_joints)
        print()