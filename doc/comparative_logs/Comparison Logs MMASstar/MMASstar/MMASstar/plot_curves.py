# plot_curves.py
import csv, numpy as np, matplotlib.pyplot as plt

def load_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        for r in rd:
            curve = list(map(int, r["curve_json"].split(";")))
            rows.append((r["func"], int(r["n"]), float(r["rho"]), int(r["run"]), curve))
    return rows

def plot_mean_curves(rows, title, outpng):
    groups = {}
    for func, n, rho, run, curve in rows:
        key = (func, rho)
        groups.setdefault(key, []).append(curve)

    plt.figure(figsize=(7,5))
    for (func, rho), curves in groups.items():
        L = min(len(c) for c in curves)
        A = np.array([c[:L] for c in curves])
        mean = A.mean(axis=0)
        x = np.arange(1, L+1)
        plt.plot(x, mean, label=f"{func} ρ={rho:.3g}")
    plt.xlabel("evaluation batches (≈ proportional to evaluations)")
    plt.ylabel("best-so-far")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpng, dpi=150)
    plt.close()

if __name__ == "__main__":
    rows = load_csv("results/mmas_star_runs.csv")
    plot_mean_curves(rows, "MMAS* mean curves", "results/mmas_star_curves.png")
