class Material:
    """
    Material class for 1D FEA

    The material needs to be defined for commodities of the user. In this way, the user
    can define diferents materials to each beam.

    For the moment, the material is going to be defined as a constant.
    """
    def __init__(self, name, E):
        self.name = name
        self.E = E