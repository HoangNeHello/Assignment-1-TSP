# `moea_core.py` — Design Choices & Rationale

This module implements a compact NSGA‑II–style multi‑objective evolutionary algorithm (MOEA) tailored for **binary vectors** and **submodular/graph** problems. Below I explain each design choice and its trade‑offs from my point of view, aligned with your Exercise 4 usage (100,000 evaluations).

---

## 1) Problem interface & objectives

```python
n = func.meta_data.n_variables
def objectives(x) -> (float, int):
    f1 = float(func(x))
    s  = int(x.sum())
    f2 = -s if second == "min_size" else s
    return (f1, f2)
```
**Why:**  
- The code assumes a *callable problem* `func` with a metadata field for dimension.  
- **Primary objective `f1`** is delegated to `func(x)` (e.g., submodular gain).  
- **Secondary objective `f2`** converts a *cardinality preference* into an objective:  
  - `min_size`: minimize selections via `f2 = -|x|` (so fewer ones is “better”).  
  - Otherwise: maximize size via `f2 = |x|`.  
- Using a simple integer for the second objective makes sorting and crowding numerically stable and fast.

**Trade‑offs:**  
- Two objectives are hard‑coded; extending to >2 would require updating sorting and crowding loops.  
- Cardinality as an objective is a coarse constraint proxy; exact cardinality is handled separately (see §3).

---

## 2) Initialization

```python
def init_ind():
    if exact_k:
        x = zeros(n); set exactly k ones uniformly at random
    else:
        x ~ Ber(0.5)^n
```
**Why:**  
- For unconstrained runs, uniform Bernoulli gives diverse starts.  
- For **exact‑k** problems, we *enforce feasibility at initialization*, avoiding wasted evaluations on infeasible individuals.

**Trade‑offs:**  
- Bernoulli(0.5) is generic; a domain‑informed prior could speed up convergence.  
- Exact‑k random init is unbiased w.r.t. positions but ignores problem structure.

---

## 3) Variation operators (crossover & mutation)

### Uniform crossover
```python
c = where(mask, a, b)
if exact_k:
    # repair to keep exactly k ones
```
**Why:**  
- **Uniform** works well for unstructured binary encodings and mixes information aggressively.  
- Under **exact‑k**, post‑crossover **repair** maintains feasibility without discarding offspring.

### Mutation
- **Exact‑k**: single **swap** (1→0 and 0→1).  
- Otherwise: standard **bit‑flip** with rate `pm = 1/n` (default). Ensures at least one flip.

**Trade‑offs:**  
- Swap‑mutation preserves Hamming weight, ideal for cardinality constraints.  
- Uniform crossover can disrupt building blocks; 1‑point/2‑point could be better for positional linkage—left out for simplicity.  
- Enforcing at least one flip avoids stagnation when `pm` is small and `rng.random(n)` happens to produce no flips.

---

## 4) Selection & survival — NSGA‑II mechanics

### Fast non‑dominated sorting
```python
def dominates(a,b):
    return (a[0] >= b[0] and a[1] >= b[1]) and (a[0] > b[0] or a[1] > b[1])
```
- Classic Pareto dominance to obtain **fronts F₁, F₂, …**.  
- Complexity is **O(M·N²)** with `M=2` objectives; acceptable for modest population sizes (10–50).

### Crowding distance
- Computed per front, per objective, with ∞ at extremes to preserve boundary points.  
- Normalization by `(vmax−vmin)` reduces scale sensitivity.

### Parent selection
- **Binary tournament** by **rank** then **crowding** (NSGA‑II).  
- Simple and efficient; biases toward better fronts while retaining diversity within a front.

### Environmental selection
- Merge parents+offspring → sort fronts → fill next population; tie‑break with crowding.  
- Guarantees elitism (best fronts survive).

**Trade‑offs & implications:**  
- Deterministic nondominated sorting + stochastic tournaments give a good accuracy/diversity balance.  
- For very large populations, you might switch to incremental dominance structures; unnecessary here.

---

## 5) Budget management & runs

```python
runs, budget, pop_size, pc, pm, seed
```
- **Budget** counts **objective evaluations**, the expensive step. All loops stop when `evals >= budget`.  
- `runs` allows outer replication (30 by default) for statistical robustness.  
- A **fixed RNG** (`np.random.default_rng(seed)`) ensures reproducibility per run.

**Design detail:** evaluations include both initial population and offspring—this is explicit and avoids accidental budget overruns.

---

## 6) Constraint handling: exact‑k

- Enforced at **init**, **crossover repair**, and **swap‑mutation**.  
- Prevents infeasible offspring and keeps search in the feasible manifold (Hamming sphere).

**Why not penalty functions?**  
- Penalties add tuning knobs and distort Pareto ranking. Exact feasibility is clean and parameter‑free.

---

## 7) Parameters & defaults

- `pc = 0.9` (high crossover) — common for binary EAs with mutation providing local search.  
- `pm = 1/n` if None — textbook choice for bit‑flip mutation.  
- `pop_size` ∈ {10, 20, 50} in your Ex4 variants — adequate for NSGA‑II’s O(N²) sorting.  
- `k_frac = 0.2` — reasonable default if exact‑k is used without a specified `k`.

**Tuning guidance for Ex4 (100,000 evals):**  
- For **noisy/flat** landscapes, consider a slightly **larger pop** (20→50) to improve spread.  
- For **tight budgets**, ensure `pm` isn’t too low; the “force‑one‑flip” safeguard already helps.

---

## 8) Complexity & performance notes

- Per generation: nondominated sort **O(N²)** with small constants (M=2).  
- Crowding distance is **O(N log N)** per front due to sorting.  
- Overall, with `N ≤ 50`, the algorithm remains fast relative to objective cost.

---

## 9) Robustness & edge cases

- **Degenerate front** (all identical objective values): crowding becomes ∞ at endpoints and 0 inside—selection remains stable.  
- **Exact‑k with k=0 or k=n**: guarded by `k = max(1, round(k_frac*n))`; if truly needed, allow k∈{0,n} explicitly.  
- **No flips at mutation**: forced single flip avoids stalled offspring.

---

## 10) Extensibility

- **More objectives**: generalize dominance & crowding loops to M objectives.  
- **Alternate secondary objective**: plug another structural prior (e.g., number of components, cost).  
- **Different variation**: add 1‑point crossover or problem‑aware operators (e.g., swap within adjacency lists).  
- **Archiving**: add an external archive for high‑resolution Pareto sets if needed for reporting.

---

## 11) Scope note (team)
> We cannot run **GSEMO** since the team only has 3 people who can run the code, check team contribution, so that this particular algo cannot be run in time.

This file focuses purely on the NSGA‑II‑style MOEA in `moea_core.py`.

---

## 12) Recommended defaults for Exercise 4

- **Budget:** 100,000 evaluations per configuration.  
- **Replications:** 30 (if time permits).  
- **Populations:** 10, 20, 50 (compare spread/quality).  
- **Crossover/Mutation:** `pc=0.9`, `pm=1/n` (or swap under exact‑k).  
- **Secondary objective:** `"min_size"` when sparsity is desired; otherwise use `"max_size"`.

---

### TL;DR
A minimal, readable **NSGA‑II** for binary vectors: exact‑k feasibility baked into variation; two objectives (value and size) with standard nondominated sorting and crowding; strict evaluation budgeting; and small‑N efficiency—ideal for your Ex4 100k‑eval runs.
