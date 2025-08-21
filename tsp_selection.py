# import random
# from TSP import TSP 

# def roulette_wheel_selection(population):
#     # select an individual based on fitness proportionate selection

#     fitness_values = [1 / ind.calulate_path_distance(ind.tour) for ind in population.individuals]
#     total_fitness = sum(fitness_values)

#     if total_fitness == 0:
#         return random.choice(population.individuals)
    
#     pick = random.uniform(0, total_fitness)
#     current = 0
#     for ind, fit in zip(population.individuals, fitness_values):
#         current = current + fit
#         if current >= pick:
#             return ind        
    
#     return random.choice(population.individuals)


# def tournament_selection(individuals, tournament_size=3):
#     # select an individual based on tournament selection

#     contenders = random.sample(individuals, tournament_size)

#     best = contenders[0]
#     for ind in contenders[1:]:
#         if ind.fitness < best.fitness():
#             best = ind

#     return best


# def elitism(population, fitness_scores, elite_fraction = 0.2):
#     # select the top elite faction of individuals based on fitness
#     # lower fitness is better 
    
#     paired = list(zip(population, fitness_scores))
#     paired.sort(key=lambda x: x[1])

#     num_elites = max(1, int(len(paired) * elite_fraction))
#     elite_individuals = [ind for ind, score in paired[:num_elites]]

#     return elite_individuals

# tsp_selection.py
import random

def roulette_wheel_selection(population):
    """Fitness-proportionate selection (lower tour length => higher weight)."""
    # compute weights = 1 / distance, with guards
    distances = [ind.fitness() for ind in population.individuals]
    weights = [1.0 / max(1.0, float(d)) for d in distances]
    total = sum(weights)
    if total <= 0:
        return random.choice(population.individuals)
    r, acc = random.uniform(0, total), 0.0
    for ind, w in zip(population.individuals, weights):
        acc += w
        if acc >= r:
            return ind
    return population.individuals[-1]

def tournament_selection(individuals, tournament_size=3):
    """Pick the best (lowest distance) among k random contenders."""
    k = min(tournament_size, len(individuals))
    contenders = random.sample(individuals, k=k)
    return min(contenders, key=lambda ind: ind.fitness())

def elitism(population, elite_fraction=0.2):
    """Return the top fraction by fitness (ascending distance)."""
    inds = sorted(population.individuals, key=lambda ind: ind.fitness())
    k = max(1, int(len(inds) * elite_fraction))
    return inds[:k]