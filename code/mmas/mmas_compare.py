
import os
import math
import numpy as np
import ioh

# ---- Config ----
DIM = 100
BUDGET = 100_000        # evaluations per run (includes first eval)
RUNS = 10
FUNCTIONS = [1, 2, 3, 18, 23, 24, 25]
INSTANCE = 1
LOG_DIR = "ioh_logs_compare"   # single folder for all algorithms

# ---- Utilities ----
def attach_logger(problem, alg_name, alg_info):
    logger = ioh.logger.Analyzer(
        root=os.getcwd(),
        folder_name=LOG_DIR,
        algorithm_name=alg_name,
        algorithm_info=alg_info,
    )
    problem.attach_logger(logger)
    return logger

# ---- Algorithms ----

def random_search(problem, budget, rng):
    """Random Search as used in Exercise 2 (same budget, same n, 10 runs)."""
    n = problem.meta_data.n_variables
    best = float("-inf")
    # No need to retain x; IOH logs every evaluation via problem(x)
    for _ in range(budget):
        x = rng.integers(0, 2, size=n, dtype=np.int32)
        fx = problem(x)
        if fx > best:
            best = fx
    return best

def rls(problem, budget, rng):
    """Randomized Local Search: start uniform random; flip 1 random bit; accept >=."""
    n = problem.meta_data.n_variables
    # initial solution
    x = rng.integers(0, 2, size=n, dtype=np.int32)
    fx = problem(x)
    evals = 1
    while evals < budget:
        i = rng.integers(0, n)
        y = x.copy()
        y[i] ^= 1
        fy = problem(y); evals += 1
        if fy >= fx:
            x, fx = y, fy
    return fx

def one_plus_one_ea(problem, budget, rng):
    """(1+1) EA with bit-flip prob 1/n, accept >=, restart from current best each iteration."""
    n = problem.meta_data.n_variables
    # initial solution
    x = rng.integers(0, 2, size=n, dtype=np.int32)
    fx = problem(x)
    evals = 1
    while evals < budget:
        # mutate each bit with prob 1/n
        mask = rng.random(n) < (1.0 / n)
        # ensure at least one bit flips (common tweak); if not, flip one random bit
        if not mask.any():
            j = rng.integers(0, n)
            mask[j] = True
        y = x.copy()
        y[mask] ^= 1
        fy = problem(y); evals += 1
        if fy >= fx:
            x, fx = y, fy
    return fx

def resolve_rho(label, n):
    if label == "1":
        return 1.0
    if label == "1/sqrt(n)":
        return 1.0 / math.sqrt(n)
    if label == "1/n":
        return 1.0 / n
    raise ValueError(label)

def mmas(problem, budget, rho, rng):
    """MMAS (no-star): accepts ties; global-best update; pheromones clamped to [1/n, 1-1/n]."""
    n = problem.meta_data.n_variables
    tau_min, tau_max = 1.0 / n, 1.0 - 1.0 / n
    p = np.full(n, 0.5, dtype=np.float64)

    x_star = rng.integers(0, 2, size=n, dtype=np.int32)
    f_star = problem(x_star)
    evals = 1

    while evals < budget:
        x = (rng.random(n) < p).astype(np.int32)
        fx = problem(x); evals += 1
        if fx >= f_star:
            x_star, f_star = x, fx
        # pheromone update
        p *= (1.0 - rho)
        p += rho * x_star
        np.clip(p, tau_min, tau_max, out=p)

    return f_star

# ---- Runner ----
def run_all():
    os.makedirs(LOG_DIR, exist_ok=True)
    RHO_LIST = ["1", "1/sqrt(n)", "1/n"]

    for fid in FUNCTIONS:
        problem = ioh.get_problem(fid, dimension=DIM, instance=INSTANCE,
                                  problem_class=ioh.ProblemClass.PBO)

        # Random Search
        alg = "RandomSearch"
        logger = attach_logger(problem, alg, f"Compare; n={DIM}; runs={RUNS}; budget={BUDGET}")
        for run in range(RUNS):
            rng = np.random.default_rng(seed=10_000*fid + 100*run + 1)
            problem.reset()
            random_search(problem, BUDGET, rng)
        logger.close()
        problem.detach_logger()

        # RLS
        alg = "RLS"
        logger = attach_logger(problem, alg, f"Compare; n={DIM}; runs={RUNS}; budget={BUDGET}")
        for run in range(RUNS):
            rng = np.random.default_rng(seed=10_000*fid + 100*run + 2)
            problem.reset()
            rls(problem, BUDGET, rng)
        logger.close()
        problem.detach_logger()

        # (1+1) EA
        alg = "(1+1)EA"
        logger = attach_logger(problem, alg, f"Compare; n={DIM}; runs={RUNS}; budget={BUDGET}")
        for run in range(RUNS):
            rng = np.random.default_rng(seed=10_000*fid + 100*run + 3)
            problem.reset()
            one_plus_one_ea(problem, BUDGET, rng)
        logger.close()
        problem.detach_logger()

        # MMAS with 3 rho settings
        for rho_label in RHO_LIST:
            alg = f"MMAS(rho={rho_label})"
            logger = attach_logger(problem, alg, f"Compare; n={DIM}; runs={RUNS}; budget={BUDGET}")
            for run in range(RUNS):
                rng = np.random.default_rng(seed=10_000*fid + 100*run + {'1':11,'1/sqrt(n)':12,'1/n':13}[rho_label])
                problem.reset()
                rho = resolve_rho(rho_label, problem.meta_data.n_variables)
                mmas(problem, BUDGET, rho, rng)
            logger.close()
            problem.detach_logger()

if __name__ == "__main__":
    run_all()
