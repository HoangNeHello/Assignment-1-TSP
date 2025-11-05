import random
import numpy as np
import ioh
from MOF import dominates, mutate, evaluate

def gsemo(problem, budget=10000):
    n = problem.meta_data.n_variables

    current_array = np.random.randint(0, 2, size=n)
    current = current_array.tolist()
    obj = evaluate(problem, current)
    population = list()
    population.append((current, obj))
    log = list()

    while problem.state.evaluations < budget:
        parent, parent_obj = random.choice(population)
        offspring = mutate(parent)
        offspring_obj = evaluate(problem, offspring)

        boolean = False
        j = 0
        while j < len(population):
            p = population[j][1]
            if dominates(p, offspring_obj):
                boolean = True
                break
            j += 1

        if boolean:
            continue

        new_population = list()
        n = 0
        while n < len(population):
            p = population[n]
            if not dominates(offspring_obj, p[1]):
                new_population.append(p)
            n +=1
        population = new_population

        population.append((offspring, offspring_obj))

        best_f1 = None
        t = 0
        while t < len(population):
            obj_t = population[t][1]
            f1_value = obj_t[0]
            if best_f1 is None:
                best_f1 = f1_value
            else:
                if f1_value > best_f1:
                    best_f1 = f1_value
            t += 1

        log.append((problem.state.evaluations, best_f1))

    return population, log