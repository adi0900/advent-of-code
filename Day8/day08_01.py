import os
from typing import List, Set, Tuple, Dict
from collections import defaultdict
from math import gcd
from time import perf_counter


def read_map(filename: str) -> List[str]:
    """
    Reads the grid map from a file.

    :param filename: The name of the file containing the grid map.
    :return: A list of strings representing the grid.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Failed to open file: {filename}")
    with open(filename, 'r') as file:
        grid = file.read().splitlines()
    return grid


def compute_antinodes_pairwise(grid: List[str]) -> Set[Tuple[int, int]]:
    """
    Computes unique antinode positions using the pairwise method.

    :param grid: A list of strings representing the grid map.
    :return: A set of unique antinode positions.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    antennas_by_freq = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch != '.':
                antennas_by_freq[ch].append((r, c))

    antinodes = set()
    for coords in antennas_by_freq.values():
        n = len(coords)
        if n < 2:
            continue

        for i in range(n):
            rA, cA = coords[i]
            for j in range(i + 1, n):
                rB, cB = coords[j]

                # Compute P1 = 2B - A
                p1_r, p1_c = 2 * rB - rA, 2 * cB - cA
                if 0 <= p1_r < rows and 0 <= p1_c < cols:
                    antinodes.add((p1_r, p1_c))

                # Compute P2 = 2A - B
                p2_r, p2_c = 2 * rA - rB, 2 * cA - cB
                if 0 <= p2_r < rows and 0 <= p2_c < cols:
                    antinodes.add((p2_r, p2_c))

    return antinodes


def add_line_points(rA: int, cA: int, rB: int, cB: int, rows: int, cols: int, antinodes: Set[Tuple[int, int]]):
    """
    Adds all points along a line between two antennas to the antinodes set.

    :param rA: Row of the first antenna.
    :param cA: Column of the first antenna.
    :param rB: Row of the second antenna.
    :param cB: Column of the second antenna.
    :param rows: Number of rows in the grid.
    :param cols: Number of columns in the grid.
    :param antinodes: Set to store unique antinode positions.
    """
    dr, dc = rB - rA, cB - cA
    g = gcd(abs(dr), abs(dc))
    dr, dc = dr // g, dc // g

    rP, cP = rA, cA
    while 0 <= rP < rows and 0 <= cP < cols:
        antinodes.add((rP, cP))
        rP += dr
        cP += dc

    rP, cP = rA - dr, cA - dc
    while 0 <= rP < rows and 0 <= cP < cols:
        antinodes.add((rP, cP))
        rP -= dr
        cP -= dc


def compute_antinodes_lines(grid: List[str]) -> Set[Tuple[int, int]]:
    """
    Computes unique antinode positions using the line-drawing method.

    :param grid: A list of strings representing the grid map.
    :return: A set of unique antinode positions.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    antennas_by_freq = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch != '.':
                antennas_by_freq[ch].append((r, c))

    antinodes = set()
    for coords in antennas_by_freq.values():
        n = len(coords)
        if n < 2:
            continue

        for i in range(n):
            rA, cA = coords[i]
            for j in range(i + 1, n):
                rB, cB = coords[j]
                add_line_points(rA, cA, rB, cB, rows, cols, antinodes)

    return antinodes


def format_time(seconds: float) -> str:
    """
    Formats the elapsed time in seconds as a human-readable string.

    :param seconds: The elapsed time in seconds.
    :return: The formatted time as a string.
    """
    return f"{seconds:.9f} s"


def main():
    try:
        grid = read_map("Day8/input.txt")

        overall_start = perf_counter()

        # Part 1: Compute using Pairwise method
        start_time = perf_counter()
        pairwise_antinodes = compute_antinodes_pairwise(grid)
        part1_time = perf_counter() - start_time

        print(f"Part 1 finished in {format_time(part1_time)}")
        print(f"Number of unique antinodes (Pairwise method): {len(pairwise_antinodes)}")

        # Part 2: Compute using Line-drawing method
        start_time = perf_counter()
        line_antinodes = compute_antinodes_lines(grid)
        part2_time = perf_counter() - start_time

        print(f"Part 2 finished in {format_time(part2_time)}")
        print(f"Number of unique antinodes (Line-drawing method): {len(line_antinodes)}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
