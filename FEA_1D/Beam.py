class Beam:
    """
    A class to define a beam element.

    A beam needs to be defined for commodities of the user. In this way, the user
    can define auxiliary nodes to define the beam. But the nodes aren't stored in the
    model.

    When the user decides to mesh the model, new "normal" nodes are created and stored. And the
    mesh will created with the precision defined by the user.

    In the case that the user define only nodes with the points of the beam, the mesh would have
    a very low precision.
    """
    def __init__(self, nodes, material, section, n_x):
        """
        Constructor of the class beam

        :param nodes: (list) List with the nodes that define the beam
        :param material: (Material) Material of the beam
        :param section: (Section) Section of the beam
        :param n_x: (float) Longitudinal load of the beam
        """

        self.nodes = nodes
        self.material = material
        self.section = section
        self.n_x = n_x