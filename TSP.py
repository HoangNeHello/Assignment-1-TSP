<<<<<<< HEAD
from __future__ import annotations
import math
from typing import List, Tuple, Optional

class TSP:
    """
    Representation of a symmetric TSPLIB95 EUC_2D instance.

    Attributes
    ----------
    name : str
    comment : Optional[str]
    n : int
    coords : List[Tuple[float, float]]   # 0-indexed nodes: 0..n-1
    """
    def __init__(self, name: str, coords: List[Tuple[float, float]], comment: Optional[str] = None):
        if not coords:
            raise ValueError("coords must be non-empty")
        self.name = name
        self.comment = comment
        self.coords = coords
        self.n = len(coords)
        self._dist_matrix: Optional[List[List[int]]] = None  # lazy

    # ---------- Construction helpers ----------
    @classmethod
    def from_file(cls, path: str) -> "TSP":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return cls._parse_tsplib(f.read())

    @classmethod
    def from_string(cls, data: str) -> "TSP":
        return cls._parse_tsplib(data)

    @staticmethod
    def _parse_tsplib(text: str) -> "TSP":
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() and ln.strip() != "EOF"]
        headers = {}
        i = 0

        # Read header lines until NODE_COORD_SECTION
        while i < len(lines) and not lines[i].startswith("NODE_COORD_SECTION"):
            ln = lines[i]
            if ":" in ln:
                k, v = ln.split(":", 1)
                headers[k.strip().upper()] = v.strip()
            i += 1

        if i == len(lines) or not lines[i].startswith("NODE_COORD_SECTION"):
            raise ValueError("TSPLIB file missing NODE_COORD_SECTION")

        name = headers.get("NAME", "unnamed")
        comment = headers.get("COMMENT")
        etype = headers.get("EDGE_WEIGHT_TYPE", "").upper()
        if etype != "EUC_2D":
            raise ValueError(f"Unsupported EDGE_WEIGHT_TYPE: {etype} (only EUC_2D supported)")

        i += 1  # first coord line
        coords: List[Tuple[float, float]] = []
        # TSPLIB coord lines: id x y  (id is usually 1..n but we ignore it and reindex)
        while i < len(lines) and not lines[i].endswith(":"):
            parts = lines[i].split()
            if len(parts) < 3:
                break
            # parts[0] is node id; ignore and trust order
            x = float(parts[1]); y = float(parts[2])
            coords.append((x, y))
            i += 1

        # Debugging DIMENSION check
        dim_hdr = headers.get("DIMENSION")
        if dim_hdr is not None:
            try:
                dim = int(dim_hdr)
            except ValueError:
                dim = None  # can't parse -> skip strict check
            if dim is not None and dim != len(coords):
                raise ValueError(f"DIMENSION={dim} but parsed {len(coords)} coordinates")
            
            return TSP(name=name, coords=coords, comment=comment)  # Parse the TSP



    # ---------- Distances ----------
    @staticmethod
    def _euc2d_round(dx: float, dy: float) -> int:
        # TSPLIB EUC_2D: round to nearest integer
        return int(math.hypot(dx, dy) + 0.5)

    def distance(self, i: int, j: int) -> int:
        if i == j:
            return 0
        xi, yi = self.coords[i]
        xj, yj = self.coords[j]
        return self._euc2d_round(xi - xj, yi - yj)

    def dist_matrix(self) -> List[List[int]]:
        if self._dist_matrix is None:
            n = self.n
            m = [[0]*n for _ in range(n)]
            for i in range(n):
                xi, yi = self.coords[i]
                for j in range(i+1, n):
                    xj, yj = self.coords[j]
                    d = self._euc2d_round(xi - xj, yi - yj)
                    m[i][j] = m[j][i] = d
            self._dist_matrix = m
        return self._dist_matrix

    # ---------- Utilities ----------
    def tour_length(self, tour: List[int], return_to_start: bool = True) -> int:
        """tour: sequence of node indices (0..n-1)."""
        if not tour:
            return 0
        total = 0
        for a, b in zip(tour, tour[1:]):
            total += self.distance(a, b)
        if return_to_start and len(tour) > 1:
            total += self.distance(tour[-1], tour[0])
        return total

    def __repr__(self) -> str:
        
        return f"TSP(name={self.name!r}, n={self.n})"

if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 2:
        print("Usage: python3 TSP.py <path-to-tsplib-file.tsp>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}")
        sys.exit(2)

    tsp = TSP.from_file(path)
    print(f"Loaded {tsp.name} with {tsp.n} nodes (EUC_2D).")
    print("d(0,1) =", tsp.distance(0, 1))
    print("Naive tour length:", tsp.tour_length(list(range(tsp.n))))
=======
#this is a test
>>>>>>> e9a83e3245915dddec27ea08684f6d7bbbcf90be
