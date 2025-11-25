def find_divisible_combinations():
    # Configuration
    max_nodes_per_layer = 6
    
    print(f"{'L1':<5} {'L2':<5} {'L3':<5} | {'Calculation':<20} | {'Total':<5}")
    print("-" * 50)

    count_found = 0

    # Iterate through Layer 1 nodes (1 to 6)
    for l1 in range(1, max_nodes_per_layer + 1):
        # Iterate through Layer 2 nodes (1 to 6)
        for l2 in range(1, max_nodes_per_layer + 1):
            # Iterate through Layer 3 nodes (1 to 6)
            for l3 in range(1, max_nodes_per_layer + 1):
                
                # Calculate connections between layers
                # (L1 connects to L2) + (L2 connects to L3) + (L3 connects to L1)
                conns_1_2 = l1 * l2
                conns_2_3 = l2 * l3
                conns_3_1 = l3 * l1
                
                total_connections = conns_1_2 + conns_2_3 + conns_3_1
                
                # Check if divisible by 3
                if total_connections % 3 == 0:
                    count_found += 1
                    calc_str = f"{l1}x{l2} + {l2}x{l3} + {l3}x{l1}"
                    print(f"{l1:<5} {l2:<5} {l3:<5} | {calc_str:<20} | {total_connections:<5}")

    print("-" * 50)
    print(f"Total combinations found: {count_found}")

if __name__ == "__main__":
    find_divisible_combinations()