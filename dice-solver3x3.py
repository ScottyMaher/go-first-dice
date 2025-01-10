from itertools import combinations

def generate_matrices_6_to_3():
    """
    Generate all 3x3 matrices (represented as a list of length 9)
    that have exactly six +1 entries and three -1 entries.
    
    We'll store the matrix in row-major order:
      index 0 = (row=0, col=0)
      index 1 = (row=0, col=1)
      ...
      index 8 = (row=2, col=2)
    """
    all_indices = range(9)
    # Choose which 6 positions will be +1, the remaining 3 will be -1.
    for plus_ones_positions in combinations(all_indices, 5):
        # Create a list of length 9, default -1
        matrix = [-1]*9
        for pos in plus_ones_positions:
            matrix[pos] = 1
        yield matrix


def matrix_entry(matrix, r, c):
    """
    Helper to access the entry of a 3x3 list 'matrix' in row r, col c.
    matrix is stored in row-major form, so index = r*3 + c.
    """
    return matrix[r*3 + c]


def has_forbidden_3_cycle(M_AB, M_BC, M_CA):
    """
    Check if the given trio of 3x3 matrices (each stored in a length-9 list)
    produces a forbidden 3-cycle. A forbidden 3-cycle means:
      - For some (i, j, k) in {0,1,2}^3, the sum of
        [M_AB[i,j], M_BC[j,k], M_CA[k,i]] = 3 or -3
      - i.e. they are all +1 or all -1.
    
    Return True if there *is* a forbidden 3-cycle, otherwise False.
    """
    for i in range(3):      # i indexes A
        for j in range(3):  # j indexes B
            for k in range(3):  # k indexes C
                val_ab = matrix_entry(M_AB, i, j)
                val_bc = matrix_entry(M_BC, j, k)
                val_ca = matrix_entry(M_CA, k, i)
                cycle_sum = val_ab + val_bc + val_ca
                if cycle_sum == 3 or cycle_sum == -3:
                    # Found a forbidden 3-cycle
                    return True
    return False


def print_matrix(m):
    """
    Print a 3x3 matrix (stored in a 9-element list) in a more readable format.
    """
    for r in range(3):
        row_vals = [matrix_entry(m, r, c) for c in range(3)]
        print(row_vals)
    print()


def count_orderings(M_AB, M_BC, M_CA):
    """
    Given three flattened 3x3 matrices M_AB, M_BC, M_CA,
    return a dictionary showing how many of the 27 possible
    (i, j, k) triples produce each of the 6 orderings:
      - "A>B>C"
      - "A>C>B"
      - "B>A>C"
      - "B>C>A"
      - "C>A>B"
      - "C>B>A"
    """
    
    # Initialize a dictionary to hold the count of each ordering.
    ordering_counts = {
        "A>B>C": 0,
        "A>C>B": 0,
        "B>A>C": 0,
        "B>C>A": 0,
        "C>A>B": 0,
        "C>B>A": 0,
    }
    
    # Enumerate all triples (i, j, k) in {0,1,2}^3.
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # Tally wins for each of A, B, C in this triple.
                wins = {"A": 0, "B": 0, "C": 0}
                
                # A_i vs B_j
                if matrix_entry(M_AB, i, j) == 1:
                    wins["A"] += 1
                else:
                    wins["B"] += 1
                
                # B_j vs C_k
                if matrix_entry(M_BC, j, k) == 1:
                    wins["B"] += 1
                else:
                    wins["C"] += 1
                
                # C_k vs A_i
                if matrix_entry(M_CA, k, i) == 1:
                    wins["C"] += 1
                else:
                    wins["A"] += 1
                
                # Figure out first/second/third place
                # We expect the wins distribution to be (2,1,0) with no ties
                # (assuming no 3-cycles).
                sorted_results = sorted(
                    [(wins["A"], "A"), (wins["B"], "B"), (wins["C"], "C")],
                    key=lambda x: x[0],
                    reverse=True
                )
                
                # The ordering is like "X>Y>Z"
                first = sorted_results[0][1]
                second = sorted_results[1][1]
                third = sorted_results[2][1]
                ordering_str = f"{first}>{second}>{third}"
                
                ordering_counts[ordering_str] += 1
    
    return ordering_counts


def main():
    # Step 1: Generate all valid 3x3 matrices (six +1, three -1).
    matrices_AB = list(generate_matrices_6_to_3())
    matrices_BC = list(generate_matrices_6_to_3())
    matrices_CA = list(generate_matrices_6_to_3())

    solutions_checked = 0
    solutions_found = 0
    valid_solutions = []

    # Step 2: Iterate through all combinations of M_AB, M_BC, M_CA
    for M_AB in matrices_AB:
        for M_BC in matrices_BC:
            for M_CA in matrices_CA:
                # Step 3: Check the 3-cycle condition
                solutions_checked += 1
                if not has_forbidden_3_cycle(M_AB, M_BC, M_CA):
                    # We found a valid configuration
                    solutions_found += 1
                    print(f"Solution #{solutions_found}")
                    print("M_AB:")
                    print_matrix(M_AB)
                    print("M_BC:")
                    print_matrix(M_BC)
                    print("M_CA:")
                    print_matrix(M_CA)
                    print("Orderings:")
                    ordering_counts = count_orderings(M_AB, M_BC, M_CA)
                    for ordering, count in ordering_counts.items():
                        print(f"  {ordering}: {count}")
                    orderings_set = set(ordering_counts.values())
                    print("Unique orderings:", orderings_set)
                    if len(orderings_set) <= 2:
                        valid_solutions.append(orderings_set)
                    print("="*40)
    
    print(f"Total solutions checked: {solutions_checked}")
    print(f"Total valid solutions found: {solutions_found}")
    print(f"Total valid solutions with 2 unique orderings: {valid_solutions}")


if __name__ == "__main__":
    main()
