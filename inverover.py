# inverover.py
from __future__ import annotations
import random
from typing import List, Tuple
from TSP import TSP

def tour_length(tsp: TSP, tour: List[int]) -> int:
    return tsp.tour_length(tour)

def inver_over(tsp: TSP, population_size: int = 50,
               generations: int = 20000, p: float = 0.02,
               seed: int | None = None) -> Tuple[List[int], int]:
    rng = random.Random(seed)
    n = tsp.n

    
    pop: List[List[int]] = []
    for _ in range(population_size):
        t = list(range(n))
        rng.shuffle(t)
        pop.append(t)

    best = min(pop, key=lambda t: tour_length(tsp, t))
    best_cost = tour_length(tsp, best)

    for _ in range(generations):
        new_pop: List[List[int]] = []
        for S in pop:
            Sprime = S[:]                  
            c = rng.choice(Sprime)         

            while True:
                
                if rng.random() < p:
                    cand = [x for x in Sprime if x != c]
                    c_prime = rng.choice(cand)
                else:
                    other = rng.choice(pop)
                    j_other = other.index(c)
                    c_prime = other[(j_other + 1) % n]

                i = Sprime.index(c)
                j = Sprime.index(c_prime)

                
                if (i + 1) % n == j or (j + 1) % n == i:
                    break

                
                a, b = (i + 1) % n, j
                if a <= b:
                    Sprime[a:b+1] = reversed(Sprime[a:b+1])
                else:
                    seg = Sprime[a:] + Sprime[:b+1]
                    seg.reverse()
                    k = 0
                    for t in range(a, n):
                        Sprime[t] = seg[k]; k += 1
                    for t in range(0, b+1):
                        Sprime[t] = seg[k]; k += 1
                c = c_prime

            
            old_cost = tour_length(tsp, S)
            new_cost = tour_length(tsp, Sprime)
            if new_cost < old_cost:
                S, old_cost = Sprime, new_cost

            if old_cost < best_cost:
                best, best_cost = S[:], old_cost

            new_pop.append(S)

        pop = new_pop

    return best, best_cost
