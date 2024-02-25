import matplotlib.pyplot as plt

from FEA_1D import *

"""
Test_1.py

Test 1: Realiza la prueba de la creación de un modelo
en el cual se añaden nodos y elementos lineales 
que son cargados con una fuerza distribuida a lo largo de
todos los elementos. Se añade una articulación en el nodo 1.
"""

'''
Script que realiza la prueba de la creación de un modelo
donde se añaden dos nodos, un elemento lineal y una articulación.
Para asi obtener la matriz de rigidez global y el vector de cargas global.
'''


# Se crea el modelo
model = Model()

# Se definen las constantes
E = 200000
A = 100
n_x = 1000

nodos = 100
elementos = nodos - 1
L = 500

x = 0
# Se añaden los nodos
for i in range(nodos):
    model.Add_node(x)
    print("Nodo añadido en x = ", x)

    paso = L / (nodos-1)
    x = paso + x

# Se añaden los elementos
for i in range(elementos):
    model.Add_elemento(Element.LINEAR, [i + 1, i + 2], E, A, n_x)

# Se añaden las articulaciones
model.Add_articulacion(1)

# Se ensambla la matriz de rigidez global
model.Assemble_K_G()

# Se ensambla el vector de cargas global
model.Assemble_f_G()

# Se imponen las condiciones de contorno
model.Boundary_Conditions()


# Se grafica el desplazamiento en funcion de x
x = np.linspace(0, L, 100)
delta = np.zeros_like(x)

for i in range(len(x)):
    delta[i] = model.calculate_delta(x[i])

plt.plot(x, delta)
plt.show()
