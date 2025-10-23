import ioh
import csv
from GSEMO import gsemo

def run_experiments(problem_ids, budget=10000, runs=30, out_file="results.csv"):
    results = []

    for pid in problem_ids:
        problem = ioh.get_problem(pid, problem_class=ioh.ProblemClass.GRAPH)

        for r in range(runs):
            iohgsemolog = ioh.logger.Analyzer(
                root="data",
                folder_name="GSEMO_run",
                algorithm_name="GSEMO",
                algorithm_info=f"run_{r}"
            )
            problem.attach_logger(iohgsemolog)

            problem.reset()
            _, log_gsemo = gsemo(problem, budget)

            for evals, best in log_gsemo:
                results.append([pid, r, "GSEMO", evals, best])

            problem.detach_logger()
            del iohgsemolog

        print(f"complete Problem {pid} 's {runs} times run")

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["problem_id", "run", "algorithm", "evaluations", "best_f1"])
        writer.writerows(results)

    print(f"all data save in to {out_file}")


if __name__ == "__main__":
    problem_ids = [2100, 2101, 2102, 2103,
                    2200, 2201, 2202, 2203,
                    2300, 2301, 2302]

run_experiments(problem_ids, budget=10000, runs=30, out_file="E2_results.csv")