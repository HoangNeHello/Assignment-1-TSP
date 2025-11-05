# Exercise 4 — Observations & Notes (Corrected)

## Status note (GSEMO)
**GSEMO was *not* executed for Exercise 4.** We explicitly note that *“We cannot run GSEMO since the team only has 3 people who can run the code, check team contribution, so that this particular algo cannot be run in time.”*

## Algorithm roster for Ex4 (100,000 evaluations)
- **RLS (Randomised Local Search)** — baseline local-improvement algorithm.
- **(1+1) EA (OnePlusOne)** — single-parent EA with bit-flip mutation (1/n).
- **SOEA (baseline GA)** — single-objective GA with the *existing* crossover used in your prior exercises.
- **UniformGA (NEW, independent GA)** — *standalone* GA that uses the **New Uniform Crossover** operator.  
  *Note: This is **not** integrated into SOEA. It is a separate algorithm and should be reported independently.*
- **MOEA (NSGA-II style)** — 2-objective Pareto optimisation.

## High-level observations (100k vs 10k)
1) **All methods improve from 10k → 100k**, with the largest gains before ~30k–50k evaluations and **diminishing returns** afterwards.
2) **Population effects (for GA-typed methods):** Pop=50 generally attains the best 100k performance; Pop=20 is a strong compromise; Pop=10 starts fast but plateaus earlier.
3) **MOEA gains more from extra budget** (denser fronts, better extremes/knee) than single-objective methods.
4) **UniformGA vs SOEA (both single-objective):**  
   - **UniformGA** tends to show **better exploration early** (due to the new uniform operator’s mixing) and **higher final quality** at 100k on most instances.  
   - **SOEA** remains a solid baseline; at 100k it improves over 10k but typically **trails UniformGA** in final best-of-run metrics.
5) **RLS and (1+1)EA** remain **important baselines**: low variance, interpretable progress. At 100k, (1+1)EA usually outperforms RLS on instances requiring occasional larger jumps.

