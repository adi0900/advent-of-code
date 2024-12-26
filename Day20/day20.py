from collections import defaultdict
import heapq

# Function to read and parse the grid input from a file
def parse_input(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append([char for char in line.strip()])
    return grid

# Helper function to check if a coordinate is inside the grid boundaries
def inside(i, j, N, M):
    return 0 <= i < N and 0 <= j < M

# Function to solve the first part of the problem
def solve1(grid, minsave):
    N, M = len(grid), len(grid[0])
    
    # Initialize start and end positions
    si, sj, ei, ej = 0, 0, 0, 0
    for i in range(N):
        for j in range(M):
            if grid[i][j] == 'S':
                si, sj = i, j
            elif grid[i][j] == 'E':
                ei, ej = i, j

    # Priority queue for BFS/DFS and visited path tracking
    h = [(0, si, sj, 0, 0)]
    path = []
    cost = {}

    while h:
        c, i, j, pi, pj = h.pop()
        
        # Skip walls
        if grid[i][j] == "#":
            continue
        
        # Mark this cell as part of the path
        path.append((i, j))
        cost[(i, j)] = c
        
        # Stop if the end is reached
        if grid[i][j] == "E":
            break

        # Check all adjacent cells
        nxt = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        for ni, nj in nxt:
            if (ni, nj) != (pi, pj):  # Avoid revisiting the previous cell
                h.append((c + 1, ni, nj, i, j))

    # Calculate potential savings for each path step
    savings = {}
    count = 0
    for i, j in path:
        nxt = [(i + 2, j), (i - 2, j), (i, j + 2), (i, j - 2)]
        thru = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        
        for x in range(len(nxt)):
            ni, nj = nxt[x]
            ti, tj = thru[x]

            # Skip invalid positions
            if not inside(ni, nj, N, M) or grid[ni][nj] == '#':
                continue
            
            # Check if we can "save" a step
            if cost[(ni, nj)] - cost[(i, j)] - 2 >= minsave and grid[ti][tj] == '#':
                savings[(i, j, ni, nj)] = cost[(ni, nj)] - cost[(i, j)] - 2
                count += 1

    print(f"Part One - {count}")  # Expected: 1518

# Function to solve the second part of the problem
def solve2(grid, minsave):
    N, M = len(grid), len(grid[0])

    # Initialize start and end positions
    si, sj, ei, ej = 0, 0, 0, 0
    for i in range(N):
        for j in range(M):
            if grid[i][j] == 'S':
                si, sj = i, j
            elif grid[i][j] == 'E':
                ei, ej = i, j

    # Priority queue for BFS/DFS and visited path tracking
    h = [(0, si, sj, 0, 0)]
    path = []
    cost = {}

    while h:
        c, i, j, pi, pj = h.pop()
        
        # Skip walls
        if grid[i][j] == "#":
            continue
        
        # Mark this cell as part of the path
        path.append((i, j))
        cost[(i, j)] = c
        
        # Stop if the end is reached
        if grid[i][j] == "E":
            break

        # Check all adjacent cells
        nxt = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        for ni, nj in nxt:
            if (ni, nj) != (pi, pj):  # Avoid revisiting the previous cell
                h.append((c + 1, ni, nj, i, j))

    # Calculate potential savings for each path step
    savings = {}
    count = 0
    for i, j in path:
        for step in range(2, 21):  # Loop through different Manhattan distances
            for di in range(step + 1):
                dj = step - di
                nxt = [
                    (i + di, j + dj), (i + di, j - dj),
                    (i - di, j + dj), (i - di, j - dj)
                ]
                for ni, nj in nxt:
                    # Skip invalid positions and already visited paths
                    if not inside(ni, nj, N, M) or grid[ni][nj] == '#' or (i, j, ni, nj) in savings:
                        continue
                    
                    # Check if we can "save" a step
                    if cost[(ni, nj)] - cost[(i, j)] - step >= minsave:
                        savings[(i, j, ni, nj)] = cost[(ni, nj)] - cost[(i, j)] - step
                        count += 1

    print(f"Part Two - {count}")  # Expected: 1032257

# Main code to parse the input file and call the solution functions
grid = parse_input('Day20/input.txt')
solve1(grid, 100)
solve2(grid, 100)
