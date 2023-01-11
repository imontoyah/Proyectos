from torch_geometric.data import Data
import matplotlib.pyplot as plt
from borders import Point, convexHull
import openmesh
import numpy as np
from functions import area, f1, f2, f3, read_obj, write_obj
from problem import Problem
from evolution import Evolution

#Leer archivo .obj
vertices, faces=read_obj("/Users/isabella/Desktop/Universidad/QuintoSemestre/Optimizacion_II/Proyecto/Caras 3D/Final/Hombre.obj")

#Buscar puntos del borde
points=[]
x=[]
y=[]
z=[]

for i in range(len(vertices)):
    vertices[i][1], vertices[i][2] = vertices[i][2], vertices[i][1]
    points.append(Point(vertices[i][0], vertices[i][1]))
    x.append(vertices[i][0])
    y.append(vertices[i][1])
    z.append(vertices[i][2])

#Encontrar los puntos que están en el borde
border=convexHull(points,len(points))

xb=[]
yb=[]
for i in range(len(border)):
    xb.append(points[border[i]].x)
    yb.append(points[border[i]].y)
    #print(border[i], points[border[i]].x, points[border[i]].y)

#BORDE: 9786 9787 9725 4094 9892 9688 9909 9935 9990 9697 9953 9860 2389 9666

p1=x.index(max(x))
p2=x.index(min(x))
p3=y.index(max(y))
p4=y.index(min(y))

#Area malla original
initial_area=0
for i in range(len(faces)):
    t=[vertices[faces[i][0]], vertices[faces[i][1]], vertices[faces[i][2]]]
    initial_area+=area(t)

print(initial_area)

#Agregar puntos fijos al final
fp=[9786, 9787, 9725, 4094, 9892, 9688, 9909, 9935, 9990, 9697, 9953, 9860, 2389, 9666]
fixed_vertices=vertices[fp]
new_vertices=np.delete(vertices, fp, 0)
vertices=np.concatenate((new_vertices, fixed_vertices))

#NSGA-II función 2: error en el área superficial
problem1 = Problem(num_of_variables=2, objectives=[f1, f2], variables_range=vertices, initial_area=initial_area)
evo1 = Evolution(problem1, num_of_generations=100, num_of_individuals=50, crossover_param=0.5, mutation_prob=0.01, mutation_param=0.05)
evol1 = evo1.evolve()

for i in range(len(evol1)-1):
    func=[j.objectives for j in evol1[i]]
    
    function1=[k[0] for k in func]
    function2=[k[1] for k in func]

    plt.scatter(function1, function2, label="Frente "+str(i+1))

plt.xlabel('Cantidad de triángulos', fontsize=15)
plt.ylabel('Error del área superficial', fontsize=15)
plt.legend()
plt.title('Frontera de Pareto', fontsize=20)

plt.show()

print('vert', len(evol1[0][0].features[0]), 'triang', len(evol1[0][0].features[1].simplices))
print('f1', evol1[0][0].objectives[0], 'f2', evol1[0][0].objectives[1])

write_obj(evol1[0][0].features[0], evol1[0][0].features[1].simplices, '/Users/mariajosebernal/Documents/EAFIT/2022-2/Optimización/Proyecto/Caras 3D/Final/HombreNuevo1.obj')

#NSGA-II función 3: error en los valores de las alturas 
problem2 = Problem(num_of_variables=2, objectives=[f1, f3], variables_range=vertices, initial_area=initial_area)
evo2 = Evolution(problem2, num_of_generations=100, num_of_individuals=50, crossover_param=0.5, mutation_prob=0.01, mutation_param=0.05)
evol2 = evo2.evolve()

for i in range(len(evol2)-1):
    func=[j.objectives for j in evol2[i]]
    
    function1=[k[0] for k in func]
    function2=[k[1] for k in func]

    plt.scatter(function1, function2, label="Frente "+str(i+1))

plt.xlabel('Cantidad de triángulos', fontsize=15)
plt.ylabel('Error', fontsize=15)
plt.legend()
plt.title('Frontera de Pareto', fontsize=20)

plt.show()

print('vert', len(evol2[0][0].features[0]), 'triang', len(evol2[0][0].features[1].simplices))
print('f1', evol2[0][0].objectives[0], 'f2', evol2[0][0].objectives[1])

write_obj(evol2[0][0].features[0], evol2[0][0].features[1].simplices, '/Users/mariajosebernal/Documents/EAFIT/2022-2/Optimización/Proyecto/Caras 3D/Final/HombreNuevo2.obj')
