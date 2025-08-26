# test_algorithms.py
import os, re, subprocess, sys

INSTANCES = [
    "eil51","eil76","eil101","st70",
    "kroA100","kroC100","kroD100",
    "lin105","pcb442","pr2392","usa13509"
]
POPS = [20, 50, 100, 200]
GENS = [2000, 5000, 10000, 20000]
ALGOS = [1, 2, 3]  # your three algorithms in algorithms.py

def parse_cost(stdout: str):
    """
    algorithms.py prints an Individual at the end; we parse 'distance=...'
    """
    m = re.search(r"distance\s*=\s*([0-9]+)", stdout)
    if m:
        return int(m.group(1))
    # fallback: last integer-looking token
    nums = re.findall(r"\d+", stdout.splitlines()[-1]) if stdout.strip() else []
    return int(nums[-1]) if nums else None

def main():
    os.makedirs("results", exist_ok=True)
    out_path = "results/algorithms_grid.txt"
    with open(out_path, "w") as f:
        f.write("# instance algo pop gens best_cost\n")
        for inst in INSTANCES:
            tsp_path = os.path.join("TSPLIB", f"{inst}.tsp")
            if not os.path.isfile(tsp_path):
                print(f"[WARN] missing {tsp_path} — skipping")
                continue
            for algo in ALGOS:
                for pop in POPS:
                    for gen in GENS:
                        cmd = ["python3", "algorithms.py", tsp_path, str(algo), str(pop), str(gen)]
                        print(f"[RUN] {inst} A{algo} pop={pop} gens={gen}")
                        p = subprocess.run(cmd, capture_output=True, text=True)
                        cost = parse_cost(p.stdout)
                        if cost is None:
                            print("  [ERR] could not parse result; writing -1")
                            cost = -1
                            # Debugging hint: print(p.stdout, p.stderr)
                        f.write(f"{inst} {algo} {pop} {gen} {cost}\n")
                        f.flush()
    print(f"\n[OK] wrote {out_path}")

if __name__ == "__main__":
    main()
