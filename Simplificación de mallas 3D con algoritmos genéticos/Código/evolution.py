from utils import NSGA2Utils
from population import Population

class Evolution:

    def __init__(self, problem, num_of_generations, num_of_individuals, crossover_param, mutation_prob, mutation_param):
        self.utils = NSGA2Utils(problem, num_of_individuals, crossover_param, mutation_prob, mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.num_of_individuals = num_of_individuals

    def evolve(self):
        print(1)
        self.population = self.utils.create_initial_population()
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        children = self.utils.create_children(self.population)
        returned_population = None
        for i in range(self.num_of_generations):
            print('Generación', i+1)
            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals-len(new_population)])
            returned_population = self.population
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)
        return returned_population.fronts

# Código tomado de:
# baopng, NSGA-II Python. GitHub [En línea]. Disponible en: 
# https://github.com/baopng/NSGA-II [Accedido: 04-Oct-2022].