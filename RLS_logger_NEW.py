"""
Implementation of the RLS Algorithm as defined in the Week 3 Lecture
Reimplementation of RLS.py based on OnePlusOneEA.py
Modified for Assignment 3
"""
# from ioh import get_problem, ProblemClass
# from ioh import logger
# import sys
# import numpy as np

# import random

# def RLS(func, budget = None):
#     # budget for each run (number of iterations) = 100,000
#     # set a default if budget isn't given, in this case 50n^2 (same as random_search function)
#     if budget is None:
#         budget = int(func.meta_data.n_variables * func.meta_data.n_variables * 50)

#     if func.meta_data.problem_id == 18 and func.meta_data.n_variables == 32:
#         optimum = 8
#     else:
#         optimum = func.optimum.y
#     print(optimum)

#     # Run 10 independant trials of the algorithm
#     f_opt = None
#     sdash_opt = None
#     for i in range(30):
#         f_opt = sys.float_info.min
#         sdash_opt = None

#         # Run algorithm for a number of iterations given by budget
#         for j in range(budget):

#             # Get current problem value
#             sdash = func.state.current_best.x

#             # Randomly select one bit
#             rand = random.randrange(len(sdash))
#             # Flip selected bit
#             sdash[rand] = 1 - sdash[rand]

#             f = func(sdash)
#             if (f > f_opt):
#                 f_opt = f
#                 sdash_opt = sdash
#             if (f_opt >= optimum):
#                 break
        
#         func.reset()

#     return f_opt, sdash_opt

# # Declaration of problems to be tested.
# om = get_problem(fid = 1, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# lo = get_problem(fid = 2, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# prob3 = get_problem(fid = 3, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# labs = get_problem(fid = 18, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# prob23 = get_problem(fid = 23, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# prob24 = get_problem(fid = 24, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# prob25 = get_problem(fid = 25, dimension=100, instance=1, problem_class = ProblemClass.PBO)

# # Create default logger compatible with IOHanalyzer
# # `root` indicates where the output files are stored.
# # `folder_name` is the name of the folder containing all output. You should compress this folder and upload it to IOHanalyzer
# log = logger.Analyzer(root="data", 
#     folder_name="RLS_run", 
#     algorithm_name="RLS", 
#     algorithm_info="Implementation of the RLS algorithm in Python")


# om.attach_logger(log)
# RLS(om, 100000)

# lo.attach_logger(log)
# RLS(lo, 100000)

# prob3.attach_logger(log)
# RLS(prob3, 100000)

# labs.attach_logger(log)
# RLS(labs, 100000)

# prob23.attach_logger(log)
# RLS(prob23, 100000)

# prob24.attach_logger(log)
# RLS(prob24, 100000)

# prob25.attach_logger(log)
# RLS(prob25, 100000)

# # This statemenet is necessary in case data is not flushed yet.
# del log