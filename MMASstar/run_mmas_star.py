# run_mmas_star.py
import os, math, numpy as np, ioh
from mmas_star import run_mmas_star_ioh

DIM = 100
BUDGET = 100_000
RUNS = 10
FUNCTIONS = [1, 2, 3, 18, 23, 24, 25]
INSTANCE = 1
RHO_LABELS = ["1", "1/sqrt(n)", "1/n"]
LOG_DIR = "ioh_logs_mmas_star"

def rho_of(label, n):
    if label == "1": return 1.0
    if label == "1/sqrt(n)": return 1.0 / math.sqrt(n)
    return 1.0 / n

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    for fid in FUNCTIONS:
        problem = ioh.get_problem(fid, dimension=DIM, instance=INSTANCE,
                                  problem_class=ioh.ProblemClass.PBO)
        for label in RHO_LABELS:
            alg_name = f"MMAS*(rho={label})"
            logger = ioh.logger.Analyzer(
                root=os.getcwd(),
                folder_name=LOG_DIR,
                algorithm_name=alg_name,
                algorithm_info=f"budget={BUDGET}, runs={RUNS}"
            )
            problem.attach_logger(logger)

            for run in range(RUNS):
                seed = 54321 + 10_000*fid + 1_000*RHO_LABELS.index(label) + run
                rng = np.random.default_rng(seed)
                problem.reset()
                rho = rho_of(label, DIM)
                run_mmas_star_ioh(problem, BUDGET, rho, rng)

            logger.close()
            problem.detach_logger()

if __name__ == "__main__":
    main()
