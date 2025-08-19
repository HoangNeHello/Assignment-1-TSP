import random
from TSP import TSP 

def roulette_wheel_selection(population):
    # select an individual based on fitness proportionate selection

    fitness_values = [1 / ind.calulate_path_distance(ind.tour) for ind in population.individuals]
    total_fitness = sum(fitness_values)

    if total_fitness == 0:
        return random.choice(population.individuals)
    
    pick = random.uniform(0, total_fitness)
    current = 0
    for ind, fit in zip(population.individuals, fitness_values):
        current = current + fit
        if current >= pick:
            return ind        
    
    return random.choice(population.individuals)


def tournament_selection(individuals, tournament_size=3):
    # select an individual based on tournament selection

    contenders = random.sample(individuals, tournament_size)

    best = contenders[0]
    for ind in contenders[1:]:
        if ind.fitness < best.fitness():
            best = ind

    return best


def elitism(population, fitness_scores, elite_fraction = 0.2):
    # select the top elite faction of individuals based on fitness
    # lower fitness is better 
    
    paired = list(zip(population, fitness_scores))
    paired.sort(key=lambda x: x[1])

    num_elites = max(1, int(len(paired) * elite_fraction))
    elite_individuals = [ind for ind, score in paired[:num_elites]]

    return elite_individuals