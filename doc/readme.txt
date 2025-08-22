============================================================
TSP Assignment – How to Run
============================================================

- Repo layout (key files):
  TSP.py
  local_search.py
  variation.py
  tsp_class.py
  tsp_selection.py
  tests/ (optional test_*.py you may have)
  TSPLIB/   ← .tsp/.tsp.gz instances are here
  results/  ← outputs will be written here
  doc/

Getting TSPLIB instances
------------------------
1) Create the folder:
   mkdir -p TSPLIB

2) Download/place these files (exact names/case matter):
   eil51.tsp, eil76.tsp, eil101.tsp, st70.tsp,
   kroA100.tsp, kroC100.tsp, kroD100.tsp,
   lin105.tsp, pcb442.tsp, pr2392.tsp, usa13509.tsp  (or .tsp.gz)

3) If you only have .tsp.gz, decompress next to it:
   gunzip -k TSPLIB/usa13509.tsp.gz   # leaves .tsp in place

------------------------------------------------------------
Exercise 1 – Problem Representation (TSP.py)
------------------------------------------------------------
Run on any EUC_2D TSPLIB file:
   python3 TSP.py TSPLIB/eil101.tsp

Expected: it prints the instance name, size, example distance, and a naive tour length.

------------------------------------------------------------
Exercise 2 – Local Search (jump / exchange / 2-opt)
------------------------------------------------------------
Run the full suite (30 runs/instance) and write results/local_search.txt:
   python3 local_search.py \
     --instances eil51 eil76 eil101 st70 kroA100 kroC100 kroD100 lin105 pcb442 pr2392 usa13509 \
     --runs 30 \
     --out results/local_search.txt

Useful flags:
   --strategy {first,best}      (default: first)
   --seed SEED                  (default: 42)
   --max-improves N             (default: 20000, safety cap per run)
   --span2opt K                 (default: 80; 2-opt window size for speed on large n)

Your 150-word summary goes in:
   results/local_search_analysis.txt   (write manually based on the numbers)

------------------------------------------------------------
Exercise 3 – Individual & Population
------------------------------------------------------------
Quick test (robust):
   python3 test_class.py

Or interactively:
   python3 - <<'PY'
from TSP import TSP
from tsp_class import Individual, Population
tsp = TSP.from_file("TSPLIB/eil51.tsp")
pop = Population(tsp, size=50)
print("Best fitness:", pop.best_individual().fitness())
print("Mean fitness:", pop.mean_fitness())
PY

------------------------------------------------------------
Exercise 4 – Variation Operators (mutation/crossover)
------------------------------------------------------------
Sanity tests for mutations (insert/swap/inversion) and crossovers (OX/PMX/CX/ERX):
   python3 test_Eileen.py      # or your test_variation_ops.py if named differently

Notes:
- OX keeps a slice from P1 and fills remaining in P2 order.
- PMX uses a fixed mapping (no infinite loops).
- ERX builds adjacency from BOTH parents and prefers common/shortest lists.

------------------------------------------------------------
Exercise 5 – Selection (roulette/tournament/elitism)
------------------------------------------------------------
Tests (any of these, depending on your file names):
   python3 test_Cynthia.py
   python3 test_Jiahe.py
   python3 test_selection.py

They sample selections repeatedly and check that
tournament ≤ roulette ≤ population mean (on average).

------------------------------------------------------------
Exercise 6 – Evolutionary Algorithms & Benchmarking
------------------------------------------------------------
We provide three EA designs (see doc/algorithm_design.txt).
If you are using a script named ea.py (baseline GA):
   python3 ea.py \
     --instances eil51 eil76 eil101 st70 kroA100 kroC100 kroD100 lin105 pcb442 pr2392 usa13509 \
     --pop 50 --gens 20000 --runs 30 \
     --algo baseline --out results/your_EA.txt

Benchmark grid (as required):
- Population sizes: 20, 50, 100, 200
- Generations: 2000, 5000, 10000, 20000
- For the “best” algorithm: pop=50, gens=20000, runs=30
  → report mean and standard deviation per instance in results/your_EA.txt

(If your EA script uses different flags, see its --help.)

------------------------------------------------------------
Troubleshooting
------------------------------------------------------------
- “file not found”: ensure the file is in TSPLIB/ and the name/case match.
- “Unsupported EDGE_WEIGHT_TYPE”: only EUC_2D is supported by TSP.py.
- Very large instances: local_search.py auto-switches to on-the-fly distances
  (no full matrix) and limits 2-opt span with --span2opt for speed.
- Reproducibility: set --seed on runners.

------------------------------------------------------------
Contacts / Notes
------------------------------------------------------------
- All scripts are pure Python and require no extra libraries.
- Outputs are written to results/ by default.
