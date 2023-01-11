import numpy as np
import math
import scipy.spatial
import matplotlib.pyplot as plt
from torch_geometric.data import Data
import openmesh

#Calcula la altura de un punto en un plano formado por un triángulo
def height(t, v):
    a=(t[1][1]-t[0][1])*(t[2][2]-t[0][2])-(t[2][1]-t[0][1])*(t[1][2]-t[0][2])
    b=-((t[1][0]-t[0][0])*(t[2][2]-t[0][2])-(t[2][0]-t[0][0])*(t[1][2]-t[0][2]))
    c=(t[1][0]-t[0][0])*(t[2][1]-t[0][1])-(t[2][0]-t[0][0])*(t[1][1]-t[0][1])
    d=-t[0][0]*a-t[0][1]*b-t[0][2]*c

    z=1/c*(-a*v[0]-b*v[1]-d)

    return z

#Calcula el producto punto entre dos vectores
def dot(a,b):
    d=a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
    return d

#Calcula la norma euclídea de un vector
def norm(a):
    n=math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])
    return n

#Calcula el ángulo entre dos vectores
def angle(a,b):
    cosang=dot(a,b)/(norm(a)*norm(b))
    ang=math.acos(cosang)
    return ang

#Calcula el área de un triángulo
def area(t):
    a=[t[1][0]-t[0][0], t[1][1]-t[0][1], t[1][2]-t[0][2]]
    b=[t[2][0]-t[0][0], t[2][1]-t[0][1], t[2][2]-t[0][2]]

    ar=1/2*norm(a)*norm(b)*math.sin(angle(a,b))
    return ar

#minimizar la cantidad de triángulos
def f1(faces):
    triangles=len(faces.simplices)
    return triangles

 #minimizar el error del área superficial
def f2(vertices, faces, variable_range, initial_area):
    facess=faces.simplices
    new_area=0
    for i in range(len(facess)):
        t=[vertices[facess[i][0]], vertices[facess[i][1]], vertices[facess[i][2]]]
        new_area+=area(t)
    return abs(initial_area-new_area)

#minimizar el error de los vértices no tomados
def f3(vertices, faces, variable_range, initial_area): 
    error=0
    indrows=vertices.view([('', vertices.dtype)] * vertices.shape[1])
    orirows=variable_range.view([('', variable_range.dtype)] * variable_range.shape[1])
    unique=np.setdiff1d(orirows, indrows).view(variable_range.dtype).reshape(-1, vertices.shape[1])

    for i in range(len(unique)):
        point=[unique[i][0],unique[i][1]]
        pos=faces.find_simplex(point)
        if(pos==-1): 
            continue
        tri=np.array([vertices[faces.simplices[pos][0]],vertices[faces.simplices[pos][1]],vertices[faces.simplices[pos][2]]])
        h=height(tri,point)
        error+=abs(h-unique[i][2])

    return error

#Leer archivo .obj
def read_obj(path):
    if openmesh is None:
        raise ImportError('`read_ply` requires the `openmesh` package.')

    mesh = openmesh.read_trimesh(path)

    return mesh.points(), mesh.face_vertex_indices()

#Guardar archivo .obj
def write_obj(vertices, faces, out_file):
    file=open(out_file, 'w')
    for v in vertices:
        file.write("v %.6f %.6f %.6f\n" % (v[0], v[1], v[2]))
    for p in faces:
        file.write("f")
        for i in p:
            file.write(" %d" % (i + 1))
        file.write("\n")