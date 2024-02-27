from FEA_1D import *


# The model is created
model = Model()

mesh = Mesh(model)

# The constants of the model are defined
E = 200000
A = 100
n_x = 1000


L = 500

# Nodes
model.Add_node(0)
model.Add_node(L)

# Maximum length of the elements
mesh.Generate_mesh(maximum_length=50)

# Elements
model.Add_elemento(Element.LINEAR, [1, 2], E, A, n_x)

model.info()

