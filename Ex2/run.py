#!/usr/bin/env python3
import random
import numpy as np
import ioh
from ioh import logger
from GSEMO import gsemo  # expected: gsemo(problem, budget) -> (best_solution, trace)

def run_experiments(problem_ids, budget=10_000, runs=30):
    for pid in problem_ids:
        L = logger.Analyzer(
            root="GSEMO_logs",
            folder_name=f"GSEMO_id{pid}",
            algorithm_name="GSEMO",
            algorithm_info=f"budget={budget}; runs={runs}"
        )
        # Add per-eval trigger later if stable: L.add_trigger(logger.trigger.Each(1))

        problem = ioh.get_problem(pid, problem_class=ioh.ProblemClass.GRAPH)
        try:
            problem.attach_logger(L)
            for r in range(runs):
                # seed external RNGs so each run is independent
                random.seed(r)
                np.random.seed(r)
                problem.reset()
                _best, _trace = gsemo(problem, budget=budget)  # no seed kwarg
            print(f"Completed problem {pid} for {runs} runs")
        finally:
            try: problem.detach_logger()
            except Exception: pass
            del L  # flush files

if __name__ == "__main__":
    problem_ids = [
        2100, 2101, 2102, 2103,  # MaxCoverage
        2200, 2201, 2202, 2203,  # MaxInfluence
        2300, 2301, 2302         # PackWhileTravel (for Ex2 third bullet)
    ]
    run_experiments(problem_ids, budget=10_000, runs=30)
