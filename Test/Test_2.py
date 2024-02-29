# The same model as in Test_1.py is created.
# The only difference is that the model is meshed with the number of elements

from FEA_1D import *


# The model is created
model = Model()

# The material is defined
material = Material("Steel", 200e3)

# The section is defined
section = Section(100)

# The loads is defined
n_x = 0

# The nodes are added
model.add_aux_node(0)
model.add_aux_node(100)

# The beam is added
model.add_beam([1, 2], material, section, n_x)

# The joints are added
model.add_joint(1)

model.add_puntual_load(2, 10000)

# The model is meshed
model.mesh(50)

model.Solve()



