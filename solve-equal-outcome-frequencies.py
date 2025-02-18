max_games = 27  # up to 6^3

solutions = []

# G must be multiple of 3, so let G = 3K with K up to 72
for K in range((max_games // 3) + 1):    # K up to 72
    # e can range from 0 to K
    for e in range(K + 1):
        x1 = e
        x4 = e
        x5 = e
        x2 = K - e
        x3 = K - e
        x6 = K - e

        G  = 3 * K  # total number of games

        # This (x1..x6) satisfies all the balanced conditions
        solutions.append((x1, x2, x3, x4, x5, x6, G))

for sol in solutions:
    x1, x2, x3, x4, x5, x6, G = sol
    print(f"x1={x1}, x2={x2}, x3={x3}, x4={x4}, x5={x5}, x6={x6}, total={G}")

# Print them out or process them as desired
print(f"Found {len(solutions)} solutions in total.\n")
