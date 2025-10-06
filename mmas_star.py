# mmas_star.py
import numpy as np
import ioh

def run_mmas_star_ioh(problem, budget: int, rho: float, rng: np.random.Generator):
    n = problem.meta_data.n_variables
    tau_min, tau_max = 1.0/n, 1.0-1.0/n
    p = np.full(n, 0.5, dtype=np.float64)

    x_best = rng.integers(0, 2, size=n, dtype=np.int32)
    f_best = problem(x_best)
    evals = 1

    while evals < budget:
        x = (rng.random(n) < p).astype(np.int32)
        fx = problem(x); evals += 1
        if fx > f_best:
            x_best, f_best = x, fx
        p *= (1.0 - rho); p += rho * x_best
        np.clip(p, tau_min, tau_max, out=p)
    return f_best
