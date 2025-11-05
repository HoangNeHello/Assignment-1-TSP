#!/usr/bin/env python3
from __future__ import annotations
from ioh import get_problem, ProblemClass, logger
import numpy as np

# --------- SOEA: same call signature style as problem_example.py ---------
def soea(func, runs: int = 30, budget: int | None = None,
         mu: int = 50, lam: int = 50, pc: float = 0.9, pm: float | None = None,
         seed: int = 0, exact_k: bool = False, k_frac: float = 0.2):
    """
    func: IOH problem (GRAPH)
    runs: independent runs (30 for the assignment)
    budget: evaluations per run (100_000 for Ex4)
    mu, lam: population and offspring sizes
    pc: crossover prob (uniform crossover)
    pm: mutation prob (default 1/n)
    exact_k: if True, init + mutate preserve |x|=round(k_frac*n) via swaps
    """
    n = func.meta_data.n_variables
    if budget is None:
        budget = 100_000
    if pm is None:
        pm = 1.0 / n
    k = max(1, int(round(k_frac * n)))

    rng = np.random.default_rng(seed)

    def init_ind():
        if exact_k:
            x = np.zeros(n, dtype=int)
            idx = rng.choice(n, size=k, replace=False)
            x[idx] = 1
            return x
        return rng.integers(0, 2, size=n, dtype=int)

    def mutate(x):
        y = x.copy()
        if exact_k:
            ones = np.flatnonzero(y)
            zeros = np.flatnonzero(1 - y)
            if ones.size and zeros.size:
                i = rng.choice(ones); j = rng.choice(zeros)
                y[i] = 0; y[j] = 1
            return y
        # standard bit-flip with ≥1 flip
        flips = rng.random(n) < pm
        if not flips.any():
            flips[rng.integers(n)] = True
        y[flips] ^= 1
        return y

    def crossover(a, b):
        mask = rng.integers(0, 2, size=n, dtype=bool)
        c = a.copy()
        c[mask] = b[mask]
        return c

    def tsel(pop):
        # tournament of size 2 on fitness
        i, j = rng.integers(len(pop), size=2)
        return pop[i] if pop[i][0] >= pop[j][0] else pop[j]

    # ---- Run the algorithm 'runs' times, resetting IOH in between ----
    for r in range(runs):
        evals = 0

        # init population
        pop = []
        for _ in range(mu):
            x = init_ind()
            f = float(func(x)); evals += 1
            pop.append((f, x))
            if evals >= budget: break
        pop.sort(key=lambda t: t[0], reverse=True)
        best_f = pop[0][0]

        # main loop
        while evals < budget:
            off = []
            for _ in range(lam):
                p1 = tsel(pop)[1]
                if rng.random() < pc:
                    p2 = tsel(pop)[1]
                    c = crossover(p1, p2)
                else:
                    c = p1.copy()
                c = mutate(c)
                f = float(func(c)); evals += 1
                off.append((f, c))
                if evals >= budget: break

            # μ + λ replacement (pure fitness)
            merged = pop + off
            merged.sort(key=lambda t: t[0], reverse=True)
            pop = merged[:mu]
            if pop[0][0] > best_f:
                best_f = pop[0][0]

        # very important for IOH runs
        func.reset()

# --------- Declare your GRAPH problems (assignment instances) ----------
GRAPH_IDS = [
    2100, 2101, 2102, 2103,  # MaxCoverage
    2200, 2201, 2202, 2203,  # MaxInfluence
]

# --------- Create ONE logger like in problem_example.py & run all ----------
if __name__ == "__main__":
    # Create IOH Analyzer logger (same pattern as problem_example.py)
    l = logger.Analyzer(
        root="SOEA_results_50",                 # updated to reflect μ=50
        algorithm_name="SOEA-50",
        algorithm_info="SOEA Ex3; mu=50, lam=50, pc=0.9, pm=1/n; runs=30; budget=10000"
    )
    # Optional but recommended: per-evaluation logging for smooth fixed-budget curves
    # l.add_trigger(logger.trigger.Each(1))

    # Attach → run → reset for each GRAPH problem (following the example style)
    for fid in GRAPH_IDS:
        prob = get_problem(fid=fid, problem_class=ProblemClass.GRAPH)
        prob.attach_logger(l)
        soea(prob, runs=30, budget=100_000, mu=50, lam=50, pc=0.9, pm=None,
             seed=0, exact_k=False, k_frac=0.2)
        # NOTE: soea() calls prob.reset() after each run (as in the example)

    # Make sure data is flushed
    del l
