"""
Implementation of the (1+1) EA Algorithm as defined in the Week 3 Lecture
Modified for Assignment 3
"""
from ioh import get_problem, ProblemClass
from ioh import logger
import sys
import numpy as np

import random

def OnePlusOneEA(func, budget = None):
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

            # Iterate through all bits of sdash
            for k in range(len(sdash)):

                # random() creates a float 0.0 <= x < 1.0
                # Checks if this value is less than 1/len(sdash)
                # Results in the bitflip only happening with a probability of 1/len(sdash)
                if (random.random() < 1/len(sdash)):
                    # Performs a bitflip
                    sdash[k] = 1 - sdash[k]
                # print(k)

            f = func(sdash)
            if (f > f_opt):
                f_opt = f
                sdash_opt = sdash
            if (f_opt >= optimum):
                break
        
        func.reset()

    return f_opt, sdash_opt

# Declaration of problems to be tested.
maxCov2100 = get_problem(fid = 2100, problem_class = ProblemClass.GRAPH)
maxCov2101 = get_problem(fid = 2101, problem_class = ProblemClass.GRAPH)
maxCov2102 = get_problem(fid = 2102, problem_class = ProblemClass.GRAPH)
maxCov2103 = get_problem(fid = 2103, problem_class = ProblemClass.GRAPH)

maxInf2200 = get_problem(fid = 2200, problem_class = ProblemClass.GRAPH)
maxInf2201 = get_problem(fid = 2201, problem_class = ProblemClass.GRAPH)
maxInf2202 = get_problem(fid = 2202, problem_class = ProblemClass.GRAPH)
maxInf2203 = get_problem(fid = 2203, problem_class = ProblemClass.GRAPH)

pwc2300 = get_problem(fid = 2300, problem_class = ProblemClass.GRAPH)
pwc2301 = get_problem(fid = 2301, problem_class = ProblemClass.GRAPH)
pwc2302 = get_problem(fid = 2302, problem_class = ProblemClass.GRAPH)

# Create default logger compatible with IOHanalyzer
# `root` indicates where the output files are stored.
# `folder_name` is the name of the folder containing all output. You should compress this folder and upload it to IOHanalyzer
log = logger.Analyzer(root="data", 
    folder_name="EX4_OnePlusOneEA_run", 
    algorithm_name="OnePlusOneEA", 
    algorithm_info="Implementation of the (1+1) EA in Python")


maxCov2100.attach_logger(log)
OnePlusOneEA(maxCov2100, 100000)
maxCov2101.attach_logger(log)
OnePlusOneEA(maxCov2101, 100000)
maxCov2102.attach_logger(log)
OnePlusOneEA(maxCov2102, 100000)
maxCov2103.attach_logger(log)
OnePlusOneEA(maxCov2103, 100000)

maxInf2200.attach_logger(log)
OnePlusOneEA(maxInf2200, 100000)
maxInf2201.attach_logger(log)
OnePlusOneEA(maxInf2201, 100000)
maxInf2202.attach_logger(log)
OnePlusOneEA(maxInf2202, 100000)
maxInf2203.attach_logger(log)
OnePlusOneEA(maxInf2203, 100000)

pwc2300.attach_logger(log)
OnePlusOneEA(pwc2300, 100000)
pwc2301.attach_logger(log)
OnePlusOneEA(pwc2301, 100000)
pwc2302.attach_logger(log)
OnePlusOneEA(pwc2302, 100000)

# This statemenet is necessary in case data is not flushed yet.
del log