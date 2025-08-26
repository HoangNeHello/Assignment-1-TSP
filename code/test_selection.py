# test_selection.py
import random, statistics
import Selection  

def test_on_numbers():
    print("=== Synthetic numbers (lower is better) ===")
    population = [10, 20, 30, 40, 50]   # fitness values (distances)
    mean_fit = statistics.fmean(population)
    print("Population:", population, "mean:", mean_fit)

    S = 1000
    rw = [Selection.Fitness_proportional(population) for _ in range(S)]
    tw = [Selection.Tournament(population, k=3, p=0.8) for _ in range(S)]
    elites = Selection.Elitism(population, size=2)

    print("Fitness_proportional avg:", round(statistics.fmean(rw), 2))
    print("Tournament avg:", round(statistics.fmean(tw), 2))
    print("Elites (top 2):", elites)
    print()

def test_on_eil51():
    print("=== Real fitness values from eil51 ===")
    from TSP import TSP
    from tsp_class import Population

    random.seed(42)
    tsp = TSP.from_file("TSPLIB/eil51.tsp")
    pop = Population(tsp, size=50)

    # Build a numeric list of distances for selection functions
    fits = [ind.fitness() for ind in pop.individuals]
    mean_fit = statistics.fmean(fits)
    best_fit = min(fits)
    print("n =", tsp.n, "pop size =", len(fits))
    print("Pop mean:", round(mean_fit, 2), "| best:", best_fit)

    S = 1000
    rw = [Selection.Fitness_proportional(fits) for _ in range(S)]
    tw = [Selection.Tournament(fits, k=5, p=0.8) for _ in range(S)]
    elites = Selection.Elitism(fits, size=5)

    print("Fitness_proportional avg:", round(statistics.fmean(rw), 2))
    print("Tournament avg:", round(statistics.fmean(tw), 2))
    print("Elites (5 best):", elites)

if __name__ == "__main__":
    random.seed(123)
    test_on_numbers()
    test_on_eil51()
