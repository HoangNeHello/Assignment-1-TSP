# mmas_only.py
import os, math
import numpy as np
import ioh

# --- config ---
DIM = 100
BUDGET = 100_000          # total evals per run (includes the initial x* eval)
RUNS = 10
FUNCTIONS = [1, 2, 3, 18, 23, 24, 25]
INSTANCE = 1
RHO_LIST = ["1", "1/sqrt(n)", "1/n"]   # printed labels; resolved at runtime
LOG_DIR = "ioh_logs_mmas"

def resolve_rho(label, n):
    if label == "1":
        return 1.0
    if label == "1/sqrt(n)":
        return 1.0 / math.sqrt(n)
    if label == "1/n":
        return 1.0 / n
    raise ValueError(label)

def construct_from_p(rng, p):
    # Sample x ~ Ber(p) independently per bit
    return (rng.random(p.size) < p).astype(np.int32)

def mmas(problem, budget, rho, rng):
    """MMAS (no star): accepts >=, updates every iteration, PBO construction."""
    n = problem.meta_data.n_variables
    tau_min, tau_max = 1.0 / n, 1.0 - 1.0 / n
    # Start with p_i = 1/2  (pheromones on 1-edges)
    p = np.full(n, 0.5, dtype=np.float64)

    # Initial best-so-far x*
    x_star = rng.integers(0, 2, size=n, dtype=np.int32)
    f_star = problem(x_star)  # logged by IOH
    evals = 1

    while evals < budget:
        # 1) construct candidate
        x = construct_from_p(rng, p)
        fx = problem(x); evals += 1

        # 2) accept ties (MMAS, no star)
        if fx >= f_star:
            x_star, f_star = x, fx

        # 3) pheromone update w.r.t x*   (then clamp to [1/n, 1-1/n])
        p *= (1.0 - rho)
        p += rho * x_star
        np.clip(p, tau_min, tau_max, out=p)

    return f_star

def run_all():
    os.makedirs(LOG_DIR, exist_ok=True)
    for fid in FUNCTIONS:
        problem = ioh.get_problem(fid, dimension=DIM, instance=INSTANCE,
                                  problem_class=ioh.ProblemClass.PBO)

        for rho_label in RHO_LIST:
            alg_name = f"MMAS(rho={rho_label})"

            # Create/attach the logger
            logger = ioh.logger.Analyzer(
                root=os.getcwd(),
                folder_name=LOG_DIR,
                algorithm_name=alg_name,
                algorithm_info=f"MMAS-no-star; budget={BUDGET}; runs={RUNS}",
            )
            problem.attach_logger(logger)

            for run in range(RUNS):
                rho_idx = RHO_LIST.index(rho_label)
                rng = np.random.default_rng(seed=12345 + 10_000*fid + 100*run + 1000*rho_idx)

                problem.reset()
                rho = resolve_rho(rho_label, problem.meta_data.n_variables)
                mmas(problem, BUDGET, rho, rng)

            # Flush files and detach
            logger.close()
            problem.detach_logger()

if __name__ == "__main__":
    run_all()
