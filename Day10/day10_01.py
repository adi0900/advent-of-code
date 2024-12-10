import time
from collections import deque

def read_map(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    grid = [[int(char) for char in line.strip()] for line in lines if line.strip()]
    return grid

def neighbors(r, c, rows, cols):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def find_trailhead_scores(grid):
    rows, cols = len(grid), len(grid[0])

    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    total_score = 0

    for start_r, start_c in trailheads:
        visited = set()
        queue = deque([(start_r, start_c)])
        visited.add((start_r, start_c))
        reachable_nines = set()

        while queue:
            r, c = queue.popleft()
            current_height = grid[r][c]

            if current_height == 9:
                reachable_nines.add((r, c))
            else:
                next_height = current_height + 1
                for nr, nc in neighbors(r, c, rows, cols):
                    if (nr, nc) not in visited and grid[nr][nc] == next_height:
                        visited.add((nr, nc))
                        queue.append((nr, nc))

        total_score += len(reachable_nines)

    return total_score

def calculate_total_rating(grid):
    rows, cols = len(grid), len(grid[0])

    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    dp = [[-1] * cols for _ in range(rows)]

    def count_paths(r, c):
        if dp[r][c] != -1:
            return dp[r][c]

        current_height = grid[r][c]

        if current_height == 9:
            dp[r][c] = 1
            return 1

        total_paths = 0
        next_height = current_height + 1
        for nr, nc in neighbors(r, c, rows, cols):
            if grid[nr][nc] == next_height:
                total_paths += count_paths(nr, nc)

        dp[r][c] = total_paths
        return total_paths

    total_rating = sum(count_paths(r, c) for r, c in trailheads)
    return total_rating

if __name__ == "__main__":
    INPUT_FILE = "Day10/input.txt"

    # Part 1
    start_time_part1 = time.time()
    grid = read_map(INPUT_FILE)
    total_score = find_trailhead_scores(grid)
    end_time_part1 = time.time()
    print(f"Part 1 Result: {total_score}")
    print(f"Time taken for Part 1: {end_time_part1 - start_time_part1:.9f} s")

    # Part 2
    start_time_part2 = time.time()
    total_rating = calculate_total_rating(grid)
    end_time_part2 = time.time()
    print(f"Part 2 Result: {total_rating}")
    print(f"Time taken for Part 2: {end_time_part2 - start_time_part2:.9f} s")
