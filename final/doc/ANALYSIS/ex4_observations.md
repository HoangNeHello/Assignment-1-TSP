# Exercise 4 — Observations & Notes

## Status note (GSEMO)
**GSEMO was *not* executed for Exercise 4.** We explicitly note that *“We cannot run GSEMO since the team only has 3 people who can run the code, check team contribution, so that this particular algo cannot be run in time.”*

## What we ran
- **SOEA-Ex4:** populations 10 / 20 / 50, budget **100,000** fitness evaluations.
- **MOEA-Ex4 (NSGA-II style):** populations 10 / 20 / 50, budget **100,000** fitness evaluations.
- Plots available under `PLOTS/Ex4_plots/…` show fixed-budget trajectories at **100k**, and `PLOTS/Ex3_plots/…` show the earlier **10k** baselines for comparison.

## High-level observations (100k vs 10k)
1) **Across-the-board improvement at 100k.**  
   Fixed-budget curves at 100k consistently sit above (or dominate) their 10k counterparts—indicating better final quality (and, for MOEA, higher diversity/hypervolume).

2) **Diminishing returns after the mid-budget.**  
   Many curves show rapid gains up to ~30k–50k evaluations, then tapering improvements. The extra 50k+ mostly refines the front (MOEA) or nudges single-objective bests (SOEA).

3) **Population size effect is consistent.**  
   - **Pop=50** tends to achieve the **best final quality** and (for MOEA) the **widest Pareto spread**.  
   - **Pop=20** offers a **balanced trade-off**—often close to Pop=50 with fewer evaluations per generation.  
   - **Pop=10** typically converges **fastest early** but can **plateau lower** by 100k.

4) **MOEA vs SOEA behavior.**  
   - **SOEA** (single-objective) often shows **strong early ascent**; at 100k it usually improves absolute best fitness over the 10k baseline but with diminishing returns.  
   - **MOEA** benefits more visibly from extra budget via **better front coverage** and **crowding-based refinement**; at 100k the Pareto set is materially improved compared to 10k (more extreme points retained, fuller knee region).

5) **Ranking stability across budgets.**  
   The relative ordering seen at 10k (e.g., Pop=50 ≥ Pop=20 ≥ Pop=10 in final quality/spread) generally **persists** at 100k, but the **gaps narrow** as budgets increase.

