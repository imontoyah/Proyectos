class Population:

    def __init__(self):
        self.population = []
        self.fronts = []

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        return self.population.__iter__()

    def extend(self, new_individuals):
        self.population.extend(new_individuals)

    def append(self, new_individual):
        self.population.append(new_individual)

# Código tomado de:
# baopng, NSGA-II Python. GitHub [En línea]. Disponible en: 
# https://github.com/baopng/NSGA-II [Accedido: 04-Oct-2022].