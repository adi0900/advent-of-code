import os
from collections import namedtuple
from typing import List, Tuple, Dict, Set

# Define data structures
Position = namedtuple("Position", ["row", "col"])
State = namedtuple("State", ["row", "col", "direction"])

# Direction mappings
DIRECTION_MAP: Dict[str, int] = {
    '^': 0,
    '>': 1,
    'v': 2,
    '<': 3
}

# Direction offsets: Up, Right, Down, Left
DIRECTION_OFFSETS: List[Tuple[int, int]] = [
    (-1, 0),  # Up
    (0, 1),   # Right
    (1, 0),   # Down
    (0, -1)   # Left
]

def trim(s: str) -> str:
    return s.strip()

def parse_grid(file_path: str) -> List[List[str]]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Unable to open file: {file_path}")

    with open(file_path, 'r') as file:
        grid = [list(trim(line)) for line in file if trim(line)]

    if not grid:
        raise ValueError("The grid is empty.")

    cols = len(grid[0])
    for row in grid:
        if len(row) != cols:
            raise ValueError("Inconsistent row lengths in the grid.")

    return grid

def find_guard(grid: List[List[str]]) -> Tuple[Position, int]:
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in DIRECTION_MAP:
                guard_pos = Position(r, c)
                guard_dir = DIRECTION_MAP[cell]
                grid[r][c] = '.'  # Clear the starting position
                return guard_pos, guard_dir

    raise ValueError("Guard not found in the grid.")

def get_possible_obstructions(grid: List[List[str]], guard_pos: Position) -> List[Position]:
    possible = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if (r, c) != (guard_pos.row, guard_pos.col) and cell == '.':
                possible.append(Position(r, c))
    return possible

def simulate_movement(grid: List[List[str]], start_pos: Position, start_dir: int) -> bool:
    visited_states: Set[State] = set()
    r, c = start_pos.row, start_pos.col
    direction = start_dir

    while True:
        current_state = State(r, c, direction)
        if current_state in visited_states:
            return True  # Loop detected

        visited_states.add(current_state)
        dr, dc = DIRECTION_OFFSETS[direction]
        new_r, new_c = r + dr, c + dc

        # Check boundaries
        if new_r < 0 or new_r >= len(grid) or new_c < 0 or new_c >= len(grid[0]):
            return False  # Guard exits the grid

        if grid[new_r][new_c] == '#':
            direction = (direction + 1) % 4  # Turn right
        else:
            r, c = new_r, new_c

def count_distinct_positions_visited(grid: List[List[str]], guard_pos: Position, guard_dir: int) -> int:
    visited_positions: Set[Position] = {guard_pos}

    current_pos = guard_pos
    current_dir = guard_dir

    while True:
        dr, dc = DIRECTION_OFFSETS[current_dir]
        new_r, new_c = current_pos.row + dr, current_pos.col + dc

        # Check boundaries
        if new_r < 0 or new_r >= len(grid) or new_c < 0 or new_c >= len(grid[0]):
            break  # Guard exits the grid

        if grid[new_r][new_c] == '#':
            current_dir = (current_dir + 1) % 4  # Turn right
        else:
            current_pos = Position(new_r, new_c)
            visited_positions.add(current_pos)

    return len(visited_positions)

# Example Usage
if __name__ == "__main__":
    file_path = "Day6/input.txt"  # Replace with your file path
    try:
        grid = parse_grid(file_path)
        guard_pos, guard_dir = find_guard(grid)
        print("Guard starting position:", guard_pos)
        print("Guard starting direction:", guard_dir)

        loop_detected = simulate_movement(grid, guard_pos, guard_dir)
        print("Loop detected:", loop_detected)

        distinct_positions = count_distinct_positions_visited(grid, guard_pos, guard_dir)
        print("Distinct positions visited:", distinct_positions)
        possible_obstructions = get_possible_obstructions(grid, guard_pos)
        print("Possible obstruction positions:", len(possible_obstructions))

    except (FileNotFoundError, ValueError) as e:
        print("Error:", e)
