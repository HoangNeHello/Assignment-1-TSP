Exercise 2

This project implements and evaluates the GSEMO (Generalised Simple Evolutionary Multi-Objective Optimizer) algorithm for submodular optimisation tasks using IOHprofiler.
The focus of this exercise is to analyse the performance of GSEMO on three classes of problems:

MaxCoverage (F2100–F2103)

MaxInfluence (F2200–F2203)

PackWhileTravel (F2300–F2302)

Each instance is tested 30 times with a budget of 10,000 fitness evaluations

File Structure:

GSEMO.py
Implementation of the GSEMO algorithm with evaluation and mutation logic.

MOF.py
utility functions for GSEMO, include evaluate(), mutate(), dominates(). evaluate() is multi-objective formulation.

E2_results.csv
Raw experimental data file recording the best fitness values across evaluations and runs.

run.py
The main experimental script for running GSEMO on all problem instances and saving the results to the ioh log.

EX2_GSEMO_logs/
This folder contains the ioh logs of GSEMO on all problem instances.

EX2_GSEMO_plot/
This folder contains the trade-off plots for each instance of the GSEMO algorithm, visualising Pareto fronts and convergence trends.

analysis.txt
This document analyzes the performance of GSEMO on different problem instances and its comparison with Exercise 1.

README.md
Documentation file (this one).