from time import perf_counter as measure_time

def measure_execution_time(function):
    """
    This decorator function measures and prints the time taken to execute another function.
    It wraps the function and prints how long it took to run.
    """
    def wrapper(*args, **kwargs):
        # Start the timer before running the function
        start_time = measure_time()
        
        # Run the function
        result = function(*args, **kwargs)
        
        # Calculate the time it took to run and print it
        elapsed_time = measure_time() - start_time
        print(f"Function {function.__name__} executed in {elapsed_time:2.5f} seconds")
        
        # Return the result of the function
        return result
    
    return wrapper

def calculate_secret_number(secret):
    """
    This function calculates the next secret number based on a series of operations.
    The operations include multiplying, dividing, and XOR'ing the value with certain constants.
    """
    # Step 1: Multiply by 64, XOR, and reduce the value
    secret ^= (secret * 64) % 16777216
    secret %= 16777216

    # Step 2: Divide by 32, XOR, and reduce the value
    secret ^= (secret // 32) % 16777216
    secret %= 16777216

    # Step 3: Multiply by 2048, XOR, and reduce the value
    secret ^= (secret * 2048) % 16777216
    secret %= 16777216

    return secret

@measure_execution_time
def part_one(values):
    """
    This function runs the secret number evolution 2000 times for each value,
    then sums up all the final results.
    """
    total = 0
    for value in values:
        # Evolve each value 2000 times
        for _ in range(2000):
            value = calculate_secret_number(value)
        total += value
    return total

@measure_execution_time
def part_two(values):
    """
    This function looks for patterns in the evolution of secret numbers.
    It collects patterns of differences and sums up certain values based on those patterns.
    """
    pattern_values = {}
    for value in values:
        last_digit = value % 10  # Starting point for pattern comparison
        pattern_list = []
        
        # Evolve the secret number 2000 times and track the patterns
        for _ in range(2000):
            value = calculate_secret_number(value)
            current_digit = value % 10
            pattern_list.append((current_digit - last_digit, current_digit))
            last_digit = current_digit
        
        # Check for repeated patterns and sum up values for unique patterns
        seen_patterns = set()
        for i in range(len(pattern_list) - 4):
            pattern = tuple(p[0] for p in pattern_list[i:i+4])
            value_at_end = pattern_list[i + 3][1]
            
            if pattern not in seen_patterns:
                seen_patterns.add(pattern)
                if pattern not in pattern_values:
                    pattern_values[pattern] = value_at_end
                else:
                    pattern_values[pattern] += value_at_end
    
    # Return the highest summed value from the patterns
    return max(pattern_values.values())

def read_input(file_path):
    """
    This function reads the input values from a file and converts them into a list of integers.
    """
    with open(file_path, "r") as file:
        lines = file.read().strip().splitlines()
    
    # Convert each line into an integer and return as a list
    return [int(x) for x in lines]

if __name__ == "__main__":
    # Read the input values from the file
    input_values = read_input("Day22/input.txt")

    # Calculate and print the results for both parts
    result_part_one = part_one(input_values)
    print(f"Part 1 Result: {result_part_one}")

    result_part_two = part_two(input_values)
    print(f"Part 2 Result: {result_part_two}")
