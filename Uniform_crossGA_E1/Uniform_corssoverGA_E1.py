
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Optional
import os

# ---- Optional IOH import guard -------------------------------------------------
try:
    import ioh
    from ioh import get_problem, ProblemClass, logger as ioh_logger
    _HAS_IOH = True
except Exception:
    _HAS_IOH = False

Bitstring = List[int]

# ---- Variation operators -------------------------------------------------------

def uniform_crossover(p1: Bitstring, p2: Bitstring, rng: random.Random) -> Bitstring:
    
    n = len(p1)
    return [p1[i] if rng.random() < 0.5 else p2[i] for i in range(n)]

def bitflip_mutation(x: Bitstring, pm: float, rng: random.Random) -> Bitstring:
   
    n = len(x)
    y = x[:]  # copy
    for i in range(n):
        if rng.random() < pm:
            y[i] = 1 - y[i]
    return y

def random_bitstring(n: int, rng: random.Random) -> Bitstring:
    return [rng.randint(0, 1) for _ in range(n)]



@dataclass
class GAParams:
    mu: int = 20               
    lambd: int = 20            
    pc: float = 0.9            
    pm_mode: str = "1/n"       
    pm: float = 0.01           
    tournament_k: int = 3      
    seed: Optional[int] = None

@dataclass
class GAResult:
    best_solution: Bitstring
    best_fitness: float
    evaluations: int
    generations: int
    history: List[Tuple[int, float]] = field(default_factory=list)  
    meta: dict = field(default_factory=dict)

class GA:
    def __init__(
        self,
        n: int,
        fitness: Callable[[Bitstring], float],
        params: GAParams = GAParams(),
        maximize: bool = True,
    ) -> None:
        assert params.mu >= 10
        self.n = n
        self.fitness_fn = fitness
        self.params = params
        self.maximize = maximize
        self.rng = random.Random(params.seed)

    def _tournament_select(self, population: List[Bitstring], fitnesses: List[float]) -> Bitstring:
        k = min(self.params.tournament_k, len(population))
        idxs = self.rng.sample(range(len(population)), k)
        best = idxs[0]
        for i in idxs[1:]:
            if (self.maximize and fitnesses[i] > fitnesses[best]) or ((not self.maximize) and fitnesses[i] < fitnesses[best]):
                best = i
        return population[best]

    def _select_parents(self, population: List[Bitstring], fitnesses: List[float]) -> Tuple[Bitstring, Bitstring]:
        return (
            self._tournament_select(population, fitnesses),
            self._tournament_select(population, fitnesses),
        )

    def _mutation_rate(self) -> float:
        return (1.0 / self.n) if self.params.pm_mode == "1/n" else float(self.params.pm)

    def run(self, eval_budget: int = 10_000) -> GAResult:
        pm = self._mutation_rate()

        # Initialize population
        population = [random_bitstring(self.n, self.rng) for _ in range(self.params.mu)]
        fitnesses = [self.fitness_fn(ind) for ind in population]
        evals = len(population)

        # Track best
        if self.maximize:
            best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
        else:
            best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
        best = population[best_idx][:]
        best_f = fitnesses[best_idx]
        history: List[Tuple[int, float]] = [(evals, best_f)]
        generations = 0

        while evals < eval_budget:
            generations += 1

            # Variation
            offspring: List[Bitstring] = []
            while len(offspring) < self.params.lambd:
                p1, p2 = self._select_parents(population, fitnesses)
                child = uniform_crossover(p1, p2, self.rng) if self.rng.random() < self.params.pc else p1[:]
                child = bitflip_mutation(child, pm, self.rng)
                offspring.append(child)

            # Evaluate offspring
            off_fit = [self.fitness_fn(ind) for ind in offspring]
            evals += len(offspring)

            # Update best
            if self.maximize:
                local_best_idx = max(range(len(offspring)), key=lambda i: off_fit[i])
                if off_fit[local_best_idx] > best_f:
                    best_f = off_fit[local_best_idx]
                    best = offspring[local_best_idx][:]
            else:
                local_best_idx = min(range(len(offspring)), key=lambda i: off_fit[i])
                if off_fit[local_best_idx] < best_f:
                    best_f = off_fit[local_best_idx]
                    best = offspring[local_best_idx][:]
            history.append((evals, best_f))

            # (mu+lambda)-selection
            combined = population + offspring
            combined_fit = fitnesses + off_fit
            order = sorted(range(len(combined)), key=lambda i: combined_fit[i], reverse=self.maximize)
            population = [combined[i] for i in order[: self.params.mu]]
            fitnesses = [combined_fit[i] for i in order[: self.params.mu]]

        return GAResult(best, best_f, evals, generations, history, meta={"pm": pm})



def graph_fitness_wrapper(fid: int, iid: int = 1):
    
    if not _HAS_IOH:
        raise RuntimeError("IOHexperimenter package 'ioh' is not installed. Please 'pip install ioh'.")
    problem = get_problem(fid, instance=iid, problem_class=ProblemClass.GRAPH)
    
    maximize = True

    
    try:
        n = problem.meta_data.n_variables
    except Exception:
        
        n = getattr(problem, "n_variables", None)
        if n is None:
            raise RuntimeError("Unable to determine problem dimension for GRAPH problem.")

    def fitness(x: Bitstring) -> float:
        
        return problem(x)

    def make_logger(root: str, folder: str, algo_name: str):
        lg = ioh_logger.Analyzer(root=root, folder_name=folder, algorithm_name=algo_name, store_positions=False)
        problem.attach_logger(lg)
        return lg

    return n, fitness, problem, maximize, make_logger



def run_ex1_ga_graph(
    algo_name: str = "GA_uniform_1overN",
    fids = (2100, 2101, 2102, 2103, 2200, 2201, 2202, 2203, 2300, 2301, 2302),
    iid: int = 1,
    runs: int =30,     
    eval_budget: int = 10_000,            
    out_root: str = "Final/ex1_ga_logs",
    folder_prefix: str = "ex1_ga",
    mu: int = 20,
    lambd: int = 20,
    pc: float = 0.9,
    pm_mode: str = "1/n",
    tournament_k: int = 3,
):
    if not _HAS_IOH:
        raise RuntimeError("IOHexperimenter 'ioh' is not available. Please 'pip install ioh'.")

    os.makedirs(out_root, exist_ok=True)
    folder = f"{folder_prefix}-{algo_name}"

    summary_lines = []
    for fid in fids:
        
        n, fitness, problem, maximize, make_logger = graph_fitness_wrapper(fid, iid=iid)

        for run in range(1, runs + 1):
            seed = run

            
            lg = make_logger(out_root, folder, f"{algo_name}_F{fid}")

            
            problem.reset()

            
            params = GAParams(mu=mu, lambd=lambd, pc=pc, pm_mode=pm_mode, seed=seed, tournament_k=tournament_k)
            ga = GA(n=n, fitness=fitness, params=params, maximize=maximize)

            
            res = ga.run(eval_budget=10_000)

            problem.detach_logger()
            try:
                lg.close()
            except Exception:
                pass

            summary_lines.append(f"F{fid}, run={run}, n={n}, best_fitness={res.best_fitness}, evals={res.evaluations}, gens={res.generations}")

    
    summary_path = os.path.join(out_root, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write("n".join(summary_lines))
    print(f"Summary written to: {summary_path}")


def _demo_local_no_ioh():
    """If IOH isn't available, provide a quick internal smoke test on OneMax."""
    def onemax(x: Bitstring) -> int:
        return sum(x)

    n = 40
    params = GAParams(mu=20, lambd=20, pc=0.9, pm_mode="1/n", seed=1, tournament_k=3)
    ga = GA(n=n, fitness=onemax, params=params, maximize=True)
    res = ga.run(eval_budget=10_000)
    print("[Local Demo] Best f:", res.best_fitness, "after evals:", res.evaluations, "gens:", res.generations)



if __name__ == "__main__":
    if _HAS_IOH:
        
        run_ex1_ga_graph(
            algo_name="GA_uniform_1overN",
            runs=30,                   
            eval_budget=10_000,
            out_root="Final/ex1_ga_logs",
            folder_prefix="ex1_ga_graph",
            mu=20, lambd=20, pc=0.9, pm_mode="1/n", tournament_k=3,
        )
    else:
        print("[Warning] IOH not installed; running local smoke test only.")
        _demo_local_no_ioh()
