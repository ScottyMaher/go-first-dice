def find_divisible_combinations():
    # Configuration
    max_nodes_per_layer = 6
    
    # Same columns as before
    print(f"{'L1':<3} {'L2':<3} {'L3':<3} | {'Calculation':<18} | {'Conn Sum':<8} | {'Prod Calc':<10} | {'Prod Total':<10}")
    print("-" * 80)

    count_found = 0

    for l1 in range(1, max_nodes_per_layer + 1):
        for l2 in range(1, max_nodes_per_layer + 1):
            for l3 in range(1, max_nodes_per_layer + 1):
                
                # 1. Calculate Connections (Connections 1-2, 2-3, 3-1)
                conns_1_2 = l1 * l2
                conns_2_3 = l2 * l3
                conns_3_1 = l3 * l1
                total_connections = conns_1_2 + conns_2_3 + conns_3_1
                
                # 2. Calculate Product of nodes
                node_product = l1 * l2 * l3
                
                # 3. Check Condition
                # ONLY check if the node_product is divisible by 3.
                # We ignore total_connections for the filtering, but still print it.
                if node_product % 3 == 0:
                    count_found += 1
                    
                    conn_calc_str = f"{l1}x{l2} + {l2}x{l3} + {l3}x{l1}"
                    prod_calc_str = f"{l1}x{l2}x{l3}"
                    
                    print(f"{l1:<3} {l2:<3} {l3:<3} | {conn_calc_str:<18} | {total_connections:<8} | {prod_calc_str:<10} | {node_product:<10}")

    print("-" * 80)
    print(f"Total combinations found: {count_found}")

if __name__ == "__main__":
    find_divisible_combinations()