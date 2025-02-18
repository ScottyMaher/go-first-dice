from copy import deepcopy

def solve_all():
    """
    Enumerate *all* valid assignments of directions to edges between A-B, B-C, and A-C,
    satisfying:
      1) Exactly one direction for each cross-layer pair.
      2) Each layer has exactly 9 outgoing edges total.
      3) No 3-cycle of length 3 that returns to the same vertex.
    
    Returns:
        A list of all solutions, where each solution is a tuple (AB, BC, AC).
        - AB[i][j] = True means A_i -> B_j, False means B_j -> A_i
        - BC[j][k] = True means B_j -> C_k, False means C_k -> B_j
        - AC[i][k] = True means A_i -> C_k, False means C_k -> A_i
    """
    # 1. Prepare a list of all cross-layer edges (27 in total).
    edges = []
    # A-B
    for i in range(3):
        for j in range(3):
            edges.append(("AB", i, j))
    # B-C
    for j in range(3):
        for k in range(3):
            edges.append(("BC", j, k))
    # A-C
    for i in range(3):
        for k in range(3):
            edges.append(("AC", i, k))
    
    # 2. Data structures for orientation.
    # None = undecided, True = "forward" as indicated, False = "reverse".
    AB = [[None]*3 for _ in range(3)]
    BC = [[None]*3 for _ in range(3)]
    AC = [[None]*3 for _ in range(3)]

    # Track out-degree for each vertex individually.
    outA = [0]*3
    outB = [0]*3
    outC = [0]*3

    # Track total out-degree per layer (must end up at 9).
    totalOutA = 0
    totalOutB = 0
    totalOutC = 0

    all_solutions = []

    def no_3_cycle(AB, BC, AC):
        """
        Check no directed 3-cycle among A_i, B_j, C_k:
          - A_i -> B_j -> C_k -> A_i
          - A_i -> C_k -> B_j -> A_i
        """
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # A_i -> B_j -> C_k -> A_i
                    if AB[i][j] and BC[j][k] and (AC[i][k] == False):
                        return False
                    # A_i -> C_k -> B_j -> A_i
                    if AC[i][k] and (BC[j][k] == False) and (AB[i][j] == False):
                        return False
        return True

    def backtrack(index, 
                  AB, BC, AC,
                  outA, outB, outC,
                  totalOutA, totalOutB, totalOutC):
        """
        Explore both possible directions for edge #index, then recurse.
        If all 27 edges have been assigned, check constraints and record solution if valid.
        """
        # If we assigned all 27 edges, check final constraints:
        if index == len(edges):
            # Must have exactly 9 outgoing edges per layer
            if (totalOutA == 9) and (totalOutB == 9) and (totalOutC == 9):
                # Check no 3-cycle
                if no_3_cycle(AB, BC, AC):
                    # Deep-copy the current orientation into our global list
                    sol_AB = deepcopy(AB)
                    sol_BC = deepcopy(BC)
                    sol_AC = deepcopy(AC)
                    all_solutions.append((sol_AB, sol_BC, sol_AC))
            return  # Continue searching for more solutions
        
        layer_pair, x, y = edges[index]

        if layer_pair == "AB":
            # Two choices: A_x -> B_y (True) or B_y -> A_x (False)

            # Choice 1: A_x -> B_y
            AB[x][y] = True
            outA[x] += 1
            newTotalOutA = totalOutA + 1

            # Prune if out-degree constraints are clearly broken
            if outA[x] <= 6 and newTotalOutA <= 9:
                backtrack(index + 1,
                          AB, BC, AC,
                          outA, outB, outC,
                          newTotalOutA, totalOutB, totalOutC)

            # Revert
            AB[x][y] = None
            outA[x] -= 1

            # Choice 2: B_y -> A_x
            AB[x][y] = False
            outB[y] += 1
            newTotalOutB = totalOutB + 1

            if outB[y] <= 6 and newTotalOutB <= 9:
                backtrack(index + 1,
                          AB, BC, AC,
                          outA, outB, outC,
                          totalOutA, newTotalOutB, totalOutC)

            # Revert
            AB[x][y] = None
            outB[y] -= 1

        elif layer_pair == "BC":
            # Two choices: B_x -> C_y (True) or C_y -> B_x (False)

            # Choice 1: B_x -> C_y
            BC[x][y] = True
            outB[x] += 1
            newTotalOutB = totalOutB + 1

            if outB[x] <= 6 and newTotalOutB <= 9:
                backtrack(index + 1,
                          AB, BC, AC,
                          outA, outB, outC,
                          totalOutA, newTotalOutB, totalOutC)

            # Revert
            BC[x][y] = None
            outB[x] -= 1

            # Choice 2: C_y -> B_x
            BC[x][y] = False
            outC[y] += 1
            newTotalOutC = totalOutC + 1

            if outC[y] <= 6 and newTotalOutC <= 9:
                backtrack(index + 1,
                          AB, BC, AC,
                          outA, outB, outC,
                          totalOutA, totalOutB, newTotalOutC)

            # Revert
            BC[x][y] = None
            outC[y] -= 1

        else:  # layer_pair == "AC"
            # Two choices: A_x -> C_y or C_y -> A_x

            # Choice 1: A_x -> C_y
            AC[x][y] = True
            outA[x] += 1
            newTotalOutA = totalOutA + 1

            if outA[x] <= 6 and newTotalOutA <= 9:
                backtrack(index + 1,
                          AB, BC, AC,
                          outA, outB, outC,
                          newTotalOutA, totalOutB, totalOutC)

            # Revert
            AC[x][y] = None
            outA[x] -= 1

            # Choice 2: C_y -> A_x
            AC[x][y] = False
            outC[y] += 1
            newTotalOutC = totalOutC + 1

            if outC[y] <= 6 and newTotalOutC <= 9:
                backtrack(index + 1,
                          AB, BC, AC,
                          outA, outB, outC,
                          totalOutA, totalOutB, newTotalOutC)

            # Revert
            AC[x][y] = None
            outC[y] -= 1

    # Start the recursion at edge 0
    backtrack(index=0,
              AB=AB, BC=BC, AC=AC,
              outA=outA, outB=outB, outC=outC,
              totalOutA=totalOutA, totalOutB=totalOutB, totalOutC=totalOutC)

    return all_solutions


if __name__ == "__main__":
    solutions = solve_all()
    print(f"Number of valid solutions found: {len(solutions)}")
    
    # If you want to print each solution, be mindful it could be very large!
    # Example of printing the first solution if it exists:
    if solutions:
        print("\nFirst solution (AB, BC, AC):")
        AB, BC, AC = solutions[0]
        print("AB (True = A->B, False = B->A):")
        for row in AB:
            print(row)
        print("\nBC (True = B->C, False = C->B):")
        for row in BC:
            print(row)
        print("\nAC (True = A->C, False = C->A):")
        for row in AC:
            print(row)
