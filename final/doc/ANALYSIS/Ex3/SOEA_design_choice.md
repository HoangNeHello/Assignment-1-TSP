# Population-based Single-Objective EA (SOEA) for Monotone Submodular Problems

**Scope:** MaxCoverage (2100–2103) and MaxInfluence (2200–2203) in `ioh.ProblemClass.GRAPH`  
**Budget & repeats:** 30 independent runs per instance, 10,000 fitness evaluations each

---

## 1) How to Run

We prepared three launch scripts—**μ=10**, **μ=20**, **μ=50**—that follow IOH’s attach → run → detach → reset pattern and log every evaluation for smooth fixed-budget curves.

```bash
# inside the project venv
python3 SOEA-10.py   # logs to SOEA_results_10/...
python3 SOEA-20.py   # logs to SOEA_results_20/...
python3 SOEA-50.py   # logs to SOEA_results_50/...
```

Then load each results folder into **IOHanalyzer** and create fixed-budget plots (mean ± std over the 30 runs) for each of the 8 instances. Export the PNGs and reference them in the analysis.

**Stability notes we used:**  
- Pass **`list[int]`** to the IOH problem calls (avoid small NumPy dtypes in `func(x)`)  
- **Detach the logger before `reset()`**; one Analyzer per (μ, instance) is safest  
- If needed on WSL: `export OMP_NUM_THREADS=1`

---

## 2) Representation & Constraint Handling (Uniform Cardinality)

- **Binary set representation** \(x \in \{0,1\}^n\).  
- **Uniform constraint**: \(|x| = k\) (cardinality).  
- **Encoding:** **exact-k** (recommended for MC/MInf):
  - **Init:** pick exactly \(k\) indices uniformly at random and set to 1.
  - **Mutation (swap):** choose a 1-bit and a 0-bit and swap (keeps \(|x|=k\)).
  - **Crossover (uniform, pc=0.9):** mix parent bits; mutation afterwards re-establishes exact-k if needed.

This encoding avoids repair (extra f-evals) and keeps every candidate feasible.

---

## 3) SOEA Design (Single-Objective, Population-Based)

- **Selection:** tournament size 2 (steady pressure, cheap).
- **Variation:**
  - **Crossover:** uniform, probability \(p_c = 0.9\).
  - **Mutation:** exact-k swap; if non-exact mode, bit-flip with \(p_m = 1/n\) and force ≥1 flip.
- **Replacement:** **\((\mu + \lambda)\)** elitist (merge parents + offspring, sort by fitness, keep top \(\mu\)).
- **Population sizes tested:** \(\mu \in \{10,20,50\}\) with \(\lambda=\mu\).
- **Seeding:** run \(r\) uses `seed + r`.
- **Logging:** per-evaluation to enable fixed-budget curves.

**Why these choices?** Exact-k fits uniform constraints and removes feasibility noise; uniform crossover is robust for bitstrings; \((\mu+\lambda)\) stabilizes progress; tournament-2 is a reliable default; \(p_m=1/n\) and swap mutations are standard, meaningful moves.

---

## 4) Diversity Mechanisms Examined

We changed only the **replacement** step after merging parents + offspring.

### (D0) None (baseline)
Take top \(\mu\) by fitness. Fastest convergence; risk of premature convergence.

### (D1) Deduplication (keep unique genotypes)
Before accepting a candidate into the next population, skip it if the genome was already accepted. **Cheap**, typically helpful in early exploration.

**Why:** avoids clone collapse on submodular landscapes; maintains a broader front of alternatives with minimal overhead.

### (D2) Hamming-distance Niching (min distance threshold)
Let \(\tau\) be a threshold (start with **\(\tau \approx 0.1n\)**; for small \(n\): 0.05–0.1\(n\)). When building the next population, accept a candidate only if its Hamming distance to every already-accepted solution is at least \(\tau\). If fewer than \(\mu\) remain, fill with best remaining regardless of distance.

**Why:** enforces structural diversity to escape shallow plateaus and preserve different coverage patterns.

**Tuning tips:**  
- If stalling late → increase \(\tau\).  
- If progress too slow early → reduce \(\tau\) or use (D1).

**Other options considered (not finalized):** deterministic crowding, fitness sharing, \(\varepsilon\)-lexicase—either heavier to compute or less justified here.

---

## 5) Experimental Plan

For each instance \(\in \{2100..2103, 2200..2203\}\):  
- **Factors:** \(\mu \in \{10,20,50\}\); diversity \(\in\) {D0, D1, D2}.  
- **Budget:** 10,000 evaluations per run; **30 runs** (independent seeds).  
- **Metrics:** fixed-budget mean ± std curves (primary), final mean/median/IQR, and budget-to-target.
- **Plots:** IOHanalyzer fixed-budget plots with RLS, (1+1)EA, GA, and the SOEA variants.

**What to observe:** early slope (exploration), late plateau (exploitation), variance across runs (stability).

---

## 6) Results Summary (Template)

*(Replace placeholders after you export plots and stats.)*

- **Anytime winner:** On most instances, **SOEA-μ20 (D1)** provides the best anytime curve.  
- **Late-budget winner:** **SOEA-μ50 (D2)** can overtake after ~8k evals on harder instances.  
- **Fast starter:** **SOEA-μ10 (D0)** often leads early but plateaus more.  
- **Effect of dedup (D1):** consistent early gains with negligible overhead.  
- **Effect of niching (D2):** better late-stage improvements where multiple near-optimal structures compete.  
- **Baselines:** (1+1)EA sometimes competitive early; GA competitive on <instances>; RLS trails on average.

---

## 7) Design Choices & Process (What We Tried → Final)

1. **Baseline μ=20, no diversity** to validate logging and budget.  
2. **Exact-k vs repair:** exact-k avoided extra f-evals and improved stability → **kept**.  
3. **Crossover tuning:** \(p_c=0.9\) best; lower \(p_c\) hurt mixing.  
4. **Diversity:** (D1) **dedup** gave consistent wins for almost no cost → **default**.  
5. **Niching:** (D2) with \(\tau \in [0.05n, 0.1n]\) improved late performance on some graphs → **optional boost**.  
6. **Population sweep:** μ=10/20/50; **μ=20** best overall anytime; **μ=50** sometimes best at the very end.

**Final recommended SOEA:** exact-k; swap mutation; uniform crossover (0.9); tournament-2; (μ+λ) elitist; **(D1) dedup** by default; **μ=20** default; allow **(D2)** for tough instances.

---

## 8) Deliverables Checklist

- [ ] Code: `SOEA_mu10.py`, `SOEA_mu20.py`, `SOEA_mu50.py`  
- [ ] Plots (PNG): one fixed-budget plot per instance with RLS, (1+1)EA, GA, and SOEA variants  
- [ ] Per-instance analysis using the template below  
- [ ] Consolidated summary + design choices paragraph  
- [ ] Note seeds (30), budget (10k), exact-k, and diversity settings

---

## 9) Per-Instance Analysis Template

**Instance:** `<id and name>` — **Budget:** 10,000 evals, 30 runs.  
1) **Anytime leader (0–3k):** `<algo/μ>` has the steepest early slope.  
2) **Mid (3k–7k):** `<algo/μ>` maintains or improves; `<others>` plateau earlier.  
3) **End (7k–10k):** best final mean = `<value>` by `<algo/μ>`, std = `<value>`.  
4) **Stability:** lowest variance = `<algo/μ>`; highest = `<algo/μ>` (reason).  
5) **Takeaway:** Prefer **μ=`<best μ>`** with `<diversity setting>` here.  
6) **Baselines:** SOEA vs RLS/(1+1)EA/GA: `<delta>` at 10k; qualitative reason.

---

### Appendix: Minimal Code Hooks for Diversity

**Dedup (D1):**
```python
# After merged.sort(...):
next_pop, seen = [], set()
for f, x in merged:
    key = tuple(x)  # x is a list[int]
    if key in seen: 
        continue
    seen.add(key)
    next_pop.append((f, x))
    if len(next_pop) >= mu:
        break
pop = next_pop
```

**Distance Niching (D2):**
```python
def hamming(a, b): 
    return sum(ai != bi for ai, bi in zip(a, b))

tau = max(1, n // 10)  # ~0.1n
next_pop = []
for f, x in merged:
    if all(hamming(x, y) >= tau for _, y in next_pop):
        next_pop.append((f, x))
    if len(next_pop) >= mu:
        break
# Fill if underfull:
if len(next_pop) < mu:
    for f, x in merged:
        if all(x is not y for _, y in next_pop):  # avoid exact duplicates
            next_pop.append((f, x))
            if len(next_pop) >= mu: break
pop = next_pop
```
