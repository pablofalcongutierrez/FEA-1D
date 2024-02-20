import numpy as np

from Elementos import *
from func_forma import *
from vector_cargas import *

E = 210*1e9     # Pa
A = 1           # m2
L = 2           # m

F = 10e3        # N
n = 10e3        # N/m

J = J_1D_LINEAR(L)

# Se generan el nodo
k = matriz_rigidez_elemental_1D_LINEAL(E, A, L)
f = vector_cargas_nodales_1D_LINEAL(n, L)

# Se generan las condiciones de contorno
# El nudo 1 está articulado
k[0,0] = 1
k[1,0] = 0
k[0,1] = 0
f[0] = 0

vector_desplazamientos_elemento = np.linalg.inv(k) @ f
print("Matriz de rigidez")
print(k)
print("Inversa de matriz de rigidez")
print(np.linalg.inv(k))
print("Vector de desplazamientos")
print(vector_desplazamientos_elemento)

print(f"Desplazamiento en nodo 1 => u_x = {func_forma_1D_LINEAR(-1) @ vector_desplazamientos_elemento}")
print(f"Desplazamiento en nodo 2 => u_x = {func_forma_1D_LINEAR(1) @ vector_desplazamientos_elemento}")

print()

print(f"Deformación en nodo 1 => eps_x = {func_derivada_forma_1D_LINEAR(-1) @ vector_desplazamientos_elemento}")
print(f"Deformación en nodo 2 => eps_x = {func_derivada_forma_1D_LINEAR(1) @ vector_desplazamientos_elemento}")

print()

print(f"Tensión en nodo 1 => eps_x = {E*A*func_derivada_forma_1D_LINEAR(-1) @ vector_desplazamientos_elemento}")
print(f"Tensión en nodo 2 => eps_x = {E*A*func_derivada_forma_1D_LINEAR(1) @ vector_desplazamientos_elemento}")




