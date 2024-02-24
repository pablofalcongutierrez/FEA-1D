from Modelo import Modelo
from Elementos import *

'''
Script que realiza la prueba de la creación de un modelo
donde se añaden dos nodos, un elemento lineal y una articulación.
Para asi obtener la matriz de rigidez global y el vector de cargas global.
'''


# Se crea el modelo
model = Modelo()

# Se definen las constantes
E = 210e9
A = 0.01
n_x = 1000

# Se añaden los nodos
model.Add_nodo(0)
model.Add_nodo(1)

# Se añaden los elementos
model.Add_elemento(Elemento.LINEAL, [1, 2], E, A, n_x)

# Se añaden las articulaciones
model.Add_articulacion(1)

# Se ensambla la matriz de rigidez global
model.Ensambla_K_G()

# Se ensambla el vector de cargas global
model.Ensambla_f_G()

# Se imprime la matriz de rigidez global
print(model.K_G)
print()

# Se imprime el vector de cargas global
print(model.f_G)
print()
