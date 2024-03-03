1D Finite Element Analysis (FEA)
===============================

# Overview
Welcome to the Finite Element Analysis (FEA)
Programming project! This endeavor is focused on providing a
foundational platform for individuals interested in understanding
and implementing Finite Element Analysis algorithms.

In this repository, you will find a collection of Python scripts for 
structural problems.

## Features
- [x] **Define nodes:**

- [ ] **Define elements:**
  - [x] Linear
  - [ ] Quadratic

- [x] **Boundary Conditions:**
    - [x] Define Joints
    - [x] Define Displacements
    - [x] Define Forces

- [ ] **Mesh Generation:**
  - [ ] Limit the number of elements
  - [x] Limit the maximum length of the elements

- [ ] **Material Properties:**
  - [x] Posibility to define the properties as a constant
  - [ ] Posibility to define the properties as a function

- [ ] **Loads:**
  - [x] Define punctual loads on the nodes
  - [ ] Define distributed loads on the elements:
    - [x] Constant
    - [ ] Linear

- [x] **Post-Processing:**
  - [x] Calculate displacements
  - [x] Calculate strains
  - [x] Calculate stresses
  - [x] Calculate reactions
  - [x] Calculate internal forces

## Example of usage

Create the model
```python
from FEA_1D import *

model = Model()
```
Define the material and the section of the beams
```python
E = 200e3       # Young's modulus [N/mm^2]
# The material is defined
material = Material("Steel", E)

A = 100         # Area [mm^2]
# The section is defined
section = Section(100)
```

Define the nodes and the beams
```python
# The load per unit length is defined
n_x = 100       # Load per unit length [N/mm]

# The nodes are added x [mm], F [N], u [mm]
model.add_aux_node(0, u=0)
model.add_aux_node(100, F=1000)
model.add_aux_node(200, F=2000)

# The beam is added
model.add_beam([0, 1], material, section, 0)
model.add_beam([1, 2], material, section, n_x)
```

The mesh is generated and the model is solved
```python
element_size = 10   # Element size [mm]
model.mesh(element_size)

model.solve()
```

The results are printed
```python
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
```




## License
This project is open-source and is licensed under the MIT License.
Feel free to use, modify, and share it according to the terms of the license.
