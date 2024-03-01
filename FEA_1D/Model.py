import math

from FEA_1D import *
from FEA_1D.Beam import *

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
        self.list_joints_AUX = []
        self.list_joints = []

        # The vector of punctual loads is created
        self.punctual_forces_AUX = {}
        self.punctual_forces = {}

        # Matriz de rigidez global
        self.K_G = None

        # Vector de cargas global
        self.f_G = None

        # Parameter of the model that indicates if the model is solved
        self.solved = False


    def add_node(self, x, F=None, u=None):
        '''
        A node is defined by its position in space, punctual load and displacement

        By default, the force and displacement are None

        :param x: (float) Position in space in coordinate x
        :param F: (float) Force in the node. It is None by default
        :param u: (float) displacement in the node. It is None by default
        :return: (Node) Node created
        '''

        # The number of nodes is updated

        # A node is created and stored
        n = Node(x, self.n_nodes, F, u)
        self.nodes[self.n_nodes] = n

        # The number of nodes is updated
        self.n_nodes += 1

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False

        return n


    def add_aux_node(self, x, F=None, u=None):
        '''
        An auxiliary node is defined by its position in space, punctual load and displacement

        By default, the force and displacement are None

        :param x: (float) Position in space in coordinate x
        :param F: (float) Force in the node. It is None by default
        :param u: (float) displacement in the node. It is None by default
        :return:
        '''

        # A node is created and stored
        aux_n = Node(x, self.n_aux_nodes, F, u)
        self.aux_nodes[self.n_aux_nodes] = aux_n

        # The number of nodes is updated
        self.n_aux_nodes += 1

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


        # A beam is created and stored
        b = Beam([n1, n2], material, section, n_x)
        self.beams[self.n_beams] = b

        # The number of beams is updated
        self.n_beams += 1

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False


    def add_element(self, tipo_Elemento, nodos_elemento, E, A, n_x):
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

    def mesh(self, maximum_length):
        '''
        The model is meshed

        :param maximum_length: (float) Maximum length of the elements
        :return: None
        '''

        # The elements are traversed for adding intermediate nodes
        for id, beam in self.beams.items():

            # The element is meshed
            distance = abs(beam.nodes[1].x - beam.nodes[0].x)

            # The number of elements between two auxiliary nodes is calculated
            n_elements = math.ceil(distance / maximum_length)

            length_element = distance / n_elements

            # Add intermediate nodes
            self._Add_intermediate_nodes_elements(beam.nodes[0], beam.nodes[1], length_element, beam)

        # Update the parameter of the model that indicates if the model is unsolved
        self.solved = False


    def obtain_vector_forces(self):
        '''
        The vector of forces is obtained

        :return: (np.array) Vector of forces
        '''
        # The vector of forces is created
        f = np.zeros((self.n_nodes, 1))

        # The forces are added to the vector
        for id, node in self.nodes.items():
            if node.F == None:
                f[node.id_global] = 0
            else:
                f[node.id_global] = node.F

        return f


    def obtain_displacements_imposed(self):
        '''
        The vector of displacements is obtained

        :return: (np.array) Vector of displacements
        '''

        # The vector of displacements is created
        u = np.zeros((self.n_nodes, 1))

        # The displacements are added to the vector
        for id, node in self.nodes.items():
            if node.u == None:
                u[node.id_global] = np.nan
            else:
                u[node.id_global] = node.u

        return u

    def _Add_intermediate_nodes_elements(self, n1, n2, length_element, beam):
        '''
        Intermediate nodes are added between two nodes

        All the elements that are added have the same features as the beam

        :param n1: (Node) Node 1. Initial node
        :param n2: (Node) Node 2. Final node
        :param length_element: (float) Length of the element
        :return: None
        '''

        # The list of nodes added is created to facilitate the addition of elements
        list_nodes_adeed = []

        # The coordinate starts at the coordinate of the first node
        x = n1.x

        # While x is less or equal than the coordinate of the second node continue adding nodes
        while x <= n2.x:

            # If the node already exists, it is not added but the node is obtained to add the element
            if self.bool_created_node(x):
                n = n2
            else:
                if x == n1.x:
                    n = self.add_node(x, n1.F, n1.u)
                elif x == n2.x:
                    n = self.add_node(x, n2.F, n2.u)
                else:
                    n = self.add_node(x)

            # Append the node to the list of nodes added
            list_nodes_adeed.append(n)

            x += length_element


        # Convierte la lista de nodos en una lista de pares de nodos concatenados es decir [(n1, n2), (n2, n3), (n3, n4), ...]
        list_nodes_adeed = list(zip(list_nodes_adeed, list_nodes_adeed[1:]))



        # The elements are added
        for nodes in list_nodes_adeed:
            self.add_element(Element.LINEAR, [nodes[0].id_global, nodes[1].id_global], beam.material.E, beam.section.A, beam.n_x)


    def bool_created_node(self, x):
        '''
        Check if a node is already created

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
            self.K_G[e.n1.id_global, e.n1.id_global] += K_e[0,0]
            self.K_G[e.n1.id_global, e.n2.id_global] += K_e[0,1]
            self.K_G[e.n2.id_global, e.n1.id_global] += K_e[1,0]
            self.K_G[e.n2.id_global, e.n2.id_global] += K_e[1,1]

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
            self.f_G[e.n1.id_global] += f_e[0]
            self.f_G[e.n2.id_global] += f_e[1]


        # The punctual loads are added to the global load vector
        self.f_G += self.obtain_vector_forces()



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

        # The displacement of the nodes that area imposed
        displacements_imposed = self.obtain_displacements_imposed()

        # The displacements are added to the vector using np.isnan()
        for i in range(self.n_nodes):

            # When the user imposes a displacement, the row and column of the global stiffness matrix are set to zero
            if not np.isnan(displacements_imposed[i]):
                self.K_G_cc[i, :] = 0
                self.K_G_cc[:, i] = 0
                self.K_G_cc[i, i] = 1

                self.f_G_cc[i] = displacements_imposed[i]



    def Solve(self):
        '''
        The model is solved

        :return: None
        '''

        # The global stiffness matrix is assembled
        self.Assemble_K_G()

        # The global load vector is assembled
        self.Assemble_f_G()

        # The boundary conditions are imposed
        self.Boundary_Conditions()

        # The displacements are calculated
        self.delta = np.linalg.solve(self.K_G_cc, self.f_G_cc)

        # print the stiffness matrix
        print(self.K_G_cc)

        # print the load vector
        print(self.f_G_cc)

        # print the displacements
        print(self.delta)


        # The model is solved
        self.solved = True


    def info(self):
        """
        Information of the model

        :return:
        """

        print("Model information:")
        print("\t- Components of the model")
        # Print all the nodes
        print("\t\tNODES")
        for id, node in self.nodes.items():
            print("\t\t\t· Node: ", node.id_global, " x: ", node.x, " F: ", node.F, " u: ", node.u)

        # Print all the aux nodes
        print()
        print("\t\tAUXILIARY NODES")
        for id, node in self.aux_nodes.items():
            print("\t\t\t· Node: ", node.id_global, " x: ", node.x, " F: ", node.F, " u: ", node.u)

        # Print all the beams
        print()
        print("\t\tBEAMS")
        for id, beam in self.beams.items():
            print("\t\t\t· Beam: ", beam.nodes[0].id_global, beam.nodes[1].id_global, " E: ", beam.material.E, " A: ", beam.section.A, " n_x: ", beam.n_x)

        # Print all the elements
        print()
        print("\t\tELEMENTS")
        for id, element in self.elements.items():
            print("\t\t\t· Element: ", element.n1.id_global, element.n2.id_global, " E: ", element.E, " A: ", element.A, " n_x: ", element.n_x)

        print()
        print("Status of the model")
        print("\t- Solved: ", self.solved)