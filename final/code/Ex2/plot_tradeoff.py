import ioh
import matplotlib.pyplot as plt
from GSEMO import gsemo

def plot_tradeoff(problem_id, budget=10000, save_path=None):
    problem = ioh.get_problem(problem_id, problem_class=ioh.ProblemClass.GRAPH)
    problem.reset()

    pareto, log = gsemo(problem, budget=budget)

    f1_values = []
    for _, obj in pareto:
        f1_values.append(obj[0])

    f2_values = []
    for _, obj in pareto:
        f2_values.append(obj[1])


    plt.figure(figsize=(6, 5))
    plt.scatter(f2_values, f1_values, c="blue", marker="o", alpha=0.7)
    plt.xlabel("f2 = -solution (smaller set is better)")
    plt.ylabel("f1 = original objective (coverage/influence/packtravel)")
    plt.title(f"Trade-off Plot (Problem {problem_id})")

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Trade-off plot saved to {save_path}")
    else:
        plt.show()


if __name__ == "__main__":
    problem_ids = [2100, 2101, 2102, 2103,
                   2200, 2201, 2202, 2203,
                   2300, 2301, 2302]

    for pid in problem_ids:
        plot_tradeoff(pid, budget=10000, save_path=f"tradeoff_{pid}.png")