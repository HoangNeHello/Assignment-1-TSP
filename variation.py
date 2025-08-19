import TSP
import random

def insert_mutation(tour: list[int]) -> list[int]:
    #Insert mutation: randomly insert a node into a new position.
    if len(tour) < 2:
        return tour
    i, j = random.sample(range(len(tour)), 2)
    node = tour.pop(i)
    tour.insert(j, node)
    return tour


def swap_mutation(tour: list[int]) -> list[int]:
    #Swap mutation: randomly swap two nodes in the tour.
    if len(tour) < 2:
        return tour
    i, j = random.sample(range(len(tour)), 2)
    tour[i], tour[j] = tour[j], tour[i]
    return tour

def reserved_mutation(tour: list[int]) -> list[int]:
    #Reserved mutation: reverse a segment of the tour.
    if len(tour) < 3:
        return tour
    i, j = sorted(random.sample(range(len(tour)), 2))
    tour[i:j+1] = reversed(tour[i:j+1])
    return tour

### Crossovers operations


def ordered_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
# Ordered Crossover: Create a child by preserving the order of nodes from both parents.
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    # Fill the child with the segment from parent1
    child[start:end+1] = parent1[start:end+1]
    # Fill the remaining positions with nodes from parent2, preserving order
    p2_filtered = [node for node in parent2 if node not in child]
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while p2_index < len(p2_filtered) and (i < start or i > end):
                child[i] = p2_filtered[p2_index]
                p2_index += 1
    return child


def pmx_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    # Partially Mapped Crossover (PMX): Create a child by mapping segments from both parents.
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end+1] = parent1[start:end+1]
    # Copy the segment from parent1
    for i in range(start, end + 1):
        child[i] = parent1[i]
    
    # Fill the remaining positions with nodes from parent2, using mapping
    for i in range(size):
        if child[i] is None:
            node = parent2[i]
            while node in child:
                node = parent1[child.index(node)]
            child[i] = node
    return child


def cycle_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    # Cycle Crossover : Create a child by following cycles in the parents.
    size = len(parent1)
    child = [None] * size
    cycle = [False] * size
    cycles = set()
    index = 0
    take_from_parent1 = True

    while None in child:
        if index in cycles:
            index = child.index(None)
            take_from_parent1 = not take_from_parent1

        start = index
        while index not in cycles:
            cycles.add(index)
            child[index] = parent1[index] if take_from_parent1 else parent2[index]
            index = parent1.index(parent2[index])
    return child

def edge_recombination_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    # Edge recombination crossover: Create a child by preserving edges from both parents.

    #build edge map
    edge_map = {}
    for i in range(len(parent1)):
        city = parent1[i]
        left = parent1[i-1]
        right = parent1[(i+1) % len(parent1)]
        edge_map.setdefault(city, set()).update([left, right])

    current = random.choice(parent1)
    child = [current]
    while len(child) < len(parent1):
        for e in edge_map.values():
            if current in e:
                e.remove(current)
        neighbors = edge_map[current]   
        if not neighbors:
            break   
        next_city = min(neighbors, key=lambda x: (parent2.index(x) if x in parent2 else float('inf')))
        child.append(next_city)
        current = next_city
    return child + [city for city in parent1 if city not in child]