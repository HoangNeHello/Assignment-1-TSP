"""
Implementation of the RLS Algorithm as defined in the Week 3 Lecture
"""

import random 

class RLS:
    def __init__(self, n, fitness_function):
        """
        n: length of the bitstring
        fitness_function: function f(s) that evaluates a bitstring
        """
        self.n = n
        self.fitness_function = fitness_function

    def run(self, max_iterations=None):
      
        current_solution = [random.choice([0, 1]) for _ in range(self.n)]
        current_fitness = self.fitness_function(current_solution)

        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            iteration = iteration + 1

            i = random.randint(0, self.n - 1)
            neighbor = current_solution[:]
            neighbor[i] = 1 - neighbor[i]

            neighbor_fitness = self.fitness_function(neighbor)

            if neighbor_fitness >= current_fitness:
                current_solution = neighbor
                current_fitness = neighbor_fitness

        return current_solution, current_fitness

        
    pass