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

- [ ] **Boundary Conditions:**
    - [x] Define Joints
    - [ ] Define Displacements:
    - [ ] Define Forces

- [ ] **Mesh Generation:**
  - [ ] Limit the number of elements
  - [ ] Limit the maximum length of the elements

- [ ] **Material Properties:**
  - [x] Posibility to define the properties as a constant
  - [ ] Posibility to define the properties as a function

- [ ] **Loads:**
  - [ ] Define punctual loads on the nodes
  - [ ] Define distributed loads on the elements:
    - [x] Constant
    - [ ] Linear

- [ ] **Solver:**
  - [ ] Static Analysis

- [ ] **Post-Processing:**
  - [ ] Plot displacements
  - [ ] Plot strains
  - [ ] Plot stresses
  - [ ] Plot reactions
  - [ ] Plot internal forces

## Example of usage
In this example, we will define a simple 1D model with 3 nodes and 2 elements.
```python
from FEA_1D import *

# Define the nodes
model = Model()

# Define nodes
model.add_node(0)
model.add_node(1)
model.add_node(4)

# Define elements
model.add_element(0, 1)
model.add_element(1, 2)

# Define boundary conditions
model.add_joint(0)

```



## License
This project is open-source and is licensed under the MIT License.
Feel free to use, modify, and share it according to the terms of the license.
