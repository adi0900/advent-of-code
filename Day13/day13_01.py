import asyncio
import re
import time
from pathlib import Path

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)


def parse_line(line, task):
    if "A:" in line:
        match = re.findall(r"\d+", line)
        if len(match) >= 2:
            task['A'] = Point(int(match[0]), int(match[1]))

    elif "B:" in line:
        match = re.findall(r"\d+", line)
        if len(match) >= 2:
            task['B'] = Point(int(match[0]), int(match[1]))

    elif "Prize" in line:
        match = re.findall(r"\d+", line)
        if len(match) >= 2:
            task['Prize'] = Point(int(match[0]), int(match[1]))


def calc_a_and_b(A, B, Prize):
    # Replace this with the actual calculation logic
    A_val = abs(A.x - Prize.x) + abs(A.y - Prize.y)
    B_val = abs(B.x - Prize.x) + abs(B.y - Prize.y)
    return A_val, B_val


def parse_input_file(file_path):
    tasks = []
    task = {}
    with open(file_path, "r") as file:
        for line in file:
            parse_line(line.strip(), task)

            if 'A' in task and 'B' in task and 'Prize' in task:
                tasks.append(task)
                task = {}

    if 'A' in task and 'B' in task and 'Prize' in task:
        tasks.append(task)

    return tasks


def part1(file_path):
    tasks = parse_input_file(file_path)
    total_sum = 0

    for task in tasks:
        A, B = calc_a_and_b(task['A'], task['B'], task['Prize'])
        if A != -1:
            total_sum += B + A * 3

    return total_sum


def part2(file_path):
    tasks = parse_input_file(file_path)
    total_sum = 0
    shift = Point(10000000000000, 10000000000000)

    for task in tasks:
        big_prize = task['Prize'].add(shift)
        A, B = calc_a_and_b(task['A'], task['B'], big_prize)
        if A > -1 and B > 0:
            total_sum += B + A * 3

    return total_sum


def main():
    print("Processing Part 1")
    start_time = time.time()
    part1_result = part1("Day13/input.txt")
    print(f"Part 1 Result: {part1_result}")
    print(f"Time Taken: {time.time() - start_time:.2f} seconds")

    print("\nProcessing Part 2")
    start_time = time.time()
    part2_result = part2("Day13/input.txt")
    print(f"Part 2 Result: {part2_result}")
    print(f"Time Taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
