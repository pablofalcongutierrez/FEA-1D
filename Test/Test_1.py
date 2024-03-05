import matplotlib.pyplot as plt
from FEA_1D import *

model = Model()
E = 200e3       # Young's modulus [N/mm^2]
# The material is defined
material = Material("Steel", E)

A = 100         # Area [mm^2]
# The section is defined
section = Section(100)

# The load per unit length is defined
n_x = 100       # Load per unit length [N/mm]

# The nodes are added x [mm], F [N], u [mm]
model.add_aux_node(0, u=0)
model.add_aux_node(100, F=1000)
model.add_aux_node(200, F=2000)

# The beam is added
model.add_beam([0, 1], material, section, 0)
model.add_beam([1, 2], material, section, n_x)

element_size = 10   # Element size [mm]
model.mesh(element_size)

model.Solve()

list_x = []
list_delta = []
list_F = []

# The displacement of the nodes are plotted
list_x = []
list_delta = []
list_F = []

for i in np.linspace(0, 200, 1000):
  list_x.append(i)
  list_delta.append(model.delta_pos(i))
  list_F.append(model.force_pos(i))


  # The displacement are plotted
plt.plot(list_x, list_delta)
plt.title("Displacement of the nodes")
plt.xlabel("x [mm]")
plt.ylabel("Displacement [mm]")
plt.show()


# The forces are plotted
plt.plot(list_x, list_F)
plt.title("Force")
plt.xlabel("x [mm]")
plt.ylabel("Force [N]")
plt.show()
