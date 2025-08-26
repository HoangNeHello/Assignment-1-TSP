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
   lin105.tsp, pcb442.tsp, pr2392.tsp, usa13509.tsp 

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

150-word summary goes in:
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
Quick test for mutations (insert/swap/inversion) and crossovers (OX/PMX/CX/ERX):
   python3 test_class.py    

Notes:
- OX keeps a slice from P1 and fills remaining in P2 order.
- PMX uses a fixed mapping (no infinite loops).
- ERX builds adjacency from BOTH parents and prefers common/shortest lists.

------------------------------------------------------------
Exercise 5 – Selection (roulette/tournament/elitism)
------------------------------------------------------------
Tests:
   python3 test_selection.py

They sample selections repeatedly and check that
tournament ≤ roulette ≤ population mean (on average).

------------------------------------------------------------
Exercise 6 – Evolutionary Algorithms & Benchmarking
------------------------------------------------------------
A) Three EA baselines (A1/A2/A3)
---------------------------------
We provide three baseline EAs in algorithms.py (see Algorithm.genalgo):
  A1: Roulette (fitness-proportionate) + OX + insert mutation
  A2: Elitism + PMX + inversion mutation
  A3: Tournament + Edge Recombination + insert mutation

Run the full benchmarking grid (instances × pop sizes × generations):
    python3 test_algorithms.py

This runs population sizes {20, 50, 100, 200} at generations {2000, 5000, 10000, 20000}
for each of the required instances and prints progress to the terminal. The script writes
a summary file to:
    results/algorithms_grid.txt

B) “Best” algorithm: Memetic GA (recommended)
---------------------------------------------
We also provide a memetic GA (crossover + mutation + 2-opt local search) for the
“best algorithm” requirement.

Run 30 times per instance at pop=50 and gens=20000:
   python3 memetic_ga.py --base TSPLIB \
  --instances eil51 eil76 eil101 st70 kroA100 kroC100 kroD100 lin105 pcb442 pr2392 usa13509 \
  --pop 50 --gens 20000 --runs 30 \
  --out results/memetic_ga.txt

This writes per-instance mean and standard deviation to:
    results/memetic_ga.txt

------------------------------------------------------------
Exercise 7 – Inver-over Evolutionary Algorithm
------------------------------------------------------------
Smoke test:
   python3 run_inverover_quick.py


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
