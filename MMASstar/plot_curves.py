# plot_curves.py
import os, json, csv
import matplotlib.pyplot as plt
from collections import defaultdict

def load_curves(csv_path):
    curves = defaultdict(list)
    with open(csv_path, "r", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        for row in rd:
            key = (row["func"], int(row["n"]), row["rho"])
            curve = json.loads(row["curve_json"])
            curves[key].append(curve)
    return curves

def plot_one(figdir, func, n, key_curves, evals_per_point=10):
    os.makedirs(figdir, exist_ok=True)
    plt.figure(figsize=(6,4))
    for rho, curves in key_curves.items():
        L = min(len(c) for c in curves)
        avg = [sum(c[i] for c in curves)/len(curves) for i in range(L)]
        xs = [i*evals_per_point for i in range(L)]
        plt.plot(xs, avg, label=f"rho={rho}")
    plt.xlabel("evaluations")
    plt.ylabel("best-so-far")
    plt.title(f"{func}, n={n}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(figdir, f"{func}_n{n}.png"))
    plt.close()

def main():
    curves = load_curves("results/mmas_star_runs.csv")
    by_fn = defaultdict(lambda: defaultdict(dict))
    for (func, n, rho), cs in curves.items():
        by_fn[(func, n)][rho] = cs
    for (func, n), m in by_fn.items():
        plot_one("results/figs_mmas_star", func, n, m, evals_per_point=10)

if __name__ == "__main__":
    main()
