# mmas_star.py
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Callable, List, Tuple

Bitstring = List[int]
EvalFn = Callable[[Bitstring], int]

@dataclass
class MMASStarConfig:
    n: int = 100
    num_ants: int = 10
    rho: float = 0.02
    p_min: float = None
    p_max: float = None
    seed: int | None = None

class MMASStar:
    def __init__(self, cfg: MMASStarConfig):
        self.cfg = cfg
        self.rng = random.Random(cfg.seed)
        self.p = [0.5] * cfg.n
        self.p_min = cfg.p_min if cfg.p_min is not None else 1.0 / cfg.n
        self.p_max = cfg.p_max if cfg.p_max is not None else 1.0 - 1.0 / cfg.n

    def _sample(self) -> Bitstring:
        return [1 if self.rng.random() < pi else 0 for pi in self.p]

    def _update_best_so_far(self, best: Bitstring):
        n, rho = self.cfg.n, self.cfg.rho
        for i in range(n):
            target = 1.0 if best[i] == 1 else 0.0
            self.p[i] = (1 - rho) * self.p[i] + rho * target
            if self.p[i] < self.p_min: self.p[i] = self.p_min
            if self.p[i] > self.p_max: self.p[i] = self.p_max

    def run(self, eval_budget: int, f: EvalFn) -> Tuple[float, list[float]]:
        evals = 0
        best_f = float("-inf")
        best_x = None
        best_curve = []

        # Initial sampling
        remain = min(self.cfg.num_ants, eval_budget)
        batch = [self._sample() for _ in range(remain)]
        vals = [f(x) for x in batch]
        evals += remain
        local_best_idx = max(range(len(batch)), key=lambda k: vals[k])
        best_f = vals[local_best_idx]
        best_x = batch[local_best_idx][:]
        best_curve.append(best_f)

        # Main loop
        while evals < eval_budget:
            batch = [self._sample() for _ in range(self.cfg.num_ants)]
            vals = [f(x) for x in batch]
            evals += len(batch)

            local_best_idx = max(range(len(batch)), key=lambda k: vals[k])
            if vals[local_best_idx] > best_f:
                best_f = vals[local_best_idx]
                best_x = batch[local_best_idx][:]
            self._update_best_so_far(best_x)
            best_curve.append(best_f)

        return best_f, best_curve

