# run_mmas_star.py
import os, csv, time, json, math, random
from mmas_star import MMASStar, MMASStarConfig
from problems import get_benchmarks

REPEATS = 30
SEED_BASE = 20251005

def run_all():
    os.makedirs("results", exist_ok=True)
    csv_path = "results/mmas_star_runs.csv"

    if not os.path.isfile(csv_path):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow([
                "func","n","rho","run",
                "best","evals_per_point","curve_json","secs"
            ])

    for fname, n, budget, func in get_benchmarks():
        rhos = [1.0, 1.0 / math.sqrt(n), 1.0 / n]
        for rho in rhos:
            for r in range(REPEATS):
                t0 = time.time()

                cfg = MMASStarConfig(
                    n=n,
                    num_ants=10,
                    rho=rho,
                    seed=SEED_BASE + hash((fname, n, r, rho)) % 10_000_000
                )
                algo = MMASStar(cfg)

                best, curve = algo.run(budget, func)
                dt = time.time() - t0


                evals_per_point = cfg.num_ants

                with open(csv_path, "a", newline="", encoding="utf-8") as f:
                    wr = csv.writer(f)
                    wr.writerow([
                        fname, n, f"{rho:.6g}", r+1,
                        best, evals_per_point,
                        json.dumps(curve), f"{dt:.2f}"
                    ])

                print(
                    f"[MMAS*] {fname} n={n} rho={rho:.4g} run={r+1}/{REPEATS} "
                    f"best={best} secs={dt:.2f}"
                )

if __name__ == "__main__":
    run_all()
