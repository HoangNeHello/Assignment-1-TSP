# problem_example.py
from ioh import get_problem, ProblemClass, logger
import sys
import numpy as np

# Provided Random Search
def random_search(func, budget=None):
    # budget per run = 50 * n^2
    if budget is None:
        n = func.meta_data.n_variables
        budget = int(50 * n * n)

    # known optimum
    if func.meta_data.problem_id == 18 and func.meta_data.n_variables == 32:
        optimum = 8
    else:
        optimum = func.optimum.y

    # 10 independent runs
    for _ in range(10):
        f_opt = -sys.float_info.max
        for _ in range(budget):
            x = np.random.randint(2, size=func.meta_data.n_variables)
            f = func(x)              # IOH logs each evaluation
            if f > f_opt:
                f_opt = f
            if f_opt >= optimum:     # early stop
                break
        func.reset()

    return

# Problems to test (template uses n=50)
om   = get_problem(fid=1,  dimension=50, instance=1, problem_class=ProblemClass.PBO)
lo   = get_problem(fid=2,  dimension=50, instance=1, problem_class=ProblemClass.PBO)
labs = get_problem(fid=18, dimension=50, instance=1, problem_class=ProblemClass.PBO)

# Logger (IOHprofiler format)
l = logger.Analyzer(
    root="data",                 # base folder (will be created)
    folder_name="run",           # subfolder to zip and upload
    algorithm_name="RandomSearch",
    algorithm_info="provided template"
)

# Attach, run, detach
om.attach_logger(l);   random_search(om)
lo.attach_logger(l);   random_search(lo)
labs.attach_logger(l); random_search(labs)

# Flush files
del l
