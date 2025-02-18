import sys

num_vertices_per_layer = 6

A_vertices = [f"A{i}" for i in range(1, num_vertices_per_layer + 1)]
B_vertices = [f"B{i}" for i in range(1, num_vertices_per_layer + 1)]
C_vertices = [f"C{i}" for i in range(1, num_vertices_per_layer + 1)]

AB_pairs = [(a, b) for a in A_vertices for b in B_vertices]
BC_pairs = [(b, c) for b in B_vertices for c in C_vertices]
AC_pairs = [(a, c) for a in A_vertices for c in C_vertices]
all_pairs = AB_pairs + BC_pairs + AC_pairs

edge_dir = {}
solutions = []

def forms_3_cycle(v1, v2):
    """Check if assigning v1->v2 created a 3-cycle among the three layers."""
    layer1, layer2 = v1[0], v2[0]
    all_layers = {"A", "B", "C"}
    layer3 = list(all_layers - {layer1, layer2})
    if len(layer3) != 1:
        return False
    layer3 = layer3[0]
    if layer3 == "A":
        third_vertices = A_vertices
    elif layer3 == "B":
        third_vertices = B_vertices
    else:
        third_vertices = C_vertices
    
    # Check potential v3 in that third layer
    for v3 in third_vertices:
        # Check if v1->v2->v3->v1 forms a cycle
        if (v2, v3) in edge_dir and edge_dir[(v2, v3)] == +1:
            if (v3, v1) in edge_dir and edge_dir[(v3, v1)] == +1:
                return True
        # Check the opposite direction, or other permutations as needed
        # (Depending on how thoroughly you want to catch all 3-cycles)
    return False

def check_condition_3():
    """Verify each layer gets 1st, 2nd, 3rd exactly n^3/3 times."""
    required_count = (num_vertices_per_layer**3)//3
    position_counts = {
        "A": {1: 0, 2: 0, 3: 0},
        "B": {1: 0, 2: 0, 3: 0},
        "C": {1: 0, 2: 0, 3: 0}
    }
    for A_v in A_vertices:
        for B_v in B_vertices:
            for C_v in C_vertices:
                # Count pairwise wins:
                wins = {A_v: 0, B_v: 0, C_v: 0}
                # A vs B
                if edge_dir.get((A_v, B_v)) == 1:
                    wins[A_v] += 1
                else:
                    wins[B_v] += 1
                # B vs C
                if edge_dir.get((B_v, C_v)) == 1:
                    wins[B_v] += 1
                else:
                    wins[C_v] += 1
                # A vs C
                if edge_dir.get((A_v, C_v)) == 1:
                    wins[A_v] += 1
                else:
                    wins[C_v] += 1
                
                # Sort by number of wins
                sorted_vertices = sorted(wins.items(), key=lambda x: x[1], reverse=True)
                first_layer = sorted_vertices[0][0][0]   # "A", "B", or "C"
                second_layer = sorted_vertices[1][0][0]
                third_layer = sorted_vertices[2][0][0]
                position_counts[first_layer][1] += 1
                position_counts[second_layer][2] += 1
                position_counts[third_layer][3] += 1
    
    # Check final counts
    for layer in ["A", "B", "C"]:
        if position_counts[layer][1] != required_count: return False
        if position_counts[layer][2] != required_count: return False
        if position_counts[layer][3] != required_count: return False
    return True

solutions_checked = 0

def backtrack_edge_assignment(idx=0):
    if idx == len(all_pairs):
        global solutions_checked
        solutions_checked += 1
        if solutions_checked % 100000 == 0:
            print(f"Checked {solutions_checked} assignments")
        if check_condition_3():
            solutions.append(dict(edge_dir))
            print("Found a valid solution!", dict(edge_dir))
        return
    
    v1, v2 = all_pairs[idx]
    
    # Try v1->v2
    edge_dir[(v1, v2)] = +1
    if (v2, v1) in edge_dir:  # remove any conflicting assignment
        del edge_dir[(v2, v1)]
    if not forms_3_cycle(v1, v2):
        backtrack_edge_assignment(idx+1)
    del edge_dir[(v1, v2)]
    
    # Try v2->v1
    edge_dir[(v2, v1)] = +1
    if not forms_3_cycle(v2, v1):
        backtrack_edge_assignment(idx+1)
    del edge_dir[(v2, v1)]

if __name__ == "__main__":
    backtrack_edge_assignment(0)
    print(f"Number of solutions: {len(solutions)}")
    if solutions:
        print("Example solution:", solutions[0])
