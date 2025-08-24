from Selection import Tournament
from Selection import Elitism
import random

# ======================================================
# Memetic Genetic Algorithm implementation for TSP
# NOTE:
# - This file depends on:
#     1) Selection.py (which defines Tournament and Elitism functions)
#     2) A TSP class instance (must provide:
#          - attribute: n (number of cities)
#          - method: tour_length() that returns the cost of a route)
# ======================================================


def memetic_ga(tsp,pop_size,generations, mutation_rate=0.3, seed=1808,iter = 100):
    """
    Main memetic GA loop.
    - tsp: TSP class instance (with .n and .tour_length())
    - pop_size: population size
    - generations: number of iterations
    - mutation_rate: probability of mutation
    - seed: random seed for reproducibility
    - iter: number of iterations in local search (2-opt)
    """
    random_eg = random.Random(seed)
    
    #Initialize population with random permutations
    population = list()
    count = 0

    while count < pop_size:
        arrey = random_arrey(tsp.n,random_eg)
        population.append(arrey)
        count += 1

    #Evaluate initial population
    population = evaluate(population, tsp)

    generation = 0

    while generation < generations:
        #Parent selection
        parents = list()
        count = 0
        while count < pop_size:
            parent = Tournament(population,k=5)
            parents.append(parent)
            count +=1

        #Elitism
        elite = Elitism(population, size=2)

        #Number of children to generate
        childrens = list()
        children = pop_size - len(elite)

        #Crossover + Mutation + Local search (2-opt)
        count_c = 0
        while count_c < children:
            parent1 = random_eg.choice(parents)
            parent2 = random_eg.choice(parents)
            child = edge_recombination(parent1,parent2,random_eg)

            r = random_eg.random()
            if r < mutation_rate:
                child = insert_mutation(child,random_eg)

            child = two_opt(child, tsp, random_eg,iter)
            childrens.append(child)

            count_c +=1

        #Form next generation
        next_population = list()
        next_count = 0
        while next_count < len(childrens):
            next_population.append(childrens[next_count])
            next_count +=1
        
        c = 0
        while c < len(elite):
            next_population.append(elite[c])
            c +=1

        population = evaluate(next_population,tsp)
        generation +=1

    return best(population)



def random_arrey(n, r):
    """Generate a random permutation of n elements using Fisher-Yates shuffle."""
    n_list = list(range(n))

    for i in range(n-1,0,-1):
        j =  r.randrange(i+1)
        n_list[i],n_list[j] = n_list[j], n_list[i]

    return n_list

def evaluate(population, tsp):
    """
    Evaluate all individuals.
    population: list of routes (list[int]) or dicts with "generations".
    Returns: list of dicts with {"generations": route, "cost": cost}
    """
    eva = list()
    for i in population:
        if isinstance(i,dict):
            generation = list(i["generations"])
        else:
            generation = i
        cost = tsp.tour_length(generation)
        eva.append({"generations":generation, "cost":cost})
    return eva
    
def edge_recombination(p1, p2, r):
    """
    Edge recombination crossover.
    Input parents can be dicts or pure routes (lists).
    Returns: one child route (list[int]).
    """
    if isinstance(p1,dict):
        a = list(p1["generations"])
    else:
        a = list(p1)

    if isinstance(p2,dict):
        b = list(p2["generations"])
    else:
        b = list(p2)

    n= len(a)

    e_dict = dict()

    for i in a:
        e_dict[i] = set()

    for p in (a,b):
        for i in range(n):
            parent = p[i]
            ri= (i+1) % n
            l= (i-1) % n
            right = p[ri]
            left = p[l]
            s = e_dict[parent]
            s.add(right)
            s.add(left)

    start = r.choice(a)
    child = [start]

    while len(child) < n:
        for i in e_dict:
            if start in e_dict[i]:
                e_dict[i].remove(start)

        neighbors = list(e_dict[start])
        if len(neighbors) > 0:
            min_size = None
            choose = None
            for i in neighbors:
                c = len(e_dict[i])
                if (min_size is None) or (c < min_size):
                    min_size = c
                    choose = i
            ne = choose

        else:
            if_list = list()
            for i in a:
                if i not in child:
                    if_list.append(i)
            ne= r.choice(if_list)
        
        child.append(ne)
        start = ne
    
    return child

def insert_mutation(arrey, r):
    """Insert mutation: remove one city and reinsert at random position."""
    n = len(arrey)
    i = r.randrange(n)
    j = r.randrange(n)
    if i==j:
        return arrey[:]
    a= arrey[:]
    b = a.pop(i)
    a.insert(j,b)
    return a

def two_opt(arrey, tsp, r, iters):
    """
    Local search (2-opt).
    Iteratively reverse segments if it shortens the route.
    """
    n = len(arrey)
    arr= arrey[:]
    arr_len = tsp.tour_length(arr)

    count = 0
    while count < iters:
        i = r.randrange(n)
        j = r.randrange(n)
        if i>j:
            i, j = j, i
        if i == j:
            count +=1
            continue
        
        a = arr[:]
        a[i:j+1] = reversed(a[i:j+1])
        l = tsp.tour_length(a)
        
        if l < arr_len:
            arr = a
            arr_len = l
        count +=1
    
    return arr

def best(population):
    return min(population, key=lambda z: z["cost"])
