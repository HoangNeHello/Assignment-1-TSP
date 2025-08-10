
import math
import random
import sys
import argparse
from typing import List, Tuple, Optional

# NOTE FOR YOUR ASSIGNMENT: This example is for learning only. 
# Do not submit this code as your own. Write your own implementation.

class TSP:
    def __init__(self, name: str, coords: List[Tuple[float, float]], metric: str = "EUC_2D"):
        self.name = name
        self.coords = coords  # 0-based list of (x, y)
        self.n = len(coords)
        self.metric = metric.upper()

        # Distance mode: precompute matrix for small/medium n; on-the-fly for large
        self._dist_matrix = None
        if self.metric == "EUC_2D" and self.n <= 1000:
            self._precompute_dist_matrix()

    # ---------- TSPLIB parsing ----------
    @staticmethod
    def from_tsplib(path: str) -> "TSP":
        name = None
        dimension = None
        metric = None
        coords = None
        in_coords = False
        coord_lines = []

        def parse_header_value(line: str) -> str:
            # Accept formats like "KEY : value" or "KEY:value"
            if ":" in line:
                return line.split(":", 1)[1].strip()
            return line.split(None, 1)[1].strip() if " " in line else ""

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.upper() == "EOF":
                    break
                up = line.upper()

                if in_coords:
                    # stop if we hit another section (defensive)
                    if up.startswith("DISPLAY_DATA_SECTION") or up.startswith("EDGE_WEIGHT_SECTION"):
                        break
                    # Expect: id  x  y
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            idx = int(float(parts[0]))  # tolerate '1', '1.0'
                            x = float(parts[1])
                            y = float(parts[2])
                            coord_lines.append((idx, x, y))
                        except ValueError:
                            # Non-coordinate line; ignore
                            pass
                    continue

                if up.startswith("NAME"):
                    name = parse_header_value(line)
                elif up.startswith("DIMENSION"):
                    v = parse_header_value(line)
                    try:
                        dimension = int(v)
                    except ValueError:
                        # Sometimes "DIMENSION : 51" is clean; else fallback
                        dimension = int(v.split()[0])
                elif up.startswith("EDGE_WEIGHT_TYPE"):
                    metric = parse_header_value(line).upper()
                elif up.startswith("NODE_COORD_SECTION"):
                    in_coords = True

            # After reading, build coords with 0-based indices
            if dimension is None or metric is None:
                raise ValueError("Missing DIMENSION or EDGE_WEIGHT_TYPE in TSPLIB file.")
            coords = [(0.0, 0.0)] * dimension
            for idx, x, y in coord_lines:
                if not (1 <= idx <= dimension):
                    raise ValueError(f"Node id {idx} out of range 1..{dimension}")
                coords[idx - 1] = (x, y)

        return TSP(name or path, coords, metric=metric)

    # ---------- Distances ----------
    def _precompute_dist_matrix(self) -> None:
        n = self.n
        self._dist_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            xi, yi = self.coords[i]
            for j in range(i + 1, n):
                d = self._edge_distance(i, j)
                self._dist_matrix[i][j] = d
                self._dist_matrix[j][i] = d

    def edge(self, i: int, j: int) -> int:
        if i == j:
            return 0
        if self._dist_matrix is not None:
            return self._dist_matrix[i][j]
        return self._edge_distance(i, j)

    def _edge_distance(self, i: int, j: int) -> int:
        if self.metric == "EUC_2D":
            x1, y1 = self.coords[i]
            x2, y2 = self.coords[j]
            return int(math.hypot(x1 - x2, y1 - y2) + 0.5)  # TSPLIB EUC rounding
        elif self.metric == "GEO":
            # Minimal GEO support (TSPLIB-style). Coords are assumed as "degree.decimalminutes".
            # Convert to radians per TSPLIB spec (deg + 5*min/3).
            # Many TSPLIB GEO files store lat/long in this special format.
            lat1, lon1 = self.coords[i]
            lat2, lon2 = self.coords[j]
            def to_radians_geo(v: float) -> float:
                deg = int(v)
                minutes = v - deg
                return math.pi * (deg + 5.0 * minutes / 3.0) / 180.0
            rlat1, rlon1 = to_radians_geo(lat1), to_radians_geo(lon1)
            rlat2, rlon2 = to_radians_geo(lat2), to_radians_geo(lon2)
            RRR = 6378.388
            q1 = math.cos(rlon1 - rlon2)
            q2 = math.cos(rlat1 - rlat2)
            q3 = math.cos(rlat1 + rlat2)
            # TSPLIB GEO distance formula:
            dij = int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
            return dij
        else:
            raise NotImplementedError(f"Unsupported metric: {self.metric}")

    # ---------- Tours ----------
    def tour_cost(self, perm: List[int]) -> int:
        if len(perm) != self.n:
            raise ValueError("Permutation length mismatch")
        seen = set(perm)
        if len(seen) != self.n or min(perm) != 0 or max(perm) != self.n - 1:
            raise ValueError("Permutation must contain each city 0..n-1 exactly once")
        total = 0
        for k in range(self.n - 1):
            total += self.edge(perm[k], perm[k + 1])
        total += self.edge(perm[-1], perm[0])  # wrap to start
        return total

# ---------- 2-opt (first improvement) ----------
def two_opt_first_improvement(tsp: TSP, perm: List[int], max_iters: int = 100000) -> List[int]:
    n = tsp.n
    if n < 4:
        return perm[:]
    improved = True
    iters = 0
    while improved and iters < max_iters:
        improved = False
        iters += 1
        # scan pairs (i, j)
        for i in range(n - 1):
            a, b = perm[i], perm[(i + 1) % n]
            for j in range(i + 2, n if i > 0 else n - 1):
                c, d = perm[j], perm[(j + 1) % n]
                # delta for replacing (a-b) + (c-d) by (a-c) + (b-d)
                delta = -tsp.edge(a, b) - tsp.edge(c, d) + tsp.edge(a, c) + tsp.edge(b, d)
                if delta < 0:
                    # reverse segment (i+1 .. j)
                    perm[i + 1 : j + 1] = reversed(perm[i + 1 : j + 1])
                    improved = True
                    break
            if improved:
                break
    return perm

# ---------- Utilities ----------
def random_tour(n: int, rng: random.Random) -> List[int]:
    perm = list(range(n))
    rng.shuffle(perm)
    return perm

# ---------- Demo / CLI ----------
def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Tiny TSP example with 2-opt (EUC_2D + basic GEO).")
    parser.add_argument("--tsplib", type=str, help="Path to a TSPLIB .tsp file (EUC_2D or GEO).")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility.")
    parser.add_argument("--runs", type=int, default=1, help="How many runs to try (random starts).")
    args = parser.parse_args(argv)

    rng = random.Random(args.seed)

    if args.tsplib:
        tsp = TSP.from_tsplib(args.tsplib)
        print(f"Loaded TSPLIB: NAME={tsp.name}  N={tsp.n}  METRIC={tsp.metric}")
    else:
        # Toy 10-city instance (EUC_2D)
        coords = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
        ]
        tsp = TSP("toy10", coords, metric="EUC_2D")
        print(f"Loaded toy instance: NAME={tsp.name}  N={tsp.n}  METRIC={tsp.metric}")

    best_cost = None
    best_perm = None
    for r in range(args.runs):
        perm = random_tour(tsp.n, rng)
        cost0 = tsp.tour_cost(perm)
        perm2 = two_opt_first_improvement(tsp, perm[:])
        cost1 = tsp.tour_cost(perm2)
        if best_cost is None or cost1 < best_cost:
            best_cost = cost1
            best_perm = perm2[:]
        print(f"Run {r+1}/{args.runs}: start_cost={cost0}  improved_cost={cost1}")

    print(f"BEST cost over {args.runs} run(s): {best_cost}")
    print(f"BEST tour (0-based): {best_perm}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
