# scripts/run_inverover_quick.py
import os, numpy as np
from TSP import TSP
from inverover import inver_over

INST = ["eil76.tsp"]

def main():
    os.makedirs("results", exist_ok=True)
    seed_base = 20250901
    name = INST[0]
    tsp = TSP.from_file(os.path.join("TSPLIB", name))
    vals = []
    for r in range(3):
        _, best_cost = inver_over(
            tsp, population_size=50, generations=200, p=0.02, seed=seed_base + r
        )
        vals.append(best_cost)
    avg, std = float(np.mean(vals)), float(np.std(vals))
    line = f"[QUICK] {name}: avg={avg:.2f}, std={std:.2f}, runs=3, gens=200"
    print(line)
    with open("results/inverover.txt", "w", encoding="utf-8") as f:
        f.write(line + "\n")

if __name__ == "__main__":
    main()
