dist = []
for corner in corners:
    if corner not in state[1]:
        dist.append(util.manhattanDistance(state[0],corner))

return max(dist)Σ