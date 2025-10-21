"""
Implementation of the RLS Algorithm as defined in the Week 3 Lecture
Reimplementation of RLS.py based on OnePlusOneEA.py
"""
from ioh import get_problem, ProblemClass
from ioh import logger
import ioh
import sys
import numpy as np
import random

def RLS(func, budget = None):
    # budget for each run (number of iterations) = 100,000
    # set a default if budget isn't given, in this case 50n^2 (same as random_search function)
    if budget is None:
        budget = int(func.meta_data.n_variables * func.meta_data.n_variables * 50)

    if func.meta_data.problem_id == 18 and func.meta_data.n_variables == 32:
        optimum = 8
    else:
        optimum = func.optimum.y
    print(optimum)

    # Run 30 independant trials of the algorithm
    f_opt = None
    sdash_opt = None
    for i in range(30):
        f_opt = sys.float_info.min
        sdash_opt = None

        # Run algorithm for a number of iterations given by budget
        for j in range(budget):

            # Get current problem value
            sdash = func.state.current_best.x

            # Randomly select one bit
            rand = random.randrange(len(sdash))
            # Flip selected bit
            sdash[rand] = 1 - sdash[rand]

            f = func(sdash)
            if (f > f_opt):
                f_opt = f
                sdash_opt = sdash
            if (f_opt >= optimum):
                break
        
        func.reset()

    return f_opt, sdash_opt

# Declaration of problems to be tested.
problem_2100 = ioh.get_problem(2100, problem_class=ioh.ProblemClass.GRAPH)
problem_2101 = ioh.get_problem(2101, problem_class=ioh.ProblemClass.GRAPH)
problem_2102 = ioh.get_problem(2102, problem_class=ioh.ProblemClass.GRAPH)
problem_2103 = ioh.get_problem(2103, problem_class=ioh.ProblemClass.GRAPH)
problem_2200 = ioh.get_problem(2200, problem_class=ioh.ProblemClass.GRAPH)
problem_2201 = ioh.get_problem(2201, problem_class=ioh.ProblemClass.GRAPH)
problem_2202 = ioh.get_problem(2202, problem_class=ioh.ProblemClass.GRAPH)
problem_2203 = ioh.get_problem(2203, problem_class=ioh.ProblemClass.GRAPH)
problem_2300 = ioh.get_problem(2300, problem_class=ioh.ProblemClass.GRAPH)
problem_2301 = ioh.get_problem(2301, problem_class=ioh.ProblemClass.GRAPH)
problem_2302 = ioh.get_problem(2302, problem_class=ioh.ProblemClass.GRAPH)


# Create default logger compatible with IOHanalyzer
# `root` indicates where the output files are stored.
# `folder_name` is the name of the folder containing all output. You should compress this folder and upload it to IOHanalyzer
log = logger.Analyzer(root="data", 
    folder_name="EX1_RLS_run", 
    algorithm_name="RLS", 
    algorithm_info="Implementation of the RLS algorithm in Python")


problem_2100.attach_logger(log)
RLS(problem_2100, 10000)

problem_2101.attach_logger(log)
RLS(problem_2101, 10000)

problem_2102.attach_logger(log)
RLS(problem_2102, 10000)

problem_2103.attach_logger(log)
RLS(problem_2103, 10000)

problem_2200.attach_logger(log)
RLS(problem_2200, 10000)

problem_2201.attach_logger(log)
RLS(problem_2201, 10000)

problem_2202.attach_logger(log)
RLS(problem_2202, 10000)

problem_2203.attach_logger(log)
RLS(problem_2203, 10000)

problem_2300.attach_logger(log)
RLS(problem_2300, 10000)

problem_2301.attach_logger(log)
RLS(problem_2301, 10000)

problem_2302.attach_logger(log)
RLS(problem_2302, 10000)

# This statemenet is necessary in case data is not flushed yet.
del log
