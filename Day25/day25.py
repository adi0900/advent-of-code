import itertools
from time import perf_counter as time_tracker

def measure_performance(function):
    def wrapper(*args, **kwargs):
        start_time = time_tracker()
        
        result = function(*args, **kwargs)
        
        elapsed_time = time_tracker() - start_time
        print(f"Execution time for {function.__name__}: {elapsed_time:2.5f} seconds")
        
        return result
    return wrapper


def read_input(file_path):
    with open(file_path, "r") as file:
        lock_data = [section.splitlines() for section in file.read().split("\n\n")]
    
    return [
        {(col, row) for col, line in enumerate(lock) 
                    for row, char in enumerate(line) if char == "#"} 
        for lock in lock_data
    ]


@measure_performance
def solve_part_one(locks):
    no_overlap_pairs = 0
    for pattern_a, pattern_b in itertools.combinations(locks, 2):
        if not set.intersection(pattern_a, pattern_b):
            no_overlap_pairs += 1
    return no_overlap_pairs


if __name__ == "__main__":
    lock_patterns = read_input("Day25/input.txt")
    result = solve_part_one(lock_patterns)
    print("Part 1:", result)
