import random
import itertools
from typing import List, Optional
from TSP import TSP 

class Individual:
    # represents a possible solution to the TSP as a premutation of given cities
    def __init__(self, tsp: TSP, tour: Optional[List[int]] = None):
        self.tsp = tsp
        self.num_cities = tsp.n 

        if tour is None:
            self.tour = list(range(self.num_cities))

        else:
            if len(tour) != self.num_cities:
                raise ValueError("Tour length must match number of cities")
            self.tour = list(tour)

        random.shuffle(self.tour)

    def calulate_path_distance(self, path: List[int]) -> int:
        
        return self.tsp.tour_length(path)

    def brute_force_tour (self) -> tuple [list[int], int]:
        
        best_path = None
        min_distance = float("inf")

        for perm in itertools.permutations(range(1, self.num_cities)):
            current_path = [0] + list(perm) + [0]
            current_distance = self.calulate_path_distance(current_path)

            if current_distance < min_distance:
                min_distance = current_distance
                best_path = current_path 

        return best_path, min_distance

    def distance_helper(self) -> int:
        return self.tsp.tour_length(self.tour)

    def __repr__(self) -> str:
        return f"Individual(tour={self.tour}, distance={self.calulate_path_distance(self.tour)})"         
                                       
        
class Population:
    # represents a population (set) of individuals

    def __init__(self, tsp: TSP, size: int):
        self.tsp = tsp
        self.size = size
        self.individuals = [Individual(tsp) for _ in range(size)]

    def best_individual(self) -> Individual:
        return min(self.individuals, key=lambda ind: ind.calulate_path_distance(ind.tour))
    
    def __repr__(self):
        return f".join(str(ind) for ind in self.individuals)"
    

