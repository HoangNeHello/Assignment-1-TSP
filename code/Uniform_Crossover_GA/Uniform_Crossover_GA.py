
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Optional

try:
    import ioh
    from ioh import get_problem, ProblemClass, logger as ioh_logger
    _HAS_IOH = True
except Exception:
    _HAS_IOH = False


Bitstring = List[int]


def uniform_crossover(p1: Bitstring, p2: Bitstring, rng: random.Random) -> Bitstring:
    """Uniform crossover: each bit chosen from p1 or p2 with p=0.5."""
    n = len(p1)
    return [p1[i] if rng.random() < 0.5 else p2[i] for i in range(n)]


def bitflip_mutation(x: Bitstring, pm: float, rng: random.Random) -> Bitstring:
    """Bit-flip mutation with per-bit rate pm."""
    n = len(x)
    y = x[:]
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
        assert params.mu >= 10, "mu must be at least 10"
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

    def run(self, eval_budget: int = 100_000) -> GAResult:
        pm = self._mutation_rate()
       
        population = [random_bitstring(self.n, self.rng) for _ in range(self.params.mu)]
        fitnesses = [self.fitness_fn(ind) for ind in population]
        evals = len(population)
        best_idx = max(range(len(population)), key=lambda i: fitnesses[i]) if self.maximize else \
                   min(range(len(population)), key=lambda i: fitnesses[i])
        best = population[best_idx][:]
        best_f = fitnesses[best_idx]
        history: List[Tuple[int, float]] = [(evals, best_f)]
        generations = 0

        while evals < eval_budget:
            generations += 1

            
            offspring: List[Bitstring] = []
            while len(offspring) < self.params.lambd:
                p1, p2 = self._select_parents(population, fitnesses)
                child = uniform_crossover(p1, p2, self.rng) if self.rng.random() < self.params.pc else p1[:]
                child = bitflip_mutation(child, pm, self.rng)
                offspring.append(child)

            
            off_fit = [self.fitness_fn(ind) for ind in offspring]
            evals += len(offspring)

            
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

           
            combined = population + offspring
            combined_fit = fitnesses + off_fit
            
            order = sorted(range(len(combined)), key=lambda i: combined_fit[i], reverse=self.maximize)
           
            population = [combined[i] for i in order[: self.params.mu]]
            fitnesses = [combined_fit[i] for i in order[: self.params.mu]]

        return GAResult(best, best_f, evals, generations, history, meta={"pm": pm})



def ioh_fitness_wrapper(fid: int, n: int, iid: int = 1):
    """
    Returns (fitness_function, ioh_problem, logger_factory)
    - fitness_function(bitstring) calls problem.evaluate()
    - logger_factory(out_root, algo_name) -> attached logger
    """
    assert _HAS_IOH, "ioh is not installed"
    problem = get_problem(fid, iid, n, ProblemClass.PBO)  
    maximize = True 

    def fitness(x: Bitstring) -> float:
        
        return problem(x)

    def make_logger(root: str, folder: str, algo_name: str):
        lg = ioh_logger.Analyzer(root=root, folder_name=folder, algorithm_name=algo_name, store_positions=False)
        problem.attach_logger(lg)
        return lg

    return fitness, problem, maximize, make_logger


def run_ex3_ga_with_ioh(
    algo_name: str = "GA_uniform_1overN",
    fids = (1, 2, 3, 18, 23, 24, 25),
    n: int = 100,
    iid: int = 1,
    runs: int = 10,
    eval_budget: int = 100_000,
    out_root: str = "final/doc/ex2_ex3_plots",
    folder_prefix: str = "ex3_ga"
):
    """
    Run GA on the specified PBO functions with IOHexperimenter logging.
    Produces IOHanalyzer-compatible files under out_root/folder_prefix-<algo_name>.
    """
    if not _HAS_IOH:
        raise RuntimeError("IOHexperimenter 'ioh' is not available. Please `pip install ioh`.")

    folder = f"{folder_prefix}-{algo_name}"
    for fid in fids:
        
        fitness, problem, maximize, make_logger = ioh_fitness_wrapper(fid, n, iid=iid)

        for run in range(1, runs + 1):
            seed = run
            lg = make_logger(out_root, folder, f"{algo_name}_F{fid}")
           
            problem.reset()

            
            params = GAParams(mu=20, lambd=20, pc=0.9, pm_mode="1/n", seed=seed, tournament_k=3)
            ga = GA(n=n, fitness=fitness, params=params, maximize=maximize)
            
            _ = ga.run(eval_budget=eval_budget)

            
            problem.detach_logger()
            try:
                lg.close()  
            except Exception:
                pass



def onemax(x: Bitstring) -> int:
    return sum(x)


def _demo_local():
    n = 20
    params = GAParams(mu=20, lambd=20, pc=0.9, pm_mode="1/n", seed=1, tournament_k=3)
    ga = GA(n=n, fitness=onemax, params=params, maximize=True)
    res = ga.run(eval_budget=10_000)
    print("Best f:", res.best_fitness, "after evals:", res.evaluations, "gens:", res.generations)


if __name__ == "__main__":
   
    _demo_local()