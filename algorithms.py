from TSP import TSP
from tsp_class import Individual, Population

import variation
import tsp_selection
import Selection
import random

class Algorithm:
    """
    Representation of an Evolutionary Algorithm for solving the TSP

    Attributes
    ----------
    popul : Population
    """
    def __init__(self, popul: Population):
        self.popul = popul

    # Function for running genetic algorithm. algorithm_num defines which algorithm is run
    @classmethod
    def genalgo(cls, algorithm_num: int, starting_tsp: TSP, population_size: int, generations: int):
        # Population Initialisation
        cls.popul = Population(starting_tsp, population_size) # RANDOMISATION OF INITIAL TOURS REQUIRED

        mating_pool: list[Individual]
        mating_pool = [] * len(cls.popul.individuals)

        # Main Generation Loop
        for i in range(generations):
            # Check which algorithm is selected
            match algorithm_num:
                case 1:
                    # Select parents for mating pool with Proportional Selection based on Distance
                    cls.popul.individuals.sort(key = Individual.distance_helper)

                    mating_pool = [] * len(cls.popul.individuals)
                    for j in range(len(cls.popul.individuals)):
                        mating_pool.append(Selection.Fitness_proportional(cls.popul.individuals))

                    # Perform Ordered Crossover on parents
                    for j in range(0, len(mating_pool), 2):
                        if j+1 < len(mating_pool):
                            cls.popul.individuals[j].tour, cls.popul.individuals[j+1].tour = variation.ordered_crossover(mating_pool[j].tour, mating_pool[j+1].tour)

                    # Perform Insert Mutation on children
                    for j in cls.popul.individuals:
                        j.tour = variation.insert_mutation(j.tour)

                case 2:
                    # Select breeding pool with Elitism Selection
                    cls.popul.individuals.sort(key = Individual.distance_helper)
                    
                    mating_pool = [] * len(cls.popul.individuals)
                    mating_pool = tsp_selection.elitism(cls.popul.individuals)
                    print(mating_pool)
                    
                    # Breed based on Roulette Selection
                    popul_size = len(cls.popul.individuals)

                    end = len(mating_pool)
                    j = len(mating_pool)
                    while len(mating_pool) < popul_size:
                        print(j)
                        parenta = Selection.Fitness_proportional(mating_pool[:end])
                        print("parenta assigned")
                        parentb = Selection.Fitness_proportional(mating_pool[:end])
                        print("parentb assigned")
                        mating_pool.append(cls.popul.individuals[j])
                        print("appended to mating_pool")
                        mating_pool[j].tour = variation.pmx_crossover(parenta.tour, parentb.tour)
                        print("mating_pool tour overwritten")
                        j += 1

                    print(mating_pool)

                case 3:
                    indiv = cls.popul.individuals

                    print(indiv[0].tour)
                    print(indiv[1].tour)
                    indiv[2].tour = variation.pmx_crossover(indiv[0].tour, indiv[1].tour)
                    print(indiv[2].tour)
                
                case _:
                    print("ERROR: algorithm ", algorithm_num, " is invalid. Valid numbers are from 1-3")
                    return

        cls.popul.individuals.sort(key = Individual.distance_helper)
        print(cls.popul.individuals[0])
        return


if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 5:
        print("Usage: python3 algorithms.py <path-to-tsplib-file.tsp> <algorithm-num> <population-size> <generation-num>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}")
        sys.exit(2)

    tsp = TSP.from_file(path)
    print(f"Loaded {tsp.name} with {tsp.n} nodes (EUC_2D).")
    print("d(0,1) =", tsp.distance(0, 1))
    print("Naive tour length:", tsp.tour_length(list(range(tsp.n))))

    alg_num = int(sys.argv[2])
    pop_size = int(sys.argv[3])
    gen_num = int(sys.argv[4])

    alg = Algorithm
    alg.genalgo(alg_num, tsp, pop_size, gen_num)
