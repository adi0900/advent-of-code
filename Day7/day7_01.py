import itertools
from time import time
from typing import List, Tuple

class TestCase:
    def __init__(self, target: int, numbers: List[int]):
        self.target = target
        self.numbers = numbers

def evaluate_left_to_right(numbers: List[int], ops: List[str]) -> int:
    result = numbers[0]
    for i, op in enumerate(ops):
        next_number = numbers[i + 1]
        if op == "+":
            result += next_number
        elif op == "*":
            result *= next_number
        else:
            raise ValueError(f"Unsupported operator: {op}")
    return result

def evaluate_with_concat(numbers: List[int], ops: List[str]) -> int:
    result = numbers[0]
    for i, op in enumerate(ops):
        next_number = numbers[i + 1]
        if op == "+":
            result += next_number
        elif op == "*":
            result *= next_number
        elif op == "||":
            result = int(str(result) + str(next_number))
        else:
            raise ValueError(f"Unsupported operator: {op}")
    return result

def parse_input(file_path: str) -> List[TestCase]:
    test_cases = []
    with open(file_path, "r") as file:
        for line in file:
            if ":" not in line:
                continue
            target_str, numbers_str = line.split(":")
            target = int(target_str.strip())
            numbers = list(map(int, numbers_str.strip().split()))
            test_cases.append(TestCase(target, numbers))
    return test_cases

def generate_operator_combinations(operators: List[str], length: int) -> List[List[str]]:
    return list(itertools.product(operators, repeat=length))

def solve_part_one(test_cases: List[TestCase]) -> int:
    operators = ["+", "*"]
    valid_test_values_sum = 0

    for test_case in test_cases:
        possible = False
        ops_length = len(test_case.numbers) - 1
        all_ops = generate_operator_combinations(operators, ops_length)

        for ops in all_ops:
            if evaluate_left_to_right(test_case.numbers, ops) == test_case.target:
                possible = True
                break
        if possible:
            valid_test_values_sum += test_case.target

    return valid_test_values_sum

def solve_part_two(test_cases: List[TestCase], part_one_time: float) -> Tuple[int, float]:
    operators = ["+", "*", "||"]
    valid_test_values_sum = 0

    total_cases = len(test_cases)
    progress_interval = max(1, total_cases // 10)

    cumulative1 = 0.0
    cumulative2 = part_one_time

    print("\nProgress    Interval(s)      Cumulative1(s)    Cumulative2(s)")
    print("-------------------------------------------------------------")

    start = time()

    for index, test_case in enumerate(test_cases):
        possible = False
        ops_length = len(test_case.numbers) - 1
        all_ops = generate_operator_combinations(operators, ops_length)

        for ops in all_ops:
            if evaluate_with_concat(test_case.numbers, ops) == test_case.target:
                possible = True
                break
        if possible:
            valid_test_values_sum += test_case.target

        if (index + 1) % progress_interval == 0 or (index + 1) == total_cases:
            now = time()
            interval_elapsed = now - start
            cumulative1 += interval_elapsed
            cumulative2 = part_one_time + cumulative1

            print(f"{index + 1:10}/{total_cases} {interval_elapsed:20.9f} {cumulative1:20.9f} {cumulative2:20.9f}")

            start = time()

    return valid_test_values_sum, cumulative2

def main():
    file_path = "Day7/input.txt"  # Change this to your actual input file location

    test_cases = parse_input(file_path)

    print("Starting Part 1...")
    part_one_start = time()
    part_one_result = solve_part_one(test_cases)
    part_one_time = time() - part_one_start
    print(f"Part 1 finished in {part_one_time:.9f} seconds")
    print(f"Part 1 Total Calibration Result: {part_one_result}")

    print("Starting Part 2...")
    part_two_result, cumulative_time = solve_part_two(test_cases, part_one_time)
    part_two_time = cumulative_time - part_one_time
    print(f"\nPart 2 finished in {part_two_time:.9f} seconds, cumulative time {cumulative_time:.9f} seconds")
    print(f"Part 2 Total Calibration Result: {part_two_result}")

if __name__ == "__main__":
    main()
