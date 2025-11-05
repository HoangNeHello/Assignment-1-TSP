README — Exercise 4: How to Run (SOEA & MOEA, 100,000 evaluations)
=====================================================================

Purpose
-------
Exercise 4 repeats the SOEA/MOEA experiments at a higher fixed budget (**100,000 evaluations**)
for each population size (10, 20, 50). This guide shows exactly how to run everything **without**
any batch runner.

Environment
-----------
- Python 3.9–3.12
- Recommended: virtual environment
- Packages:
    pip install numpy tqdm ioh
  (If your scripts produce figures: pip install matplotlib)

Project layout (relevant to Ex4)
--------------------------------
SOEA-Ex4/
  soea_core.py
  SOEA-10.py
  SOEA-20.py
  SOEA-50.py
  SOEA_results_10/  SOEA_results_20/  SOEA_results_50/
  plot/   results/

MOEA-Ex4/
  moea_core.py
  MOEA-10.py
  MOEA-20.py
  MOEA-50.py
  MOEA_results_10/  MOEA_results_20/  MOEA_results_50/
  plot/   results/

(Each *_results_xx/ holds IOHprofiler logs; results/ usually stores zipped logs ready for IOHanalyzer.)

How to run — one configuration at a time
----------------------------------------
# SOEA (population 10, 20, 50)
python SOEA-Ex4/SOEA-10.py
python SOEA-Ex4/SOEA-20.py
python SOEA-Ex4/SOEA-50.py

# MOEA (population 10, 20, 50)
python MOEA-Ex4/MOEA-10.py
python MOEA-Ex4/MOEA-20.py
python MOEA-Ex4/MOEA-50.py

Budget & repetitions
--------------------
- **Budget:** 100,000 evaluations per configuration.
- **Replications:** if your scripts support multiple runs/seed loops, keep it consistent with
  earlier exercises (e.g., 30 runs). Otherwise, re-invoke the script with different seeds.

Optional: run all three populations sequentially (no batch file)
----------------------------------------------------------------
Linux/macOS (bash):
    (cd SOEA-Ex4 && python SOEA-10.py && python SOEA-20.py && python SOEA-50.py)
    (cd MOEA-Ex4 && python MOEA-10.py && python MOEA-20.py && python MOEA-50.py)

Windows (PowerShell):
    cd SOEA-Ex4; python SOEA-10.py; python SOEA-20.py; python SOEA-50.py; cd ..
    cd MOEA-Ex4; python MOEA-10.py; python MOEA-20.py; python MOEA-50.py

Outputs
-------
- *_results_xx/ioh_data/ — raw .dat/.json logs (IOHprofiler format)
- results/ — zipped archives for IOHanalyzer upload
- plot/ or plots/ — optional exported .png figures

IOHanalyzer quick steps
-----------------------
1) Open IOHanalyzer in your browser.
2) Upload each zip from **results/** you want to compare.
3) Select the correct problem/dimension (as logged in the IOH metadata).
4) Use Fixed-Budget/Fixed-Target plots to compare populations 10 vs 20 vs 50.
5) Export .png for your report.

Reproducibility
---------------
- If CLI flags exist, set a seed:  --seed 42
- Otherwise, set the seed in the script (search for np.random.seed / random.seed).
- Keep parameters identical across populations when comparing.

Troubleshooting
---------------
- Missing IOH:   pip install ioh
- Plots blocking: use a non-interactive backend (e.g., MPLBACKEND=Agg) or disable plotting.
- Missing output dirs: create plot/, results/, and *_results_xx/ if scripts don’t auto-create them.
- Windows path/permission quirks: use a simple working path (e.g., C:\work\ex4).

Scope & limitation
------------------
- Ex4 focuses on SOEA and MOEA baselines using the shared cores (**soea_core.py**, **moea_core.py**).
- IMPORTANT: "We cannot run GSEMO since the team only has 3 people who can run the code, check team contribution, so that this particular algo cannot be run in time".

Contacts
--------
When reporting issues, include: OS, Python version, exact command used, and the last ~20 lines of console output.
