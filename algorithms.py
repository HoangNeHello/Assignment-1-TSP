from TSP import TSP
from tsp_class import Individual, Population

import variation
import tsp_selection
import Selection
import random

class Algorithm1:
    """
    Representation of an Evolutionary Algorithm for solving the TSP

    Attributes
    ----------
    popul : Population
    """
    def __init__(self, popul: Population):
        self.popul = popul

    # Test function for experimenting with generation structure
    @classmethod
    def testalgo(cls, starting_tsp: TSP, population_size: int, generations: int):
        # Population Initialisation
        cls.popul = Population(starting_tsp, population_size) # RANDOMISATION OF INITIAL TOURS REQUIRED

        # Main Generation Loop
        for i in range(generations):
            # Do Mutation/Crossover
            for i in cls.popul.individuals:
                i.tour = variation.insert_mutation(i.tour)

            # Check Distances
            for i in cls.popul.individuals:
                print(i.calulate_path_distance(i.tour))

            # Perform Selection



if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 4:
        print("Usage: python3 algorithms.py <path-to-tsplib-file.tsp> <population-size> <generation-num>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}")
        sys.exit(2)

    tsp = TSP.from_file(path)
    print(f"Loaded {tsp.name} with {tsp.n} nodes (EUC_2D).")
    print("d(0,1) =", tsp.distance(0, 1))
    print("Naive tour length:", tsp.tour_length(list(range(tsp.n))))

    pop_size = int(sys.argv[2])
    gen_num = int(sys.argv[3])

    alg = Algorithm1
    alg.testalgo(tsp, pop_size, gen_num)
