# random_search.py
import os
import numpy as np
import ioh

DIM = 100
BUDGET = 100_000
RUNS = 10
FUNCTIONS = [1, 2, 3, 18, 23, 24, 25]
INSTANCE = 1
LOG_DIR = "ioh_logs_ex2_RS"

def random_search(problem, budget, rng):
    n = problem.meta_data.n_variables
    best = float("-inf")
    for _ in range(budget):
        x = rng.integers(0, 2, size=n, dtype=np.int32)
        fx = problem(x)            # IOH logs each evaluation
        if fx > best:
            best = fx

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    for fid in FUNCTIONS:
        problem = ioh.get_problem(fid, dimension=DIM, instance=INSTANCE,
                                  problem_class=ioh.ProblemClass.PBO)
        logger = ioh.logger.Analyzer(
            root=os.getcwd(),
            folder_name=LOG_DIR,
            algorithm_name="RandomSearch",
            algorithm_info=f"Ex2 RS; n={DIM}; runs={RUNS}; budget={BUDGET}",
        )
        problem.attach_logger(logger)

        for run in range(RUNS):
            rng = np.random.default_rng(seed=12345 + 1000*fid + run)
            problem.reset()
            random_search(problem, BUDGET, rng)

        logger.close()
        problem.detach_logger()

if __name__ == "__main__":
    main()
