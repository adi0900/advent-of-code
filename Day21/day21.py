from collections import Counter
from time import perf_counter as measure_time

def performance_profiler(method):
    """
    A decorator to measure and print the execution time of a method.
    """
    def timing_wrapper(*args, **kwargs):
        start_time = measure_time()  # Start the timer
        
        # Execute the original method
        result = method(*args, **kwargs)
        
        # Print the execution time
        print(f"Method {method.__name__} took: {measure_time() - start_time:2.5f} sec")
        
        return result  # Return the original method's result
    return timing_wrapper


def calculate_manhattan_distance(point1, point2):
    """
    Calculate the Manhattan distance between two points in the complex plane.
    """
    return abs(point1.real - point2.real) + abs(point1.imag - point2.imag)


def create_keypad_mapping(keypad_layout):
    """
    Create a dictionary that maps each character on the keypad to its position 
    (represented as a complex number).
    """
    return {
        char: row_idx + 1j * col_idx  # Using complex numbers to represent positions
        for row_idx, row in enumerate(keypad_layout.split(','))
        for col_idx, char in enumerate(row)
        if char != '_'
    }


def find_shortest_paths(start_pos, end_pos, keypad):
    """
    Find all shortest paths between the start and end positions using depth-first search.
    """
    exploration_stack = [(start_pos, [])]  # Stack of positions to explore
    valid_paths = []  # List to store valid paths
    directions = (1, -1, 1j, -1j)  # Directions to move: down, up, right, left
    direction_to_symbol = {1: 'v', -1: '^', 1j: '>', -1j: '<'}  # Direction to symbol mapping
    
    while exploration_stack:
        current_pos, path = exploration_stack.pop()  # Get the next position and its current path
        
        if current_pos == end_pos:
            valid_paths.append(path)  # If we reached the destination, store the path
            continue
        
        # Explore all directions
        for direction in directions:
            next_pos = current_pos + direction
            # Only move if the next position is closer to the end and valid
            if (calculate_manhattan_distance(next_pos, end_pos) >= 
                calculate_manhattan_distance(current_pos, end_pos) or 
                next_pos not in keypad.values()):
                continue
            exploration_stack.append((next_pos, path + [direction]))  # Continue exploring from next position

    # Convert direction sequences into symbols
    return [''.join(direction_to_symbol[d] for d in path) for path in valid_paths]


def generate_input_sequences(sequence, keypad):
    """
    Generate all possible shortest input sequences to type a given sequence on the keypad.
    """
    sequence = 'A' + sequence  # Add the starting point ('A') to the sequence
    current_paths = ['']  # Start with an empty path
    
    # Iterate through the sequence and generate paths between each pair of consecutive characters
    for i in range(len(sequence) - 1):
        new_paths = []
        for current_path in current_paths:
            for shortest_path in find_shortest_paths(
                keypad[sequence[i]], keypad[sequence[i + 1]], keypad
            ):
                new_paths.append(current_path + shortest_path + 'A')  # Append new path to current path
        current_paths = new_paths  # Update current paths
    
    return current_paths


def precalculate_best_paths(direction_keypad):
    """
    Pre-calculate optimal paths for all pairs of directions (valid directions: ^, <, v, >, A).
    """
    valid_directions = "^<>vA"
    best_paths = {}
    
    # Calculate the best paths between all direction pairs
    for dir1 in valid_directions:
        for dir2 in valid_directions:
            # Find all possible paths between dir1 and dir2
            paths = [(x, x) for x in find_shortest_paths(
                direction_keypad[dir1], direction_keypad[dir2], direction_keypad
            )]
            
            # Keep refining the paths until all paths are the same
            while len(set(x for x, _ in paths)) != 1:
                paths = find_optimal_sequences(paths, direction_keypad)
            
            best_paths[(dir1, dir2)] = paths[0][0]  # Store the best path for the direction pair
    
    return best_paths


def optimize_sequence(sequence_data, best_paths):
    """
    Optimize the sequence using pre-calculated best paths to minimize the number of steps.
    """
    transitions, first_char = sequence_data
    optimized_transitions = Counter()
    
    # Start with the best path from 'A' to the first character
    start_sequence = best_paths[('A', first_char)] + 'A'
    new_first_char = start_sequence[0]
    transitions[('A', first_char)] += 1
    optimized_transitions[('A', new_first_char)] -= 1
    
    # Optimize the transitions between characters in the sequence
    for (char1, char2), count in transitions.items():
        path = 'A' + best_paths[(char1, char2)] + 'A'
        for i in range(len(path) - 1):
            optimized_transitions[(path[i], path[i+1])] += count

    return (optimized_transitions, new_first_char)


def convert_to_transition_counter(sequence):
    """
    Convert a sequence into a Counter object that counts transitions between characters.
    """
    transitions = Counter()
    for i in range(len(sequence) - 1):
        transitions[(sequence[i], sequence[i + 1])] += 1
    return (transitions, sequence[0])  # Return the transitions and the first character


def solve_sequence(sequence, number_keypad, best_paths, iterations):
    """
    Solve the sequence optimization for a given number of iterations to find the minimum number of steps.
    """
    sequences = [convert_to_transition_counter(seq) 
                for seq in generate_input_sequences(sequence, number_keypad)]
    
    # Perform optimization for the given number of iterations
    for _ in range(iterations):
        sequences = [optimize_sequence(seq, best_paths) for seq in sequences]

    # Return the minimum number of steps required
    return min(sum(seq[0].values()) + 1 for seq in sequences)


@performance_profiler
def solve_day_21(codes):
    """
    Solve the problem for both parts using the provided codes.
    """
    # Create keypad mappings for numbers and directions
    number_keypad = create_keypad_mapping("789,456,123,_0A")
    direction_keypad = create_keypad_mapping("_^A,<v>")
    
    # Pre-calculate optimal paths for directions
    best_paths = precalculate_best_paths(direction_keypad)
    
    # Initialize results for both parts
    part1 = part2 = 0
    
    # Solve for each code and accumulate the results
    for code in codes:
        multiplier = int(code[:3])
        part1 += int(multiplier * solve_sequence(code, number_keypad, best_paths, 2))
        part2 += int(multiplier * solve_sequence(code, number_keypad, best_paths, 25))

    return part1, part2


def parse_input(file_path):
    """
    Parse the input file and return the list of codes.
    """
    with open(file_path, "r") as f:
        lines = f.read().strip().splitlines()
    return lines


if __name__ == "__main__":
    codes = parse_input("Day21/input.txt")  # Parse the input file
    p1, p2 = solve_day_21(codes)  # Solve both parts
    print(f"Part 1:", p1)
    print(f"Part 2:", p2)
