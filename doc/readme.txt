Evolutionary Algorithms — How to Run the Code (doc/readme.txt)
==============================================================

This guide explains how to reproduce the experiments and plots comparing:
- Random Search (RS)
- Randomized Local Search (RLS)
- (1+1) Evolutionary Algorithm ((1+1) EA)
- GA with Uniform Crossover (GA-UniformXover)
- Ant System (ACO-AS)
- Max–Min Ant System (MMAS) and MMAS* (iteration-best) with ρ ∈ {1, 1/√n, 1/n}

The setup targets the IOHProfiler PBO suite on functions:
F1, F2, F3, F18, F23, F24, F25 with n = 100, 10 runs, 100,000 evaluations.

-------------------------------------------------------------------------------
A) Quick Start (Recommended: single driver)
-------------------------------------------------------------------------------
1) Create & activate env (Python 3.9+):
   macOS/Linux:
       python3 -m venv .venv && source .venv/bin/activate
   Windows (PowerShell):
       py -3 -m venv .venv
       .venv\Scripts\Activate.ps1

2) Install dependencies:
       python3 -m pip install ioh numpy

3) Run the algorithms to generate logs:
       python3 random_search.py
       python3 RLS.py
       python3 OnePlusOneEA.py
       python3 ACO.py
       python3 mmas.py
       python3 mmas_star.py
       python3 Uniform_Crossover_GA.py

4) Plot in IOHanalyzer:
   - Go to https://iohanalyzer.liacs.nl/
   - Load all produced log folders (drag-and-drop).
   - Select “Fixed-budget” and tick the algorithms you want to compare.


-------------------------------------------------------------------------------
B) Running each algorithm separately (if you prefer module-by-module)
-------------------------------------------------------------------------------
Standalone scripts (if provided in your repo), plus the unified driver:

  - random_search.py              # Random Search baseline
  - RLS.py                        # Randomized Local Search
  - OnePlusOneEA.py               # (1+1) Evolutionary Algorithm
  - ACO.py                        # Ant colony

  - mmas.py(rho ∈ {1, 1/√n, 1/n}) # Max-Min ant system
  - Uniform_Crossover_GA.py       # GA with uniform crossover 
  - mmas_star.py(rho ∈ {1, 1/√n, 1/n})   # Iteration-best variant with τ-bounds

To run a single algorithm (example commands):
   python3 random_search.py
   python3 RLS.py
   python3 OnePlusOneEA.py
   python3 ACO.py
   python3 mmas.py
   python3 mmas_star.py
   python3 Uniform_Crossover_GA.py

Expected output:
- Each script attaches an IOHProfiler Analyzer logger and writes data to a log
  folder (e.g., ./ioh_logs_ex2_* or ./ioh_logs_mmas). For *direct comparison*
  on a single plot.


-------------------------------------------------------------------------------
C) Where results are written
-------------------------------------------------------------------------------
- If you used stand-alone scripts, you will have per-algorithm folders, typically:
    ./ioh_logs_random/
    ./ioh_logs_rls/
    ./ioh_logs_1p1EA/
    ./ioh_logs_aco/
    ./ioh_logs_mmas/
    ./ioh_logs_mmas_star/
    ./ioh_logs_ga_uniform/
  You can still load multiple folders into IOHanalyzer together to overlay curves.


-------------------------------------------------------------------------------
D) Changing the experiment settings
-------------------------------------------------------------------------------
Open each of algorithm .py and edit the configuration block near the top:

    DIM = 100               # problem dimension (bits)
    BUDGET = 100_000        # evaluations per run (includes initial eval)
    RUNS = 10               # independent runs
    FUNCTIONS = [1,2,3,18,23,24,25]   # PBO function IDs
    INSTANCE = 1            # IOH instance (keep 1 unless testing robustness)
    LOG_DIR = "ioh_logs_compare"      # output folder for all logs

MMAS / MMAS*:
    RHO_LIST = ["1", "1/sqrt(n)", "1/n"]
    ACO_ANTS = 20      # ants per iteration (ACO-AS, MMAS*)
GA parameters:
    GA_POP = 50        # population size
    GA_TOURNAMENT_K = 2

-------------------------------------------------------------------------------
E) Creating the comparison plots for submission
-------------------------------------------------------------------------------
** For mmas and ACO, run the (algorithm's name)_compare.py
We can achieve a result logs to put into IOH and receive the plots

** For mmas_star and Uniform_Crossover_GA, there's a zip of result logs of neccessary algorithm to put into IOH.
(Refer to /doc/comparative_logs/Comparison Logs MMASstar and Comparison Logs Uniform Crossover GA)

1) Run each script (see Quick Start step 3) to produce IOH logs.
2) Open IOHanalyzer and load the corresponding log folders.
3) For each function (F1, F2, F3, F18, F23, F24, F25), select “Fixed-budget”,
   tick the algorithms (RS, RLS, (1+1)EA, ACO, MMAS, MMAS*, GA-UniformXover),
   and export the figure (PNG/SVG).
(If you have pre-generated logs in /doc/comparative_logs, unzip and load those folders.)

-------------------------------------------------------------------------------
G) Troubleshooting
-------------------------------------------------------------------------------
- "ModuleNotFoundError: No module named 'ioh'":
    python3 -m pip install ioh

- No logs appearing:
    - Ensure scripts are executed with Python >= 3.9.
    - Verify write permissions in the working directory.
    - Confirm the problem class is PBO and the logger is attached before the run.

- Plots look empty in IOHanalyzer:
    - Make sure you selected the correct view ("Fixed-budget").
    - Ensure multiple algorithms are checked in the legend.
    - If you ran stand-alone scripts to separate folders, load those folders together.

- Very different curves after changes:
    - Check that DIM, BUDGET, RUNS, and INSTANCE match across algorithms.
    - Verify acceptance criteria (all algorithms here are elitist / accept-if-not-worse).


-------------------------------------------------------------------------------
H) Notes on algorithm behavior (short)
-------------------------------------------------------------------------------
- RS: exploration-only baseline; expect slow progress.
- RLS: excels on smooth/separable landscapes (F1–F3); plateaus on deceptive/rugged ones.
- (1+1) EA: slightly more robust than RLS via multi-bit mutations.
- GA-UniformXover: leverages recombination + mutation; generally stronger than pure local search on rugged landscapes.
- ACO-AS: probabilistic construction with pheromone learning; iteration-best update.
- MMAS / MMAS*: min–max bounded pheromones; MMAS uses global-best, MMAS* uses iteration-best.
  Lower ρ (e.g., 1/√n) typically improves late-budget robustness on deceptive/rugged cases.

End of doc/readme.txt
