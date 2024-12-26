import time
from collections import deque
import sys

# ************ Initialization ************
_DAY = "16"  # Challenge day
_FILE = sys.argv[1] if len(sys.argv) > 1 else "Day16/input.txt"  # Input file
_TIMERS = {"global": time.time(), "part_1": None, "part_2": None}
_OUTPUT_LENGTH = 50
_ANSWERS = {}

def print_day_title_plate(day):
    """Print the day of the challenge."""
    print(f"Day {_DAY}")

print_day_title_plate(_DAY)

# ************ Helper Functions ************

def read_input_file(file_path):
    """Read the input file and return its content as a string."""
    with open(file_path, "r") as file:
        return file.read().strip()

def is_within_bounds(grid, x, y):
    """Check if the coordinates are within the grid's bounds."""
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def pick_time_unit(time_diff):
    """Convert time to a suitable unit for display."""
    if time_diff < 1:
        return time_diff * 1000, "µs"
    elif time_diff < 1000:
        return time_diff, "ms"
    elif time_diff < 60000:
        return time_diff / 1000, "s"
    elif time_diff < 3600000:
        return time_diff / 60000, "m"
    else:
        return time_diff / 3600000, "h"

def log_answer(answer, part):
    """Log the answer for each part."""
    print(f"Part {part} answer: {answer}")

def parse_input(file_path):
    """Parse the input file and extract useful data like start, end, and grid."""
    input_data = read_input_file(file_path)
    start, end = None, None
    grid = []
    
    for y, row in enumerate(input_data.split("\n")):
        grid_row = []
        for x, char in enumerate(row):
            if char == "S":
                start = (x, y)
            if char == "E":
                end = (x, y)
            grid_row.append({
                "x": x, "y": y, "char": char,
                "score": float("inf"), "turns": 0,
                "visited": []
            })
        grid.append(grid_row)
    
    return {"map": grid, "start": start, "end": end}

# ************ Main Logic ************

def solve_part1(data):
    """Solve the first part of the challenge."""
    answer = 0
    queue = deque()
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    start_x, start_y = data["start"]
    end_x, end_y = data["end"]
    grid = data["map"]

    # Initialize the starting point for all possible directions
    for i in range(4):
        grid[start_y][start_x]["score"] = 0
        queue.append((start_x, start_y, i))

    # BFS to find the shortest path
    while queue:
        # Sort the queue by score (prioritize lower scores)
        queue = sorted(queue, key=lambda x: grid[x[1]][x[0]]["score"])
        current_x, current_y, current_dir = queue.pop(0)

        # If we reached the end, store the answer
        if (current_x, current_y) == (end_x, end_y):
            answer = grid[current_y][current_x]["score"]
            break

        # Explore neighboring cells
        for i, (dx, dy) in enumerate(directions):
            next_x, next_y = current_x + dx, current_y + dy
            if not is_within_bounds(grid, next_x, next_y) or grid[next_y][next_x]["char"] == "#":
                continue

            # Calculate the new score based on the direction
            new_score = grid[current_y][current_x]["score"] + (1 if i == current_dir else 1001)
            if new_score < grid[next_y][next_x]["score"]:
                grid[next_y][next_x]["score"] = new_score
                queue.append((next_x, next_y, i))

    return answer

def solve_part2(data):
    """Solve the second part of the challenge."""
    best_paths = []
    best_score = float("inf")
    queue = deque()
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    start_x, start_y = data["start"]
    end_x, end_y = data["end"]
    grid = data["map"]

    # Initialize the starting point for all possible directions
    for i in range(4):
        grid[start_y][start_x]["score"] = 0
        queue.append((start_x, start_y, i))

    # BFS to find the best paths
    while queue:
        # Sort the queue by score (prioritize lower scores)
        queue = sorted(queue, key=lambda x: grid[x[1]][x[0]]["score"])
        current_x, current_y, current_dir = queue.pop(0)

        # If we reached the end, store the best path
        if (current_x, current_y) == (end_x, end_y):
            if grid[current_y][current_x]["score"] > best_score:
                continue
            best_paths.append({"score": grid[current_y][current_x]["score"]})
            best_score = grid[current_y][current_x]["score"]
            continue

        # Explore neighboring cells
        for i, (dx, dy) in enumerate(directions):
            next_x, next_y = current_x + dx, current_y + dy
            if not is_within_bounds(grid, next_x, next_y) or grid[next_y][next_x]["char"] == "#":
                continue

            # Calculate the new score based on the direction
            new_score = grid[current_y][current_x]["score"] + (1 if i == current_dir else 1001)
            if new_score < grid[next_y][next_x]["score"]:
                grid[next_y][next_x]["score"] = new_score
                queue.append((next_x, next_y, i))

    # Calculate the number of unique positions visited across all best paths
    unique_positions = set()
    for path in best_paths:
        for position in path["visited"]:
            unique_positions.add(position)
    
    return len(unique_positions)

if __name__ == "__main__":
    input_data = parse_input(_FILE)

    # Solve part 1
    _TIMERS["part_1"] = time.time()
    _ANSWERS["part1"] = solve_part1(input_data)
    log_answer(_ANSWERS["part1"], 1)

    # Solve part 2
    _TIMERS["part_2"] = time.time()
    _ANSWERS["part2"] = solve_part2(input_data)
    log_answer(_ANSWERS["part2"], 2)

    # Calculate and print the total execution time
    total_time = time.time() - _TIMERS["global"]
    total_time_value, total_time_unit = pick_time_unit(total_time)
    print(f"Total execution time: {total_time_value:.2f} {total_time_unit}")
