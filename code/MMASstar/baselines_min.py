# baselines_min.py
import random
from typing import Callable, List, Tuple
Bitstring = List[int]; EvalFn = Callable[[Bitstring], int]

def rand_x(n, rng): return [rng.randint(0,1) for _ in range(n)]
def flip_one(x, i): y=x[:]; y[i]^=1; return y
def flip_each_with_prob(x, rng, p):
    y=x[:]
    for i in range(len(x)):
        if rng.random() < p: y[i]^=1
    return y

def rls(n: int, f: EvalFn, budget: int, seed: int) -> Tuple[int, list[int]]:
    rng = random.Random(seed)
    x = rand_x(n, rng); fx = f(x); best_curve=[fx]; evals=1
    while evals < budget:
        i = rng.randrange(n)
        y = flip_one(x, i); fy = f(y); evals += 1
        if fy >= fx: x, fx = y, fy
        best_curve.append(fx)
    return fx, best_curve

def one_plus_one_ea(n: int, f: EvalFn, budget: int, seed: int) -> Tuple[int, list[int]]:
    rng = random.Random(seed); p = 1.0/n
    x = rand_x(n, rng); fx = f(x); best_curve=[fx]; evals=1
    while evals < budget:
        y = flip_each_with_prob(x, rng, p); fy = f(y); evals += 1
        if fy >= fx: x, fx = y, fy
        best_curve.append(fx)
    return fx, best_curve
