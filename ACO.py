import random

def onemax(bitstring):
    return sum(bitstring)

class ACO:
    def __init__(self, n=100, num_ants=10, r=0.1, q=1.0, max_iter=100000, alpha=1.0, beta=1.0):
        '''
        n is the length of the bit string, 
        num_ants is the number of ants, 
        r is the evaporation rate, 
        q is the pheromone gain factor, 
        max_iter is the maximum number of iterations, 
        alpha: influence of pheromone,
        beta: influence of heuristic,
        pheromone is the initial value of each position pheromone (set to 1.0)
        '''
        self.n = n
        self.num_ants = num_ants
        self.r = r
        self.q = q
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.pheromone = [0.5] * n
        self.best_solution = None
        self.best_fitness = float("-inf")

    def solution(self):
        solution = []
        for i in range(self.n):
            phe = self.pheromone[i] ** self.alpha
            heu = 1.0 ** self.beta
            p = phe / (phe + heu)

            ran = random.random()
            if ran < p:
                bit = 1
            else:
                bit = 0
            solution.append(bit)
        return solution
    
    def update_pheromones(self, solutions, fitnesses):
        for i in range(self.n):
            self.pheromone[i] *= (1 - self.r)

        for sol, fit in zip(solutions, fitnesses):
            for i, bit in enumerate(sol):
                if bit == 1:
                    self.pheromone[i] += self.q * fit / self.n

    def run(self, fitness_function):
        best_curve = []
        for i in range(1, self.max_iter + 1):
            solutions, fitnesses = [], []
            for j in range(self.num_ants):
                s = self.solution()
                f = fitness_function(s)
                solutions.append(s)
                fitnesses.append(f)
                if f > self.best_fitness:
                    self.best_fitness = f
                    self.best_solution = s[:]

            self.update_pheromones(solutions, fitnesses)
            best_curve.append(self.best_fitness)

        return self.best_solution, self.best_fitness, best_curve
