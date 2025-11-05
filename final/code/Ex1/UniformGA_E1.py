from ioh import get_problem, ProblemClass
from ioh import logger
import ioh
import numpy as np
import random


def _tournament_select(pop, fits, k, maximize=True, rng=None):
    if rng is None:
        rng = random
    idxs = rng.sample(range(len(pop)), min(k, len(pop)))
    best = idxs[0]
    for i in idxs[1:]:
        if (maximize and fits[i] > fits[best]) or ((not maximize) and fits[i] < fits[best]):
            best = i
    return pop[best]


def _uniform_crossover(p1, p2, rng=None):
    if rng is None:
        rng = random
    n = len(p1)
    child = p1.copy()
    for i in range(n):
        if rng.random() >= 0.5:
            child[i] = p2[i]
    return child


def _bitflip_mutation(x, pm, rng=None):
    if rng is None:
        rng = random
    n = len(x)
    y = x.copy()
    for i in range(n):
        if rng.random() < pm:
            y[i] = 1 - y[i]
    return y


def UniformCrossoverGA(func, budget=None, mu=20, lambd=20, pc=0.9, tournament_k=3, runs=30, seed=None):
    rng = random.Random(seed)

    n = func.meta_data.n_variables
    if budget is None:
        budget = int(50 * n * n)

    try:
        optimum = func.optimum.y
    except Exception:
        optimum = None

    for run in range(runs):
        pop = np.random.randint(0, 2, size=(mu, n), dtype=int).tolist()
        fits = [func(ind.copy()) for ind in pop]
        evals = len(fits)

        best_idx = int(np.argmax(fits))
        best_f = fits[best_idx]
        best_x = pop[best_idx].copy()

        pm = 1.0 / n

        while evals < budget:
            off = []
            off_f = []
            for _ in range(lambd):
                p1 = _tournament_select(pop, fits, tournament_k, maximize=True, rng=rng)
                p2 = _tournament_select(pop, fits, tournament_k, maximize=True, rng=rng)

                child = p1.copy()
                if rng.random() < pc:
                    child = _uniform_crossover(p1, p2, rng=rng)
                child = _bitflip_mutation(child, pm, rng=rng)

                f = func(child.copy())
                evals += 1
                off.append(child)
                off_f.append(f)

                if optimum is not None and f >= optimum:
                    best_x = child.copy()
                    best_f = f
                    break

            if off_f:
                idx = int(np.argmax(off_f))
                if off_f[idx] > best_f:
                    best_f = off_f[idx]
                    best_x = off[idx].copy()

                merged = pop + off
                merged_f = fits + off_f
                order = sorted(range(len(merged)), key=lambda i: merged_f[i], reverse=True)
                pop = [merged[i] for i in order[:mu]]
                fits = [merged_f[i] for i in order[:mu]]

            if optimum is not None and best_f >= optimum:
                break

        func.reset()


maxCov2100 = get_problem(fid=2100, problem_class=ProblemClass.GRAPH)
maxCov2101 = get_problem(fid=2101, problem_class=ProblemClass.GRAPH)
maxCov2102 = get_problem(fid=2102, problem_class=ProblemClass.GRAPH)
maxCov2103 = get_problem(fid=2103, problem_class=ProblemClass.GRAPH)

maxInf2200 = get_problem(fid=2200, problem_class=ProblemClass.GRAPH)
maxInf2201 = get_problem(fid=2201, problem_class=ProblemClass.GRAPH)
maxInf2202 = get_problem(fid=2202, problem_class=ProblemClass.GRAPH)
maxInf2203 = get_problem(fid=2203, problem_class=ProblemClass.GRAPH)

pwc2300 = get_problem(fid=2300, problem_class=ProblemClass.GRAPH)
pwc2301 = get_problem(fid=2301, problem_class=ProblemClass.GRAPH)
pwc2302 = get_problem(fid=2302, problem_class=ProblemClass.GRAPH)


log = logger.Analyzer(
    root="data",
    folder_name="EX1_UniformGA_run",
    algorithm_name="UniformGA",
    algorithm_info="Uniform crossover GA (mu+lambda), pc=0.9, pm=1/n, tournament selection"
)

maxCov2100.attach_logger(log)
UniformCrossoverGA(maxCov2100, 10000)
maxCov2101.attach_logger(log)
UniformCrossoverGA(maxCov2101, 10000)
maxCov2102.attach_logger(log)
UniformCrossoverGA(maxCov2102, 10000)
maxCov2103.attach_logger(log)
UniformCrossoverGA(maxCov2103, 10000)

maxInf2200.attach_logger(log)
UniformCrossoverGA(maxInf2200, 10000)
maxInf2201.attach_logger(log)
UniformCrossoverGA(maxInf2201, 10000)
maxInf2202.attach_logger(log)
UniformCrossoverGA(maxInf2202, 10000)
maxInf2203.attach_logger(log)
UniformCrossoverGA(maxInf2203, 10000)

pwc2300.attach_logger(log)
UniformCrossoverGA(pwc2300, 10000)
pwc2301.attach_logger(log)
UniformCrossoverGA(pwc2301, 10000)
pwc2302.attach_logger(log)
UniformCrossoverGA(pwc2302, 10000)

del log
