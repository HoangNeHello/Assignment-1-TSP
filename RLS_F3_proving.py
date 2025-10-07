from RLS import RLS

# Define fitness function
def f3_harmonic_weights(bitstring):
    """F3: Linear function with harmonic weights"""
    return sum((i+1) * bit for i, bit in enumerate(bitstring))

# run RLS
n = 100
rls = RLS(n, f3_harmonic_weights)
solution, fitness = rls.run(max_iterations=10000)

print(f"Solution: {solution}")
print(f"Fitness: {fitness}")
print(f"Optimum: {n * (n + 1) // 2}")

"""The result show that, once all bits are set to 1, we've reached the global optimum x* = (1,1,...,1).
Solution: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Fitness: 5050
Optimum: 5050

RLS will never accept backward moves as any single-bit flip (1 to 0) 
strictly reduces fitness once all bits are 1. 
The algorithm remains in its optimal state.

Since E[T] = O(n log n),
P[T = O(n log n)] ≥ constant > 0
Therefore, the probability = Ω(1) 
"""
