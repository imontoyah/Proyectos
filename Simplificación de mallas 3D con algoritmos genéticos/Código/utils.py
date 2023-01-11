from population import Population
from individual import Individual
import random
import numpy as np
import scipy.spatial

class NSGA2Utils:

    def __init__(self, problem, num_of_individuals, crossover_param, mutation_prob, mutation_param):
        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.crossover_param = crossover_param
        self.mutation_prob = mutation_prob
        self.mutation_param = mutation_param

    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generate_individual()
            self.problem.calculate_objectives(individual)
            population.append(individual)
        return population

    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10**9
                front[solutions_num-1].crowding_distance = 10**9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num-1):
                    front[i].crowding_distance += (front[i+1].objectives[m] - front[i-1].objectives[m])/scale

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def create_children(self, population):
        children = []
        while len(children) < len(population):
            r1=random.randint(0, len(population)-1)
            r2=random.randint(0,len(population)-1)
            while r1==r2:
                r2=random.randint(0,len(population)-1)
            parent1 = population.population[r1]
            parent2 = population.population[r2]
            child = self.__crossover(parent1, parent2)
            self.__mutate(child)
            self.problem.calculate_objectives(child)
            children.append(child)

        return children

    def __crossover(self, individual1, individual2):
        fix=individual1.features[0][len(individual1.features[0])-14:len(individual1.features[0])]
        ind1=individual1.features[0][0:len(individual1.features[0])-13]
        ind2=individual2.features[0][0:len(individual2.features[0])-13]

        r=random.randint(min(len(ind1),len(ind2)), max(len(ind1),len(ind2)))
        num1=int((r-14)*self.crossover_param)

        child=Individual()
        nv1=random.sample(range(0,len(ind1)),min(num1,len(ind1)))
        newv1=ind1[nv1]

        num2=r-14-len(newv1)

        ind1rows = newv1.view([('', newv1.dtype)] * newv1.shape[1])
        ind2rows = ind2.view([('', ind2.dtype)] * ind2.shape[1])
        unique=np.setdiff1d(ind2rows, ind1rows).view(ind2.dtype).reshape(-1, newv1.shape[1])

        if(min(num2,len(unique))<0):
            print(len(unique))
            print(r)
            print(len(newv1))
            print(min(num2,len(unique)))

        nv2=random.sample(range(0,len(unique)),min(num2,len(unique)))
        newv2=unique[nv2]

        vertices=np.concatenate((newv1, newv2, fix))

        faces=scipy.spatial.Delaunay(vertices[:,0:2])
        child.features=[vertices,faces]

        return child

    def __mutate(self, child):
        r=random.random()
        if(r<self.mutation_prob):
            rr=random.random()
            q=int(len(child.features[0])*self.mutation_param)
            if(rr<0.5):
                dv=random.sample(range(0,len(child.features[0])-14),q)
                vertices=np.delete(child.features[0], dv, 0)
            else:
                vrrows=self.problem.variables_range.view([('', self.problem.variables_range.dtype)] * self.problem.variables_range.shape[1])
                childrows=child.features[0].view([('', child.features[0].dtype)] * child.features[0].shape[1])
                unique=np.setdiff1d(vrrows, childrows).view(self.problem.variables_range.dtype).reshape(-1, child.features[0].shape[1])
                nv=random.sample(range(0,len(unique)),q)
                newv=unique[nv]
                vertices=np.concatenate((child.features[0], newv))

            faces=scipy.spatial.Delaunay(vertices[:,0:2])
            child.features=[vertices, faces]

# Código tomado y adaptado de:
# baopng, NSGA-II Python. GitHub [En línea]. Disponible en: 
# https://github.com/baopng/NSGA-II [Accedido: 04-Oct-2022].