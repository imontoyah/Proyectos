from individual import Individual
import random
import scipy.spatial
import numpy as np

class Problem:

    def __init__(self, objectives, num_of_variables, variables_range, initial_area):
        self.num_of_objectives = len(objectives)
        self.num_of_variables = num_of_variables
        self.objectives = objectives
        self.variables_range = variables_range
        self.initial_area = initial_area
        
    def generate_individual(self):
        individual = Individual()
        r=random.randint(3000,7000)
        nv=random.sample(range(0,len(self.variables_range)-14),r-14)
        newv=self.variables_range[nv]
        fix=self.variables_range[len(self.variables_range)-14:len(self.variables_range)]
        vertices=np.concatenate((newv,fix))
        faces=scipy.spatial.Delaunay(vertices[:,0:2])
        individual.features=[vertices,faces]
        return individual

    def calculate_objectives(self, individual):
        f1=self.objectives[0](individual.features[1])
        f2=self.objectives[1](individual.features[0], individual.features[1], self.variables_range, self.initial_area)
        individual.objectives = [f1, f2]

# Código tomado y adaptado de:
# baopng, NSGA-II Python. GitHub [En línea]. Disponible en: 
# https://github.com/baopng/NSGA-II [Accedido: 04-Oct-2022].