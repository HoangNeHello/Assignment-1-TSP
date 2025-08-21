# import random
# import itertools
# from typing import List, Optional
# from TSP import TSP 

# class Individual:
#     # represents a possible solution to the TSP as a premutation of given cities
#     def __init__(self, tsp: TSP, tour: Optional[List[int]] = None):
#         self.tsp = tsp
#         self.num_cities = tsp.n 

#         if tour is None:
#             self.tour = list(range(self.num_cities))

#         else:
#             if len(tour) != self.num_cities:
#                 raise ValueError("Tour length must match number of cities")
#             self.tour = list(tour)

#     def calulate_path_distance(self, path: List[int]) -> int:
        
#         return self.tsp.tour_cost(path)

#     def brute_force_tour (self) -> tuple [list[int], int]:
        
#         best_path = None
#         min_distance = float("inf")

#         for perm in itertools.permutations(range(1, self.num_cities)):
#             current_path = [0] + list(perm) + [0]
#             current_distance = self.calulate_path_distance(current_path)

#             if current_distance < min_distance:
#                 min_distance = current_distance
#                 best_path = current_path 

#         return best_path, min_distance

#     def __repr__(self) -> str:
#         return f"Individual(tour={self.tour}, distance={self.calulate_path_distance(self.tour)})"         
                                       
        
# class Population:
#     # represents a population (set) of individuals

#     def __init__(self, tsp: TSP, size: int):
#         self.tsp = tsp
#         self.size = size
#         self.individuals = [Individual(tsp) for _ in range(size)]

#     def best_individual(self) -> Individual:
#         return min(self.individuals, key=lambda ind: ind.calulate_path_distance(ind.tour))
    
#     def __repr__(self):
#         return f".join(str(ind) for ind in self.individuals)"
    

# tsp_class.py
import random
import itertools
from typing import List, Optional
from TSP import TSP

class Individual:
    """Permutation encoding of a TSP tour (nodes 0..n-1)."""
    def __init__(self, tsp: TSP, tour: Optional[List[int]] = None, random_init: bool = True):
        self.tsp = tsp
        self.num_cities = tsp.n

        if tour is None:
            # O(n) uniform random permutation (Fisher–Yates via random.shuffle)
            self.tour = list(range(self.num_cities))
            if random_init:
                random.shuffle(self.tour)
        else:
            if len(tour) != self.num_cities:
                raise ValueError("Tour length must match number of cities")
            # (Optionally validate permutation:)
            # if set(tour) != set(range(self.num_cities)): raise ValueError("Tour must be a permutation")
            self.tour = list(tour)

    # ---------- evaluation ----------
    def fitness(self) -> int:
        """Lower is better (total tour length; returns to start by TSP.tour_length default)."""
        return self.tsp.tour_length(self.tour)

    # Backward-compatibility aliases (if other code still calls these)
    def calculate_path_distance(self, path: List[int]) -> int:
        return self.tsp.tour_length(path)

    def calulate_path_distance(self, path: List[int]) -> int:  # keep the typo as alias
        return self.calculate_path_distance(path)

    # (Optional) brute force — only feasible for very small n
    def brute_force_tour(self) -> tuple[list[int], int]:
        best_path, best_len = None, float("inf")
        # Let TSP.tour_length handle closing the loop; no need to add [0] ... [0]
        for perm in itertools.permutations(range(self.num_cities)):
            L = self.tsp.tour_length(list(perm))
            if L < best_len:
                best_len, best_path = L, list(perm)
        return best_path, best_len

    def __repr__(self) -> str:
        return f"Individual(len={self.num_cities}, fitness={self.fitness()})"


class Population:
    """A population (set) of Individuals."""
    def __init__(self, tsp: TSP, size: int):
        if size <= 0:
            raise ValueError("Population size must be positive")
        self.tsp = tsp
        self.size = size
        self.individuals = [Individual(tsp) for _ in range(size)]

    def best_individual(self) -> Individual:
        return min(self.individuals, key=lambda ind: ind.fitness())

    def __repr__(self) -> str:
        return "\n".join(str(ind) for ind in self.individuals)
