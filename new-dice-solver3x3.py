import numpy as np

def find3x3Coordinates(node1, node2):
    """
    Given a two nodes, return the 3x3x3 coordinates that edge in the Dice Matrix.

    Returns:
        (x, y, z) (tuple): The 3x3x3 coordinates of the dice faces.
    """
    # Define the 3x3x3 coordinates of the dice faces
    coordinates = {
        ("A1", "B1"): (0, 0, 0),
        ("A1", "B2"): (0, 0, 1),
        ("A1", "B3"): (0, 0, 2),
        ("A2", "B1"): (0, 1, 0),
        ("A2", "B2"): (0, 1, 1),
        ("A2", "B3"): (0, 1, 2),
        ("A3", "B1"): (0, 2, 0),
        ("A3", "B2"): (0, 2, 1),
        ("A3", "B3"): (0, 2, 2),
        ("B1", "C1"): (1, 0, 0),
        ("B1", "C2"): (1, 0, 1),
        ("B1", "C3"): (1, 0, 2),
        ("B2", "C1"): (1, 1, 0),
        ("B2", "C2"): (1, 1, 1),
        ("B2", "C3"): (1, 1, 2),
        ("B3", "C1"): (1, 2, 0),
        ("B3", "C2"): (1, 2, 1),
        ("B3", "C3"): (1, 2, 2),
        ("C1", "A1"): (2, 0, 0),
        ("C1", "A2"): (2, 0, 1),
        ("C1", "A3"): (2, 0, 2),
        ("C2", "A1"): (2, 1, 0),
        ("C2", "A2"): (2, 1, 1),
        ("C2", "A3"): (2, 1, 2),
        ("C3", "A1"): (2, 2, 0),
        ("C3", "A2"): (2, 2, 1),
        ("C3", "A3"): (2, 2, 2)
    }

    return coordinates[(node1, node2)]


def main():
    # Step 1: Initialize a NumPy 3x3x3 matrix with zeros.
    DM = np.full((3, 3, 3), 0)      # DM = Dice Matrix
    
    # DM[0, 0, 1] = 1
    # DM[testVal, :] = 1

    tests_list = ["A1", "A2", "A3"]
    current_path = []

    # create an undirected graph where each vertex is a dice face, and each edge connects to all other faces on the other dice
    # each vertex therefore has 6 edges
    dice_graph = {
        "A1": ["B1", "B2", "B3"],
        "A2": ["B1", "B2", "B3"],
        "A3": ["B1", "B2", "B3"],
        "B1": ["C1", "C2", "C3"],
        "B2": ["C1", "C2", "C3"],
        "B3": ["C1", "C2", "C3"],
        "C1": ["A1", "A2", "A3"],
        "C2": ["A1", "A2", "A3"],
        "C3": ["A1", "A2", "A3"]
    }

    while tests_list:
        test = tests_list.pop()
        print("testing:", test)

        # if at level 3
        if test in {"C1", "C2", "C3"}:
            current_path.append(test)
            (x, y, z) = find3x3Coordinates(current_path[-2], current_path[-1])
            DM[x, y, z] = 1
            (x, y, z) = find3x3Coordinates(current_path[-1], current_path[-3])
            DM[x, y, z] = -1
            print(tests_list)
            print(current_path)
            print(DM)
            current_path.pop()
            continue
        
        for face in dice_graph[test]:
            tests_list.append(face)

        while current_path and (test not in dice_graph[current_path[-1]]):
            current_path.pop()
            print("backtrack to:", current_path, "with", tests_list)
        current_path.append(test)

        if len(current_path) == 1:
            # do something
            pass

        if len(current_path) == 2:
            (x, y, z) = find3x3Coordinates(current_path[-2], current_path[-1])
            DM[x, y, z] = 1
            print(tests_list)
            print(current_path)
            print(DM)
            # return




if __name__ == "__main__":
    main()
