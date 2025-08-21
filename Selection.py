import random

def Fitness_proportional (population):

    total = sum(1.0 / (1.0 + x) for x in population)
    if total <= 0:
        return random.choice(population)
    pointer = random.uniform(0.0, total)
    acc = 0.0
    for x in population:
        acc += 1.0 / (1.0 + x)   
        if acc >= pointer:
            return x
    return population[-1]

    

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