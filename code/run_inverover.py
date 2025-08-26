# scripts/run_inverover.py
import os, numpy as np
from TSP import TSP
from inverover import inver_over

INST = [
    "eil51.tsp","eil76.tsp","eil101.tsp","st70.tsp","kroA100.tsp",
    "kroC100.tsp","kroD100.tsp","lin105.tsp","pcb442.tsp","pr2392.tsp","usa13509.tsp",
]

def main():
    os.makedirs("results", exist_ok=True)
    lines = []
    seed_base = 20250901
    for name in INST:
        tsp = TSP.from_file(os.path.join("TSPLIB", name))
        vals = []
        for r in range(30):
            _, best_cost = inver_over(
                tsp, population_size=50, generations=20000, p=0.02, seed=seed_base + r
            )
            vals.append(best_cost)
        avg, std = float(np.mean(vals)), float(np.std(vals))
        line = f"{name}: avg={avg:.2f}, std={std:.2f}"
        print(line)
        lines.append(line)

    with open("results/inverover.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
