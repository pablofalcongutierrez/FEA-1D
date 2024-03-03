# The same model as in Test_1.py is created.
# The only difference is that the model is meshed with the number of elements

import matplotlib.pyplot as plt
from FEA_1D import *


# The model is created
model = Model()

# The material is defined
material = Material("Steel", 200e3)

# The section is defined
section = Section(100)

# The loads is defined
n_x = 1000

# The nodes are added
model.add_aux_node(0, u=0)
model.add_aux_node(100)
model.add_aux_node(200)
model.add_aux_node(300)

# The beam is added
model.add_beam([0, 1], material, section, 0)
model.add_beam([1, 2], material, section, n_x)
model.add_beam([2, 3], material, section, 0)

# The model is meshed
model.mesh(50)



# model.info()

model.Solve()

list_x = []
list_delta = []

# The displacement of the nodes are plotted
for i in range(1, 300):
    list_x.append(i)
    list_delta.append(model.delta_pos(i))

plt.plot(list_x, list_delta)
plt.show()

# print("Desplazamiento")
# print(model.delta_pos(1))


# model.Solve()



