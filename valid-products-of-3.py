# We only consider multiples of 3 in [3..216].
for product_value in range(3, 217, 3):
    triples = []
    
    # We'll search for all (a,b,c) with 1 <= a,b,c <= product_value.
    # A quick optimization: once we fix 'a', let leftover = product_value // a,
    # then we only need 1 <= b <= leftover, and c = leftover // b (if divisible).
    for a in range(1, product_value+1):
        # If 'a' doesn't divide product_value, skip it:
        if product_value % a != 0:
            continue
        
        leftover = product_value // a
        for b in range(a, leftover+1):
            if leftover % b != 0:
                continue
            
            c = leftover // b
            # Ensure b <= c (so we don't double-count permutations).
            if b <= c and a * b * c == product_value:
                triples.append((a, b, c))
    
    # Sort the found triples for a neat display (first by a, then b, then c)
    triples.sort()
    
    # Print the product value followed by all valid triples
    print(f"{product_value}: {triples}")
