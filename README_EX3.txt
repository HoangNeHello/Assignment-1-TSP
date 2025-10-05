
Exercise 3 GA – quick-start
===========================
Files created:
- ex3_ga/ga.py : GA implementation with uniform crossover, bit-flip mutation, μ+λ elitist selection, tournament parent selection. IOH integration supported.
- ex3_ga/ex3_runner.py : Runs GA on F1, F2, F3, F18, F23, F24, F25 with n=100, 10 runs, 100,000-eval budget.

How to run (with IOHexperimenter):
1) pip install ioh
2) From the repo root, run:
   python ex3_ga/ex3_runner.py
3) Logs for IOHanalyzer will be in:
   final/doc/ex2_ex3_plots/ex3_ga-GA_uniform_1overN/

How to add the GA curve into your Exercise 2 plots:
- Upload the resulting folder to https://iohanalyzer.liacs.nl/ and select "Fixed budget" plots.
- Compare "GA_uniform_1overN" against your Random Search, RLS, (1+1) EA curves.

Parameter tuning tips (in ga.py -> GAParams):
- mu, lambd: try (20, 40) or (50, 50) for more exploration.
- pc: 0.7–1.0 usually works well.
- pm_mode: keep "1/n" for classic GA; try pm=0.005 if you use "const".
- tournament_k: 2–5; larger k increases selection pressure.

Budget semantics:
- The runner enforces a *fitness-evaluation* budget of 100,000 for fair comparison with Exercise 2.
- IOH will count evaluations via problem(x) calls; GA.fill offspring -> evaluates each child exactly once.

Local smoke test (without IOH):
   python -c "from ex3_ga.ga import GA, GAParams, onemax; print(GA(20,onemax,GAParams()).run(10000).best_fitness)"
