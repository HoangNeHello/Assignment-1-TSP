from tsp_class import Individual, Population
import random

def Fitness_proportional(population: list[Individual]) -> Individual:

    Total_Fitness = 0.0

    for i in range(len(population)):
        Total_Fitness += 1.0 / 1.0 + i
    
    pointer = random.uniform(0.0, 1.0)
    
    count = 0.0
    j = 1

    for i in reversed(population):
        count += j/Total_Fitness
        if pointer < count:
            return i
        j += 1

    return random.choice(population)

    

def Tournament(population,k=5,p=0.8):

    select = random.sample(population,k)

    select.sort()

    for i, j in enumerate(select):
        if random.random() < p or i == len(select) - 1:
            return j


def Elitism(population,size=1):

    e_sort = sorted(population)

    e = e_sort[:size]

    return e
