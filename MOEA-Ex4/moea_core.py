# moea_core.py
from __future__ import annotations
from typing import List, Tuple
import numpy as np

def run_moea_graph(
    func,
    runs: int = 30,
    budget: int = 100_000,
    pop_size: int = 20,
    pc: float = 0.9,
    pm: float | None = None,
    seed: int = 0,
    exact_k: bool = False,
    k_frac: float = 0.2,
    second: str = "min_size",
):

    rng = np.random.default_rng(seed)
    n = func.meta_data.n_variables
    if pm is None:
        pm = 1.0 / n
    k = max(1, int(round(k_frac * n)))

    def objectives(x: np.ndarray) -> Tuple[float, int]:
        f1 = float(func(x))
        s  = int(x.sum())
        f2 = -s if second == "min_size" else s
        return (f1, f2)

    def init_ind() -> np.ndarray:
        if exact_k:
            x = np.zeros(n, dtype=np.int32)
            idx = rng.choice(n, size=k, replace=False)
            x[idx] = 1
            return x
        return rng.integers(0, 2, size=n, dtype=np.int32)

    def cx_uniform(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        mask = rng.random(n) < 0.5
        c = np.where(mask, a, b)
        if exact_k:
            ones = c.sum()
            if ones > k:
                pos = np.flatnonzero(c)
                flip = rng.choice(pos, size=(ones - k), replace=False)
                c[flip] = 0
            elif ones < k:
                pos = np.flatnonzero(1 - c)
                flip = rng.choice(pos, size=(k - ones), replace=False)
                c[flip] = 1
        return c.astype(np.int32)

    def mutate(x: np.ndarray) -> np.ndarray:
        y = x.copy()
        if exact_k:
            ones  = np.flatnonzero(y)
            zeros = np.flatnonzero(1 - y)
            if ones.size and zeros.size:
                i = rng.choice(ones); j = rng.choice(zeros)
                y[i] = 0; y[j] = 1
            return y
        flips = rng.random(n) < pm
        if not flips.any():
            flips[rng.integers(n)] = True
        y[flips] ^= 1
        return y

    def fast_nondom_sort(F: List[Tuple[Tuple[float, int], np.ndarray]]):
        S = [[] for _ in range(len(F))]
        n_dom = [0] * len(F)
        fronts = [[]]

        def dominates(a, b):
            return (a[0] >= b[0] and a[1] >= b[1]) and (a[0] > b[0] or a[1] > b[1])

        for p in range(len(F)):
            for q in range(len(F)):
                if p == q: continue
                if dominates(F[p][0], F[q][0]):
                    S[p].append(q)
                elif dominates(F[q][0], F[p][0]):
                    n_dom[p] += 1
            if n_dom[p] == 0:
                fronts[0].append(p)

        i = 0
        while fronts[i]:
            Q = []
            for p in fronts[i]:
                for q in S[p]:
                    n_dom[q] -= 1
                    if n_dom[q] == 0:
                        Q.append(q)
            i += 1
            fronts.append(Q)
        fronts.pop()
        return fronts

    def crowding_distance(front: List[int], fit_list: List[Tuple[float,int]]):
        m = len(front)
        dist = np.zeros(m, dtype=float)
        if m == 0:
            return dist
        for obj in [0, 1]:
            idx = sorted(range(m), key=lambda i: fit_list[front[i]][obj])
            dist[idx[0]]  = float("inf")
            dist[idx[-1]] = float("inf")
            vals = [fit_list[front[i]][obj] for i in idx]
            vmin, vmax = vals[0], vals[-1]
            if vmax == vmin:
                continue
            for t in range(1, m - 1):
                dist[idx[t]] += (vals[t+1] - vals[t-1]) / (vmax - vmin)
        return dist

    for _ in range(runs):
        evals = 0

        pop = [init_ind() for _ in range(pop_size)]
        fits = []
        for x in pop:
            fits.append(objectives(x)); evals += 1
            if evals >= budget: break

        while evals < budget:
            off = []
            for _g in range(pop_size):
                F = list(zip(fits, pop))
                fronts = fast_nondom_sort(F)
                rank = {idx: r for r, fr in enumerate(fronts) for idx in fr}
                def pick_one():
                    a, b = rng.integers(len(pop)), rng.integers(len(pop))
                    ra, rb = rank[a], rank[b]
                    if ra < rb: return pop[a]
                    if rb < ra: return pop[b]
                    fr = fronts[ra]
                    cd = crowding_distance(fr, [f for f,_ in F])
                    ia, ib = fr.index(a), fr.index(b)
                    return pop[a] if cd[ia] >= cd[ib] else pop[b]

                p1 = pick_one()
                if rng.random() < pc:
                    p2 = pick_one()
                    child = cx_uniform(p1, p2)
                else:
                    child = p1.copy()
                child = mutate(child)
                off.append(child)

            off_fit = []
            for y in off:
                off_fit.append(objectives(y)); evals += 1
                if evals >= budget: break

            merged = list(zip(fits, pop)) + list(zip(off_fit, off))
            fronts = fast_nondom_sort(merged)

            new_pop, new_fits = [], []
            for fr in fronts:
                if len(new_pop) + len(fr) <= pop_size:
                    for idx in fr:
                        new_fits.append(merged[idx][0])
                        new_pop.append(merged[idx][1])
                else:
                    cd = crowding_distance(fr, [f for f,_ in merged])
                    order = sorted(range(len(fr)), key=lambda i: cd[i], reverse=True)
                    need = pop_size - len(new_pop)
                    for i in order[:need]:
                        idx = fr[i]
                        new_fits.append(merged[idx][0])
                        new_pop.append(merged[idx][1])
                    break
            pop, fits = new_pop, new_fits

        func.reset()
