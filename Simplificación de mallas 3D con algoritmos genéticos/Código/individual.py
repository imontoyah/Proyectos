class Individual(object):

    def __init__(self):
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None
        self.objectives = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features[0].all() == other.features[0].all() and self.features[1].all() == other.features[1].all()
        return False

    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)

# Código tomado de:
# baopng, NSGA-II Python. GitHub [En línea]. Disponible en: 
# https://github.com/baopng/NSGA-II [Accedido: 04-Oct-2022].