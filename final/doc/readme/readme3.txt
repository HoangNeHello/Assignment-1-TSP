README – SOEA & MOEA Experiments (Ex3 & Ex4)
================================================

This repository contains Single-Objective EA (SOEA) and Multi-Objective EA (MOEA) implementations and experiment results for the COMP SCI 3316/7316 Assignment (Exercises 3 & 4). Both families follow the IOHprofiler workflow (attach logger → run → reset) and produce zips ready for IOHanalyzer.

------------------------------------------------
1) WHAT’S HERE
------------------------------------------------
- SOEA-Ex3: SOEA runs for μ ∈ {10, 20, 50} at 10,000 evaluations.
- SOEA-Ex4: SOEA runs for μ ∈ {10, 20, 50} at 100,000 evaluations (batch script included).
- MOEA-Ex3: MOEA (NSGA-II-lite) runs for pop ∈ {10, 20, 50} at 10,000 evaluations.
- MOEA-Ex4: MOEA runs for pop ∈ {10, 20, 50} at 100,000 evaluations (batch script included).

All SOEA files use the shared algorithm in soea_core.py.
All MOEA files use the shared algorithm in moea_core.py.

------------------------------------------------
2) FOLDER STRUCTURE
------------------------------------------------
SOEA-Ex3/
  soea_core.py
  SOEA-10.py
  SOEA-20.py
  SOEA-50.py
  SOEA_results_10/
  SOEA_results_20/
  SOEA_results_50/
  plots/
  results/

SOEA-Ex4/
  soea_core.py
  SOEA-10.py
  SOEA-20.py
  SOEA-50.py
  run_all.py
  SOEA_results_10/
  SOEA_results_20/
  SOEA_results_50/
  plot/
  results/

MOEA-Ex3/
  moea_core.py
  MOEA-10.py
  MOEA-20.py
  MOEA-50.py
  MOEA_results_10/
  MOEA_results_20/
  MOEA_results_50/
  plots/
  results/

MOEA-Ex4/
  moea_core.py
  MOEA-10.py
  MOEA-20.py
  MOEA-50.py
  run_all.py
  MOEA_results_10/
  MOEA_results_20/
  MOEA_results_50/
  plot/
  results/

Each *_results_xx/ contains IOHprofiler logs (ioh_data with .dat/.json).
results/ holds zipped logs ready for IOHanalyzer.
plots/ or plot/ optionally stores exported .png plots.

------------------------------------------------
3) DEPENDENCIES
------------------------------------------------
- Python 3.9+ recommended
- Install packages:
  pip install numpy tqdm ioh

------------------------------------------------
4) HOW TO RUN
------------------------------------------------
Exercise 3 (10,000 evaluations)

SOEA:
  cd SOEA-Ex3
  python SOEA-10.py
  python SOEA-20.py
  python SOEA-50.py

MOEA:
  cd MOEA-Ex3
  python MOEA-10.py
  python MOEA-20.py
  python MOEA-50.py

Each script:
- Imports soea_core.py or moea_core.py
- Runs all required GRAPH instances
- Writes logs to *_results_xx/ioh_data/
- Optionally zips outputs into results/*.zip

Exercise 4 (100,000 evaluations)

Batch runners execute 10, 20, 50 sequentially:

SOEA:
  cd SOEA-Ex4
  python run_all.py

MOEA:
  cd MOEA-Ex4
  python run_all.py

Zips appear in results/:
  SOEA_results_10.zip, SOEA_results_20.zip, SOEA_results_50.zip
  MOEA_results_10.zip, MOEA_results_20.zip, MOEA_results_50.zip

------------------------------------------------
5) BENCHMARKS & PARAMETERS
------------------------------------------------
Problems: MaxCoverage (2100–2103), MaxInfluence (2200–2203)
Runs: 30 per configuration
Budgets: 10,000 (Ex3) and 100,000 (Ex4)
Population sizes: 10, 20, 50
Seeds: fixed per run for reproducibility
Logging: IOHprofiler Analyzer with per-evaluation triggers for smooth fixed-budget curves

SOEA core: tournament(2), uniform crossover, bit-flip mutation (or exact-k swap mode).
MOEA core: NSGA-II-lite (non-dominated sorting + crowding), uniform crossover, bit-flip mutation, bi-objective (maximize f(S), minimize |S|) with unit cost per node for MaxCoverage/MaxInfluence.

------------------------------------------------
6) VISUALIZATION WITH IOHANALYZER
------------------------------------------------
1. Go to https://iohanalyzer.liacs.nl/
2. Upload each zipped result from results/.
3. Set the correct Problem ID (e.g., 2100) and the correct Dimension (matches the logs, often 450).
4. Generate Fixed-Budget plots and export .png for the report.
5. For MOEA trade-offs (Exercise 2), use your Pareto scatter plots as needed (or local plotting scripts).

------------------------------------------------
7) OUTPUT LOCATIONS
------------------------------------------------
- *_results_xx/ioh_data/ — raw .dat + .json logs
- results/ — zipped archives for IOHanalyzer upload
- plots/ or plot/ — optional exported .png

------------------------------------------------
8) EXAMPLE END-TO-END (SOEA EX4)
------------------------------------------------
cd SOEA-Ex4
python run_all.py

# inspect logs
ls SOEA_results_20/ioh_data

# optional manual zip (if auto-zip disabled)
zip -r results/SOEA_results_20.zip SOEA_results_20/ioh_data

# then upload results/*.zip to IOHanalyzer

------------------------------------------------
9) WHAT TO INCLUDE IN THE REPORT
------------------------------------------------
Exercise 3:
- For each instance, upload zips from SOEA-Ex3 and MOEA-Ex3.
- Produce fixed-budget plots showing all population sizes (10, 20, 50).
- Report mean ± sd and discuss diversity effects.

Exercise 4:
- Repeat with 100,000-eval runs (SOEA-Ex4 and MOEA-Ex4).
- Include one trade-off plot (first run) for MOEA per instance (MaxCoverage/MaxInfluence).
- Compare performance vs. 10k-eval runs.

------------------------------------------------
10) QUICK COMMANDS
------------------------------------------------
# SOEA Ex3 (10k)
python SOEA-Ex3/SOEA-10.py
python SOEA-Ex3/SOEA-20.py
python SOEA-Ex3/SOEA-50.py

# MOEA Ex3 (10k)
python MOEA-Ex3/MOEA-10.py
python MOEA-Ex3/MOEA-20.py
python MOEA-Ex3/MOEA-50.py


