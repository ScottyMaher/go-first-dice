import random

# ----------------------------------------------------------
# Hardcode the matrices from the specified solution.
# Each matrix is stored as a flat list of length 9 in row-major order.
# For example, M_AB[r,c] = M_AB_flat[r*3 + c].
# ----------------------------------------------------------

M_AB_flat = [
    -1, -1, -1,
    -1,  1,  1,
     1,  1,  1
]

M_BC_flat = [
    -1,  1,  1,
    -1, -1,  1,
    -1,  1,  1
]

M_CA_flat = [
     1,  1,  1,
     1, -1, -1,
     1, -1, -1
]

def M_AB(i, j):
    """Return the sign (+1 or -1) for A_i vs B_j."""
    return M_AB_flat[i*3 + j]

def M_BC(j, k):
    """Return the sign (+1 or -1) for B_j vs C_k."""
    return M_BC_flat[j*3 + k]

def M_CA(k, i):
    """Return the sign (+1 or -1) for C_k vs A_i."""
    return M_CA_flat[k*3 + i]


def simulate_round():
    """
    Randomly pick i, j, k in {0,1,2}, then determine
    who is 1st, 2nd, 3rd among A_i, B_j, C_k.
    
    Returns a tuple (winner_layer, ordering_string),
    where ordering_string is one of:
      'A>B>C', 'A>C>B', 'B>A>C', 'B>C>A', 'C>A>B', 'C>B>A'.
    """
    i = random.randint(0, 2)
    j = random.randint(0, 2)
    k = random.randint(0, 2)
    
    # Track wins for each of the three "contestants" in this round
    # We'll label them as "A", "B", "C" so we know the layer only.
    wins = {"A": 0, "B": 0, "C": 0}
    
    # A_i vs B_j
    if M_AB(i, j) == 1:
        wins["A"] += 1
    else:
        wins["B"] += 1
    
    # B_j vs C_k
    if M_BC(j, k) == 1:
        wins["B"] += 1
    else:
        wins["C"] += 1
    
    # C_k vs A_i
    if M_CA(k, i) == 1:
        wins["C"] += 1
    else:
        wins["A"] += 1
    
    # Now figure out the 1st, 2nd, 3rd place by who got 2 wins, 1 win, or 0.
    # Because there's no 3-cycle, we should have a clean 2-1-0 distribution.
    # Let's invert the dict into a list of (wins, layer) pairs, then sort.
    # More wins => higher in the ordering.
    results = [(wins["A"], "A"), (wins["B"], "B"), (wins["C"], "C")]
    results.sort(reverse=True, key=lambda x: x[0])  # sort by # of wins descending

    # results[0] is the winner (2 wins), results[1] second place, results[2] third.
    winner = results[0][1]
    second = results[1][1]
    third = results[2][1]
    
    return winner, second, third


def main():
    num_rounds = 100_000  # change this as desired
    layer_win_count = {
        "A first": 0, "A second": 0, "A third": 0,
        "B first": 0, "B second": 0, "B third": 0,
        "C first": 0, "C second": 0, "C third": 0
    }
    
    # Possible permutations among A,B,C
    orderings = [
        "A>B>C", "A>C>B",
        "B>A>C", "B>C>A",
        "C>A>B", "C>B>A"
    ]
    ordering_count = {o: 0 for o in orderings}

    pairings = [
        "A>B", "A>C", "B>A", "B>C", "C>A", "C>B"
    ]
    pairing_count = {p: 0 for p in pairings}
    
    # Run the random simulation
    for _ in range(num_rounds):
        winner, second, third = simulate_round()
        
        ordering = f"{winner}>{second}>{third}"
        ordering_count[ordering] += 1
        
        layer_win_count[f"{winner} first"] += 1
        layer_win_count[f"{second} second"] += 1
        layer_win_count[f"{third} third"] += 1

    # Count the pairings
    for ordering in orderings:
        winner, second, third = ordering.split(">")
        pairing_count[f"{winner}>{second}"] += ordering_count[ordering]
        pairing_count[f"{second}>{third}"] += ordering_count[ordering]
        pairing_count[f"{winner}>{third}"] += ordering_count[ordering]
    
    # Print results
    print(f"After {num_rounds} rounds:")
    print("Layer win counts:")
    for layer in ["A", "B", "C"]:
        first_key = f"{layer} first"
        second_key = f"{layer} second"
        third_key = f"{layer} third"
        print(f"  {first_key}: {layer_win_count[first_key]}, {second_key}: {layer_win_count[second_key]}, {third_key}: {layer_win_count[third_key]}")
    
    print("\nPairing frequencies:")
    for p in pairings:
        print(f"  {p}: {pairing_count[p]}")
    
    print("\nOrdering frequencies:")
    for o in orderings:
        print(f"  {o}: {ordering_count[o]}")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
