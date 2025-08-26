# inverover.py
from __future__ import annotations
import random
from typing import List, Tuple
from TSP import TSP

def inver_over(tsp: TSP, population_size: int = 50,
               generations: int = 20000, p: float = 0.02,
               seed: int | None = None) -> Tuple[List[int], int]:
    rng = random.Random(seed)
    n = tsp.n

    # Use full matrix only when it’s safe; otherwise compute on the fly
    MATRIX_CACHE_THRESHOLD = 1500
    if n <= MATRIX_CACHE_THRESHOLD:
        M = tsp.dist_matrix()
        def w(a, b): return M[a][b]
    else:
        def w(a, b): return tsp.distance(a, b)

    def cost(tour):
        s = 0
        for k in range(n):
            s += w(tour[k], tour[(k + 1) % n])
        return s

    M = tsp.dist_matrix()
    def cost(tour: List[int]) -> int:
        s = 0
        for k in range(n):
            s += M[tour[k]][tour[(k + 1) % n]]
        return s

    # init population
    pop: List[List[int]] = []
    for _ in range(population_size):
        t = list(range(n))
        rng.shuffle(t)
        pop.append(t)

    best = min(pop, key=cost)
    best_cost = cost(best)

    for _ in range(generations):
        new_pop: List[List[int]] = []
        for S in pop:
            Sprime = S[:]
            c = rng.choice(Sprime)

            while True:
                # pick c'
                if rng.random() < p:
                    cand = [x for x in Sprime if x != c]
                    c_prime = rng.choice(cand)
                else:
                    other = rng.choice(pop)
                    j_other = other.index(c)
                    c_prime = other[(j_other + 1) % n]

                i = Sprime.index(c)
                j = Sprime.index(c_prime)

                # stop if adjacent (either side)
                if (i + 1) % n == j or (j + 1) % n == i:
                    break

                # invert from successor of c to c'
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

            # accept only if improved
            old_cost = cost(S)
            new_cost = cost(Sprime)
            if new_cost < old_cost:
                S, old_cost = Sprime, new_cost

            if old_cost < best_cost:
                best, best_cost = S[:], old_cost

            new_pop.append(S)

        pop = new_pop

    return best, best_cost
