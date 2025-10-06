# problems.py
import math
from typing import List, Tuple, Callable

Bitstring = List[int]
EvalFn = Callable[[Bitstring], int]

def onemax(x: Bitstring) -> int:
    return sum(x)

def leading_ones(x: Bitstring) -> int:
    c = 0
    for v in x:
        if v == 1:
            c += 1
        else:
            break
    return c

def get_benchmarks():

    benches = []
    for n in [50, 100, 200]:
        budget = 10000
        benches.append((f"OneMax", n, budget, onemax))
        benches.append((f"LeadingOnes", n, budget, leading_ones))
    return benches
