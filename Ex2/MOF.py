import random

def dominates(a, b):
    not_worse = True
    a_iter = iter(a)
    b_iter = iter(b)

    while True:
        try:
            x = next(a_iter)
            y = next(b_iter)
        except StopIteration:
            break
        if not (x >= y):
            not_worse = False
            break

    better = False
    a_iter2 = iter(a)
    b_iter2 = iter(b)
    while True:
        try:
            x = next(a_iter2)
            y = next(b_iter2)
        except StopIteration:
            break
        if x > y:
            better = True
            break

    return (not_worse and better)

def evaluate(problem, solution):
    f1_raw = problem(solution)
    if problem.meta_data.problem_id < 2300:
        f1 = -f1_raw
    else:
        f1 = f1_raw
    f2 = -sum(solution)
    return (f1, f2)

def mutate(individual):
    length = len(individual)
    mutated = list()
    count = 0
    while count < length:
        bit = individual[count]
        r = random.random()
        threshold = 1.0 / float(length)
        if r < threshold:
            new_bit = 1 - bit
        else:
            new_bit = bit
        mutated.append(new_bit)
        count += 1
    return mutated