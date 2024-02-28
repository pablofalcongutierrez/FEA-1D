from FEA_1D import *


# The model is created
model = Model()

# The material is defined
material = Material("Steel", 210e3)

# The section is defined
section = Section(100)

# The loads is defined
n_x = 1000

# The nodes are added
model.add_aux_node(0)
model.add_aux_node(10)

# The beam is added
model.add_beam([1, 2], material, section, 0)

# The model is meshed
model.mesh(3)

model.info()


