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

def inversion_mutation(tour: list[int]) -> list[int]:
    #Inversed mutation: reverse a segment of the tour.
    if len(tour) < 3:
        return tour
    i, j = sorted(random.sample(range(len(tour)), 2))
    tour[i:j+1] = reversed(tour[i:j+1])
    return tour

### Crossovers operations


def ordered_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
# # Ordered Crossover: Create a child by preserving the order of nodes from both parents.
#     size = len(parent1)
#     start, end = sorted(random.sample(range(size), 2))
#     child = [None] * size
#     # Fill the child with the segment from parent1
#     child[start:end+1] = parent1[start:end+1]
#     # Fill the remaining positions with nodes from parent2, preserving order
#     p2_filtered = [node for node in parent2 if node not in child]
#     p2_index = 0
#     for i in range(size):
#         if child[i] is None:
#             while p2_index < len(p2_filtered) and (i < start or i > end):
#                 child[i] = p2_filtered[p2_index]
#                 p2_index += 1
#     return child
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n

    # copy slice from parent1
    child[a:b+1] = parent1[a:b+1]

    # iterate parent2 in order, placing items not yet in child
    remaining = (x for x in parent2 if x not in child)

    idx = (b + 1) % n
    for x in remaining:
        # advance until we find an empty slot (wrap around)
        while child[idx] is not None:
            idx = (idx + 1) % n
        child[idx] = x
        idx = (idx + 1) % n

    return child


def pmx_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    # # Partially Mapped Crossover (PMX): Create a child by mapping segments from both parents.
    # size = len(parent1)
    # start, end = sorted(random.sample(range(size), 2))
    # child = [None] * size
    # child[start:end+1] = parent1[start:end+1]
    # # Copy the segment from parent1
    # for i in range(start, end + 1):
    #     child[i] = parent1[i]
    
    # # Fill the remaining positions with nodes from parent2, using mapping
    # for i in range(size):
    #     if child[i] is None:
    #         node = parent2[i]
    #         while node in child:
    #             node = parent1[child.index(node)]
    #         child[i] = node
    # return child
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n

    # 1) copy slice from p1
    child[a:b+1] = parent1[a:b+1]

    # 2) build mapping from the slice: p1 -> p2
    #    (when a candidate is already present in the child because it's in p1-slice,
    #     we map it to its counterpart from p2 until it lands outside the slice)
    m_inv = {parent1[i]: parent2[i] for i in range(a, b+1)}
    slice_vals = set(parent1[a:b+1])

    # 3) fill remaining positions using p2, resolving conflicts via mapping chain
    for i in list(range(0, a)) + list(range(b+1, n)):
        x = parent2[i]
        while x in slice_vals:
            x = m_inv[x]        # follow mapping out of the slice
        child[i] = x

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
    n = len(parent1)

    # Build adjacency tables from BOTH parents
    def adj_from(p):
        A = {v: set() for v in p}
        for i, v in enumerate(p):
            A[v].add(p[(i - 1) % n])
            A[v].add(p[(i + 1) % n])
        return A

    adj1 = adj_from(parent1)
    adj2 = adj_from(parent2)

    # unified neighbor table we will shrink as we go
    neighbors = {v: (adj1[v] | adj2[v]).copy() for v in parent1}

    child = []
    unvisited = set(parent1)
    current = random.choice(parent1)

    while len(child) < n:
        child.append(current)
        unvisited.remove(current)

        # remove current from all adjacency lists
        for s in neighbors.values():
            s.discard(current)

        # candidates are neighbors of current that we haven't used yet
        cand = [v for v in neighbors[current] if v in unvisited]

        if cand:
            # 1) prefer common edges (present in BOTH parents)
            common = [v for v in cand if v in adj1[current] and v in adj2[current]]
            if common:
                next_city = random.choice(common)
            else:
                # 2) otherwise pick one with the SHORTEST adjacency list
                m = min(len(neighbors[v]) for v in cand)
                best = [v for v in cand if len(neighbors[v]) == m]
                next_city = random.choice(best)
        else:
            # 3) empty list → pick any unvisited city at random
            if not unvisited:
                break
            next_city = random.choice(list(unvisited))

        current = next_city

    return child

# alias to match algorithms.py
reserved_mutation = inversion_mutation
