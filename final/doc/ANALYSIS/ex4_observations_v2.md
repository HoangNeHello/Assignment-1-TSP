# Exercise 4 — Observations & Notes (Updated)

## Status note (GSEMO)
**GSEMO was *not* executed for Exercise 4.** We explicitly note that *“We cannot run GSEMO since the team only has 3 people who can run the code, check team contribution, so that this particular algo cannot be run in time.”*

## What we ran
- **SOEA-Ex4:** baselines and variants with standard and *New Uniform Crossover*, populations **10 / 20 / 50**, budget **100,000** fitness evaluations.
- **MOEA-Ex4 (NSGA-II style):** populations **10 / 20 / 50**, budget **100,000**.
- **Ex1-style algorithms re-run at 100k for comparison (where present in plots):**
  - **RLS (Randomised Local Search)**
  - **(1+1) EA (OnePlusOne)**

Plots are available under `PLOTS/Ex4_plots/…` (100k) and the earlier baselines under `PLOTS/Ex3_plots/…` (10k).

---

## High-level observations (100k vs 10k, all methods)

1) **All methods benefit from 10k → 100k, but with diminishing returns.**  
   Curves shift upward at 100k, with the largest gains typically before ~30k–50k evaluations.

2) **Population effects (SOEA & MOEA).**  
   - **Pop=50** delivers the best late-budget quality and (for MOEA) the broadest Pareto spread.  
   - **Pop=20** is a strong compromise—close to Pop=50 but cheaper per generation.  
   - **Pop=10** starts fast but often plateaus lower by 100k.

3) **MOEA benefits more from extra budget.**  
   At 100k the Pareto front is clearly denser (better knee and extremes) than at 10k.

---

## Method-specific notes

### RLS (Randomised Local Search)
- **Behaviour:** Very **steady, local** improvement; excellent **early stability** and **low-variance** progress.  
- **10k → 100k:** Continues to make gains but often **plateaus** once local maxima are reached; extra evaluations yield **smaller increments** than population-based methods that can jump basins.  
- **When to use:** As a **fast, reliable baseline** or when objective calls are very expensive and local moves are preferred.

### (1+1) EA (OnePlusOne)
- **Behaviour:** Similar to RLS but with a flexible **bit-flip mutation rate (1/n)** enabling **larger occasional jumps**.  
- **10k → 100k:** Shows **more late-budget improvement** than RLS on problems where escaping local traps matters; still below the very best SOEA/MOEA late-budget quality in most graphs.  
- **When to use:** As a **simple yet robust** baseline; good for ablation or sanity checks.

### SOEA — *New Uniform Crossover* variant
- **Behaviour:** The new uniform crossover mixes parents more aggressively than 1-point/2-point and pairs well with bit-flip mutation.  
- **10k → 100k:** Gains are **visible**: better **diversity early** and **higher final quality** on most instances vs. the older operator, thanks to better exploration.  
- **Population impact:** Benefits from **Pop=20/50**—more material for recombination and better coverage at 100k.

### MOEA (NSGA-II style)
- **Behaviour:** Rank + crowding selection steadily **fills the front**; boundary points are preserved by ∞ crowding.  
- **10k → 100k:** The **Pareto set quality and spread** improve substantially; knee region becomes clearer and extremes are retained more consistently.  
- **Population impact:** **Pop=50** > **Pop=20** > **Pop=10** in final spread/quality, with reduced variance at higher pops.

---

## Practical takeaways
- For **single-objective** reporting at 100k: prefer **SOEA with New Uniform Crossover, Pop=50** for best late-budget quality; **Pop=20** if runtime is tight.  
- For **multi-objective** reporting: **MOEA Pop=50 @ 100k** gives the strongest fronts.  
- Keep **RLS** and **(1+1)EA** as **reference baselines** to quantify gains.  
- Use **identical seeds/params** when comparing 10k vs 100k to isolate budget effects.

---

## Known limitation (explicit again)
- **GSEMO for Ex4 was not run** due to team capacity/time constraints. Include this in the README/report as a transparent limitation.

