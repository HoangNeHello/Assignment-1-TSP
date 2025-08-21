# test_class.py
import random, statistics
from TSP import TSP
from tsp_class import Individual, Population
from tsp_selection import roulette_wheel_selection, tournament_selection, elitism

def load_eil51_or_tiny():
    try:
        return TSP.from_file("TSPLIB/eil51.tsp")
    except Exception:
        tiny = """NAME : tiny5
TYPE : TSP
DIMENSION : 5
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
1 0 0
2 10 0
3 10 10
4 0 10
5 5 5
EOF"""
        return TSP.from_string(tiny)

def main():
    random.seed(42)  # reproducible
    tsp = load_eil51_or_tiny()
    pop = Population(tsp, size=50)

    # basic invariants
    n = tsp.n
    for ind in pop.individuals:
        assert len(ind.tour) == n and set(ind.tour) == set(range(n)), "not a permutation"

    fits = [ind.fitness() for ind in pop.individuals]
    mean_fit = statistics.fmean(fits)
    best_fit = min(fits)

    # selection sampling
    S = 1000
    rw = [roulette_wheel_selection(pop).fitness() for _ in range(S)]
    tourn = [tournament_selection(pop.individuals, tournament_size=5).fitness() for _ in range(S)]
    rw_avg = statistics.fmean(rw)
    tr_avg = statistics.fmean(tourn)

    # tolerances to handle randomness
    tol = 1.03  # 3% slack
    assert rw_avg <= mean_fit * tol, "roulette should be ~<= mean on average"
    assert tr_avg <= rw_avg * tol, "tournament should be at least as selective as roulette"
    elites = elitism(pop, elite_fraction=0.2)
    assert elites and elites[0].fitness() == best_fit, "best must be in elites"

    print("ALL TESTS PASSED ✅")
    print(f"mean={mean_fit:.2f} best={best_fit}  roulette={rw_avg:.2f}  tournament={tr_avg:.2f}")

if __name__ == "__main__":
    main()
