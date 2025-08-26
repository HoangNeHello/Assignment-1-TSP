# memetic.py
# A memetic GA for TSPLIB EUC_2D TSP
# - Representation: permutation of city indices [0..n-1]
# - Selection: tournament + elitism
# - Variation: OX/PMX/CX/ERX + insert/swap/inversion (from variation.py)
# - Local search: bounded 2-opt (from local_search.py) applied intermittently to top offspring
#
# Usage (single instance, quick sanity):
#   python3 memetic.py --base TSPLIB --instances eil51 --runs 3 --pop 50 --gens 2000
#
# Full assignment-style run (long):
#   python3 memetic.py --base TSPLIB \
#     --instances eil51 eil76 eil101 st70 kroA100 kroC100 kroD100 lin105 pcb442 pr2392 usa13509 \
#     --pop 50 --gens 20000 --runs 30 --out results/memetic_ga.txt
#
from __future__ import annotations
import os, argparse, random, statistics
from typing import List, Dict, Tuple, Optional

from TSP import TSP
from variation import (
    ordered_crossover, pmx_crossover, cycle_crossover, edge_recombination_crossover,
    insert_mutation, swap_mutation, inversion_mutation
)
from local_search import local_search  # optimized 2-opt with span + move caps


# ------------------------ utilities ------------------------

def ensure_dir(path: str) -> None:
    if path:
        os.makedirs(path, exist_ok=True)

def random_perm(n: int, rng: random.Random) -> List[int]:
    arr = list(range(n))
    rng.shuffle(arr)
    return arr

def evaluate(pop: List[List[int]], tsp: TSP) -> List[Dict]:
    """Return [{'tour': tour, 'cost': int}, ...]"""
    return [{"tour": t, "cost": tsp.tour_length(t)} for t in pop]

def pick_crossover(name: str):
    name = name.lower()
    if name in ("ox", "ordered", "order", "ordered_crossover"):
        return ordered_crossover
    if name in ("pmx", "pmxcrossover", "pmx_crossover"):
        return pmx_crossover
    if name in ("cx", "cycle", "cycle_crossover"):
        return cycle_crossover
    if name in ("erx", "edge", "edge_recombination", "edge_recombination_crossover"):
        return edge_recombination_crossover
    raise ValueError(f"Unknown crossover '{name}'")

def pick_mutation(name: str):
    name = name.lower()
    if name in ("insert", "ins", "jump"):
        return insert_mutation
    if name in ("swap", "exchange"):
        return swap_mutation
    if name in ("invert", "inversion", "reverse", "rev"):
        return inversion_mutation
    raise ValueError(f"Unknown mutation '{name}'")


# ---------------------- selection ops ----------------------

def tournament_select(evaluated: List[Dict], k: int, rng: random.Random) -> Dict:
    """Return the best (lowest cost) among k sampled individuals (dicts)."""
    k = max(1, min(k, len(evaluated)))
    contenders = rng.sample(evaluated, k)
    return min(contenders, key=lambda z: z["cost"])

def elites(evaluated: List[Dict], k: int) -> List[Dict]:
    k = max(0, min(k, len(evaluated)))
    return sorted(evaluated, key=lambda z: z["cost"])[:k]


# ------------------------ memetic GA ------------------------

def memetic_ga(
    tsp: TSP,
    pop_size: int,
    generations: int,
    *,
    crossover: str = "ERX",
    mutation: str = "insert",
    mutation_rate: float = 0.3,
    tournament_k: int = 5,
    elitism_k: int = 2,
    seed: Optional[int] = 1808,
    # local search schedule (intermittent, bounded)
    ls_every: int = 10,         # run LS every N generations (0/None to disable)
    ls_frac: float = 0.30,      # run LS on top p fraction of children
    span2opt: int = 80,         # 2-opt window ahead of i
    max_improves: int = 200,    # cap accepted improving moves in 2-opt
    stall_limit: Optional[int] = None,  # early stop if no improvement
    verbose: bool = False,
    heartbeat: bool = False,    # Print % progress
    hb_label: Optional[str] = None  # Label shows heartbeat line
) -> Dict:
    """
    Return best {'tour': List[int], 'cost': int}.
    """
    if seed is not None:
        random.seed(seed)
    rng = random.Random(seed)
    # heartbeat state
    last_pct = -1
    label = hb_label or getattr(tsp, "name", "run")

    # Build full matrix cache when small (faster tour_length); ignore errors for large instances
    try:
        if tsp.n <= 1500:
            setattr(tsp, "_M_cache", tsp.dist_matrix())
    except Exception:
        pass

    xo_fn = pick_crossover(crossover)
    mut_fn = pick_mutation(mutation)

    # --- init population ---
    pop = [random_perm(tsp.n, rng) for _ in range(pop_size)]
    eval_pop = evaluate(pop, tsp)

    best = min(eval_pop, key=lambda z: z["cost"]).copy()
    no_improv = 0

    for gen in range(1, generations + 1):
        if heartbeat:
            pct = int(gen * 100 / max(1, generations))
            if pct != last_pct:
                print(f"\r[{label}] {pct:3d}%", end="", flush=True)
                last_pct = pct

        # --- parent pool via tournament selection ---
        parents = [tournament_select(eval_pop, tournament_k, rng) for _ in range(pop_size)]

        # --- offspring via XO + mutation ---
        children: List[List[int]] = []
        while len(children) < max(0, pop_size - elitism_k):
            p1 = rng.choice(parents)["tour"]
            p2 = rng.choice(parents)["tour"]

            child = xo_fn(p1, p2)

            if rng.random() < mutation_rate:
                # variation.* functions use global random; we already seeded global RNG
                child = mut_fn(child)

            children.append(child)

        # --- (optional) memetic local search (bounded 2-opt) ---
        if ls_every and (gen % ls_every == 0) and children:
            scored = [{"tour": c, "cost": tsp.tour_length(c)} for c in children]
            scored.sort(key=lambda z: z["cost"])
            take = max(1, int(len(scored) * ls_frac))
            for z in scored[:take]:
                improved_tour, _ = local_search(
                    tsp, z["tour"], neighborhood="2opt", strategy="first",
                    max_improves=max_improves, span2opt=span2opt
                )
                z["tour"] = improved_tour
                z["cost"] = tsp.tour_length(improved_tour)
            children = [z["tour"] for z in scored]

        # --- survivor selection: children + elites ---
        next_eval: List[Dict] = [{"tour": c, "cost": tsp.tour_length(c)} for c in children]
        next_eval.extend(elites(eval_pop, elitism_k))
        eval_pop = next_eval

        # --- best tracking / early stop ---
        cur_best = min(eval_pop, key=lambda z: z["cost"])
        if cur_best["cost"] < best["cost"]:
            best = cur_best.copy()
            no_improv = 0
        else:
            no_improv += 1

        if verbose and (gen % max(1, generations // 10) == 0):
            print(f"[gen {gen:>6}] best={best['cost']}")

        if stall_limit is not None and no_improv >= stall_limit:
            if verbose:
                print(f"[early stop] no improvement in {stall_limit} generations.")
            break

    if heartbeat:
        print()  # newline at 100%
    return best


# -------------------------- CLI ----------------------------

DEFAULT_INSTANCES = [
    "eil51", "eil76", "eil101", "st70",
    "kroA100", "kroC100", "kroD100",
    "lin105", "pcb442", "pr2392", "usa13509"
]

def find_instance(base_dir: str, name: str) -> Optional[str]:
    for stem in (name, name.lower(), name.upper()):
        p = os.path.join(base_dir, stem + ".tsp")
        if os.path.isfile(p):
            return p
        gz = p + ".gz"
        if os.path.isfile(gz):
            # lazy decompress next to it
            import gzip
            try:
                with gzip.open(gz, "rt") as fin, open(p, "w") as fout:
                    fout.write(fin.read())
                return p
            except Exception:
                pass
    return None

def main():
    ap = argparse.ArgumentParser(description="Memetic GA for TSPLIB EUC_2D TSP")
    ap.add_argument("--base", default="TSPLIB", help="Folder with .tsp/.tsp.gz files")
    ap.add_argument("--instances", nargs="*", default=DEFAULT_INSTANCES,
                    help="Instance names without extension (default: the 11 required)")
    ap.add_argument("--runs", type=int, default=5, help="Runs per instance (default: 5)")
    ap.add_argument("--pop", type=int, default=50, help="Population size (default: 50)")
    ap.add_argument("--gens", type=int, default=2000, help="Generations (default: 2000)")
    ap.add_argument("--seed", type=int, default=42, help="Seed for reproducibility")
    ap.add_argument("--crossover", default="ERX", help="OX | PMX | CX | ERX (default: ERX)")
    ap.add_argument("--mutation", default="insert", help="insert | swap | inversion (default: insert)")
    ap.add_argument("--mutation-rate", type=float, default=0.30, help="Mutation rate (default: 0.30)")
    ap.add_argument("--tournament-k", type=int, default=5, help="Tournament size (default: 5)")
    ap.add_argument("--elitism-k", type=int, default=2, help="Elites kept each gen (default: 2)")
    ap.add_argument("--ls-every", type=int, default=10, help="Run LS every N gens (0 to disable)")
    ap.add_argument("--ls-frac", type=float, default=0.30, help="Fraction of children to polish (default: 0.30)")
    ap.add_argument("--span2opt", type=int, default=80, help="2-opt window ahead of i (default: 80)")
    ap.add_argument("--max-improves", type=int, default=200, help="2-opt accepted move cap (default: 200)")
    ap.add_argument("--stall-limit", type=int, default=None, help="Early stop if no-improv for N gens")
    ap.add_argument("--out", default="results/memetic_ga.txt", help="Results file path")
    ap.add_argument("--heartbeat", action="store_true", help="Print % progress during each run") # Heartbeat
    args = ap.parse_args()

    ensure_dir(os.path.dirname(args.out))

    # deterministic global RNG for variation functions that call random.*
    if args.seed is not None:
        random.seed(args.seed)

    rows = []
    for name in args.instances:
        tsp_path = find_instance(args.base, name)
        if tsp_path is None:
            print(f"[WARN] Missing {name}.tsp in {args.base}/ — skipping.")
            continue

        tsp = TSP.from_file(tsp_path)
        print(f"[INFO] {tsp.name}.tsp: n={tsp.n} — running {args.runs} runs, pop={args.pop}, gens={args.gens}")

        costs = []
        for r in range(args.runs):
            best = memetic_ga(
                tsp, args.pop, args.gens,
                crossover=args.crossover, mutation=args.mutation,
                mutation_rate=args.mutation_rate, tournament_k=args.tournament_k,
                elitism_k=args.elitism_k, seed=(args.seed + r if args.seed is not None else None),
                ls_every=args.ls_every, ls_frac=args.ls_frac,
                span2opt=args.span2opt, max_improves=args.max_improves,
                stall_limit=args.stall_limit, verbose=False,
                heartbeat=args.heartbeat, hb_label=f"{tsp.name} r{r+1}/{args.runs}"
            )
            costs.append(best["cost"])

        mean = statistics.fmean(costs)
        std = statistics.stdev(costs) if len(costs) > 1 else 0.0
        rows.append((name, args.pop, args.gens, args.runs, mean, std))
        print(f"  -> avg={mean:.2f}, std={std:.2f}")

    with open(args.out, "w") as f:
        f.write("# instance  pop  gens  runs  mean  stdev\n")
        for name, pop, gens, runs, mean, std in rows:
            f.write(f"{name} {pop} {gens} {runs} {mean:.2f} {std:.2f}\n")

    print(f"\n[OK] Wrote {args.out}")


if __name__ == "__main__":
    main()
