from Uniform_Crossover_GA import run_ex3_ga_with_ioh

if __name__ == "__main__":
   
    run_ex3_ga_with_ioh(
        algo_name="GA_uniform_1overN",
        fids=(1, 2, 3, 18, 23, 24, 25),
        n=100,
        iid=1,
        runs=10,
        eval_budget=100_000,
        out_root="final/doc/ex2_ex3_plots",
        folder_prefix="ex3_ga"
    )