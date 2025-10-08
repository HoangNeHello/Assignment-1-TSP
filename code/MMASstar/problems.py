# problems.py
from typing import List, Tuple, Callable

def onemax(x): return sum(x)

def leading_ones(x):
    s = 0
    for b in x:
        if b == 1: s += 1
        else: break
    return s

def get_benchmarks():
    benches = []
    for n in [100, 200]:
        budget = 20000
        benches += [
            (f"OneMax-{n}", n, budget, onemax),
            (f"LeadingOnes-{n}", n, budget, leading_ones),
        ]
    return benches
