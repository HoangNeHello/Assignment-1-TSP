# example.py
import os
import numpy as np
import ioh

# --- config you may tweak ---
DIM = 100                 # dimension of the bitstring
BUDGET = 10000            # #evaluations per run
RUNS = 20                 # independent runs per function
FUNCTIONS = [1, 2, 18]    # F1 OneMax, F2 LeadingOnes, F18 LABS
INSTANCE = 1              # use instance 1 for all
LOG_DIR = "ioh_logs"      # output folder for IOHanalyzer

# Random Search over {0,1}^n: sample fresh bitstrings, keep the best (logger will record)
def random_search(problem, budget, rng):
    best_fx = float("-inf")
    n = problem.meta_data.n_variables
    for _ in range(budget):
        x = rng.integers(0, 2, size=n, dtype=np.int32)
        fx = problem(x)              # evaluation is automatically logged
        if fx > best_fx:
            best_fx = fx

def main():
    os.makedirs(LOG_DIR, exist_ok=True)

    for fid in FUNCTIONS:
        # Create the problem from the PBO suite
        problem = ioh.get_problem(
            fid, dimension=DIM, instance=INSTANCE,
            problem_class=ioh.ProblemClass.PBO
        )

        # One logger per (fid) is fine; IOHanalyzer will see runs by run-id in the files
        logger = ioh.logger.Analyzer(
            root=os.getcwd(),
            folder_name=LOG_DIR,
            algorithm_name="RandomSearch",
            algorithm_info=f"budget={BUDGET},runs={RUNS}",
        )
        problem.attach_logger(logger)

        for run in range(RUNS):
            # set deterministic RNG per run
            rng = np.random.default_rng(seed=run + 12345)
            problem.reset()           # reset before each run
            random_search(problem, BUDGET, rng)

        logger.close()                # flush files

if __name__ == "__main__":
    main()
