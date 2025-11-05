# MOEA-10.py
from ioh import get_problem, ProblemClass, logger
from moea_core import run_moea_graph

GRAPH_IDS = [
    2100, 2101, 2102, 2103,  # MaxCoverage
    2200, 2201, 2202, 2203,  # MaxInfluence
]

if __name__ == "__main__":
    l = logger.Analyzer(
        root="MOEA_results_10",
        algorithm_name="MOEA-10",
        algorithm_info="NSGA-II-lite; pop=10; runs=30; budget=1000 00; pc=0.9; pm=1/n; 2nd=min_size"
    )
    for fid in GRAPH_IDS:
        prob = get_problem(fid=fid, problem_class=ProblemClass.GRAPH)
        prob.attach_logger(l)
        run_moea_graph(
            func=prob,
            runs=30,
            budget=100_000,
            pop_size=10,
            pc=0.9, pm=None,
            seed=0,
            exact_k=False,
            k_frac=0.2,
            second="min_size"
        )
    del l
