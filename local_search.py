# local_search.py
from __future__ import annotations
import os, random, statistics, argparse, gzip
from typing import List, Tuple, Optional
from TSP import TSP

# ---------- knobs ----------
MATRIX_CACHE_THRESHOLD = 1500  # cache NxN only when n <= 1500

# ---------- helpers ----------
def d(tsp: TSP, a: int, b: int) -> int:
    """Fast distance lookup; avoid O(n^2) memory on very large instances."""
    if tsp.n <= MATRIX_CACHE_THRESHOLD:
        M = getattr(tsp, "_M_cache", None)
        if M is None:
            M = tsp.dist_matrix()
            setattr(tsp, "_M_cache", M)
        return M[a][b]
    else:
        return tsp.distance(a, b)

def ensure_dir(path: str) -> None:
    if path:
        os.makedirs(path, exist_ok=True)

# ---------- 2-opt ----------
def delta_2opt(tsp: TSP, tour: List[int], i: int, k: int) -> int:
    n = len(tour)
    if i == k or (k - i + 1) % n < 2:
        return 0
    a = tour[(i - 1) % n]
    b = tour[i]
    c = tour[k]
    d_ = tour[(k + 1) % n]
    return d(tsp, a, c) + d(tsp, b, d_) - d(tsp, a, b) - d(tsp, c, d_)

def apply_2opt(tour: List[int], i: int, k: int) -> None:
    tour[i:k+1] = reversed(tour[i:k+1])

# ---------- exchange (swap) ----------
def _adjacent(i: int, j: int, n: int) -> bool:
    return (j - i) % n == 1 or (i - j) % n == 1

def delta_swap(tsp: TSP, tour: List[int], i: int, j: int) -> int:
    if i == j:
        return 0
    n = len(tour)
    if j < i:
        i, j = j, i
    a, b = tour[(i - 1) % n], tour[i]
    c = tour[(i + 1) % n]
    d_, e = tour[(j - 1) % n], tour[j]
    f = tour[(j + 1) % n]

    if _adjacent(i, j, n):
        old = d(tsp, a, b) + d(tsp, b, e) + d(tsp, e, f)
        new = d(tsp, a, e) + d(tsp, e, b) + d(tsp, b, f)
        return new - old
    else:
        old = d(tsp, a, b) + d(tsp, b, c) + d(tsp, d_, e) + d(tsp, e, f)
        new = d(tsp, a, e) + d(tsp, e, c) + d(tsp, d_, b) + d(tsp, b, f)
        return new - old

def apply_swap(tour: List[int], i: int, j: int) -> None:
    tour[i], tour[j] = tour[j], tour[i]

# ---------- jump (insert) ----------
def delta_insert(tsp: TSP, tour: List[int], i: int, j: int) -> int:
    """Move city at position i to appear BEFORE position j (circular tour)."""
    n = len(tour)
    if i == j or ((j - i) % n == 1):
        return 0
    a = tour[(i - 1) % n]
    x = tour[i]
    b = tour[(i + 1) % n]
    removal = d(tsp, a, b) - d(tsp, a, x) - d(tsp, x, b)

    j_eff = j - 1 if j > i else j  # index after removal
    if j_eff == 0:
        c_prev = tour[-1]
        c = tour[0]
    else:
        c_prev = tour[j_eff - 1]
        c = tour[j_eff]

    insertion = -d(tsp, c_prev, c) + d(tsp, c_prev, x) + d(tsp, x, c)
    return removal + insertion

def apply_insert(tour: List[int], i: int, j: int) -> None:
    n = len(tour)
    if i == j or ((j - i) % n == 1):
        return
    x = tour.pop(i)
    if j > i:
        j -= 1
    tour.insert(j, x)

# ---------- generic local search ----------
def local_search(
    tsp: TSP,
    tour: List[int],
    neighborhood: str,
    strategy: str = "first",            # "first" or "best"
    max_improves: Optional[int] = 20000,
    span2opt: Optional[int] = None,     # 2-opt window (None = full)
) -> Tuple[List[int], int]:
    n = len(tour)
    best_len = tsp.tour_length(tour)
    improves = 0

    improved = True
    while improved:
        improved = False
        best_delta = 0
        best_move = None

        if neighborhood == "2opt":
            for i in range(n):
                # Limit k to a window ahead of i for speed on big n
                k_start = i + 2
                k_end = n if span2opt is None else min(n, i + 1 + max(2, span2opt))
                for k in range(k_start, k_end):
                    delta = delta_2opt(tsp, tour, i, k)
                    if delta < 0:
                        if strategy == "first":
                            apply_2opt(tour, i, k)
                            best_len += delta
                            improves += 1
                            best_len = tsp.tour_length(tour)  # resync
                            if max_improves is not None and improves >= max_improves:
                                return tour, best_len
                            improved = True
                            break
                        elif delta < best_delta:
                            best_delta = delta
                            best_move = ("2opt", i, k)
                if improved and strategy == "first":
                    break

            if (not improved) and strategy == "best" and best_move:
                _, i, k = best_move
                apply_2opt(tour, i, k)
                best_len += best_delta
                improves += 1
                best_len = tsp.tour_length(tour)  # resync
                if max_improves is not None and improves >= max_improves:
                    return tour, best_len
                improved = True

        elif neighborhood == "exchange":
            for i in range(n - 1):
                for j in range(i + 1, n):
                    delta = delta_swap(tsp, tour, i, j)
                    if delta < 0:
                        if strategy == "first":
                            apply_swap(tour, i, j)
                            best_len += delta
                            improves += 1
                            best_len = tsp.tour_length(tour)  # resync
                            if max_improves is not None and improves >= max_improves:
                                return tour, best_len
                            improved = True
                            break
                        elif delta < best_delta:
                            best_delta = delta
                            best_move = ("swap", i, j)
                if improved and strategy == "first":
                    break

            if (not improved) and strategy == "best" and best_move:
                _, i, j = best_move
                apply_swap(tour, i, j)
                best_len += best_delta
                improves += 1
                best_len = tsp.tour_length(tour)  # resync
                if max_improves is not None and improves >= max_improves:
                    return tour, best_len
                improved = True

        elif neighborhood == "jump":
            for i in range(n):
                for j in range(n):
                    if i == j or ((j - i) % n == 1):
                        continue
                    delta = delta_insert(tsp, tour, i, j)
                    if delta < 0:
                        if strategy == "first":
                            apply_insert(tour, i, j)
                            best_len += delta
                            improves += 1
                            best_len = tsp.tour_length(tour)  # resync
                            if max_improves is not None and improves >= max_improves:
                                return tour, best_len
                            improved = True
                            break
                        elif delta < best_delta:
                            best_delta = delta
                            best_move = ("ins", i, j)
                if improved and strategy == "first":
                    break

            if (not improved) and strategy == "best" and best_move:
                _, i, j = best_move
                apply_insert(tour, i, j)
                best_len += best_delta
                improves += 1
                best_len = tsp.tour_length(tour)  # resync
                if max_improves is not None and improves >= max_improves:
                    return tour, best_len
                improved = True

        else:
            raise ValueError(f"Unknown neighborhood: {neighborhood}")

    # final safety resync
    best_len = tsp.tour_length(tour)
    return tour, best_len

# ---------- suite runner ----------
DEFAULT_INSTANCES = [
    "eil51", "eil76", "eil101", "st70",
    "kroA100", "kroC100", "kroD100",
    "lin105", "pcb442", "pr2392", "usa13509"
]

def find_instance_path(base_dir: str, name: str) -> Optional[str]:
    """Return a usable .tsp path; if only .tsp.gz exists, decompress next to it."""
    for stem in (name, name.lower(), name.upper()):
        tsp_path = os.path.join(base_dir, stem + ".tsp")
        if os.path.isfile(tsp_path):
            return tsp_path
        gz_path = tsp_path + ".gz"
        if os.path.isfile(gz_path):
            try:
                with gzip.open(gz_path, "rt") as fin, open(tsp_path, "w") as fout:
                    fout.write(fin.read())
                return tsp_path
            except Exception:
                pass
    return None

def run_suite(
    base_dir: str = "TSPLIB",
    runs: int = 30,
    strategy: str = "first",
    instances: Optional[List[str]] = None,
    out_path: str = "results/local_search.txt",
    max_improves: int = 20000,
    span2opt: int = 80,
) -> None:
    if instances is None:
        instances = DEFAULT_INSTANCES
    ensure_dir(os.path.dirname(out_path))

    algos = [("jump","first"), ("exchange","first"), ("2opt", strategy)]
    rows = []

    for name in instances:
        tsp_path = find_instance_path(base_dir, name)
        if tsp_path is None:
            print(f"[WARN] Missing {name}.tsp in {base_dir}/ — skipping.")
            continue

        print(f"[DEBUG] trying {name} at {tsp_path}")
        try:
            tsp = TSP.from_file(tsp_path)
            if tsp is None:
                print(f"[WARN] Parser returned None for {name} — skipping.")
                continue
        except Exception as e:
            print(f"[WARN] Failed to parse {name}: {e} — skipping.")
            continue

        n = tsp.n
        print(f"[INFO] {name} (n={n}) loaded.")
        for algo, strat in algos:
            print(f"  [{algo}] starting {runs} runs...", flush=True)
            results = []
            for run_idx in range(runs):
                tour = list(range(n))
                random.shuffle(tour)
                tour, L = local_search(
                    tsp, tour,
                    neighborhood=algo if algo != "2opt" else "2opt",
                    strategy=strat,
                    max_improves=max_improves,
                    span2opt=span2opt
                )
                results.append(L)
                step = max(1, runs // 5)
                if (run_idx + 1) % step == 0 or (run_idx + 1) == runs:
                    print(f"    [{algo}] {run_idx + 1}/{runs} done", flush=True)

            mn = min(results)
            mean = statistics.fmean(results)
            rows.append((name, algo, runs, mn, mean))
            print(f"  {algo:9s} | min={mn:>8d}  mean={mean:>12.2f}")

    with open(out_path, "w") as f:
        f.write("# instance  algorithm  runs  min  mean\n")
        for name, algo, rr, mn, mean in rows:
            f.write(f"{name} {algo} {rr} {mn} {mean:.2f}\n")

    print(f"\n[OK] Wrote {out_path}")

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Local search (jump/exchange/2opt) for TSPLIB TSP.")
    ap.add_argument("--base", default="TSPLIB", help="Directory containing .tsp files (default: TSPLIB)")
    ap.add_argument("--runs", type=int, default=30, help="Runs per algorithm per instance (default: 30)")
    ap.add_argument("--strategy", choices=["first","best"], default="first",
                    help="Improvement rule (default: first)")
    ap.add_argument("--instances", nargs="*", default=DEFAULT_INSTANCES,
                    help="Instance names without extension")
    ap.add_argument("--out", default="results/local_search.txt", help="Output results file")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    ap.add_argument("--max-improves", type=int, default=20000,
                    help="Max accepted improving moves per run (default: 20000)")
    ap.add_argument("--span2opt", type=int, default=80,
                    help="2-opt: only try k up to this many positions ahead of i (default: 80)")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    run_suite(base_dir=args.base, runs=args.runs, strategy=args.strategy,
              instances=args.instances, out_path=args.out,
              max_improves=args.max_improves, span2opt=args.span2opt)

if __name__ == "__main__":
    main()
