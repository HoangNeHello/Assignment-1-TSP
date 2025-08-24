import random

def Fitness_proportional (population):

    Total_Fitness = 0.0

    for i in population:
        Total_Fitness += 1.0 / (1.0 + i)
    
    pointer = random.uniform(0.0, Total_Fitness)
    
    count = 0.0

    for i in population:
        count += 1.0/(1.0+i)
        if count >= pointer:
            return i

    

def Tournament(population,k=5,p=0.8):

    k = min(k, len(population))

    select = random.sample(population,k)

    select.sort(key=lambda ind: ind["cost"])

    for i, j in enumerate(select):
        if random.random() < p or i == len(select) - 1:
            return j


def Elitism(population,size=1):

    size = max(0, min(size, len(population)))

    e_sort = sorted(population, key=lambda ind: ind["cost"])

    e = e_sort[:size]

    return e
