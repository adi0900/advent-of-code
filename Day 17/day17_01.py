import re

# Function to extract all integers from a text string, including negative numbers.
def extract_integers(text):
    """
    Extract all integers (including negative) from a given text string.
    
    Args:
        text (str): Input text to extract integers from.
    
    Returns:
        list: List of integers found in the text.
    """
    return [int(x) for x in re.findall(r"-?\d+", text)]


# Function to read the input file, which contains register values and program instructions.
def read_input_file(file_path):
    """
    Read and parse the input file containing register values and program instructions.
    
    Args:
        file_path (str): Path to the input file.
    
    Returns:
        tuple: A tuple containing (register_values, program_instructions)
    """
    with open(file_path, "r") as file:
        raw_text = file.read().strip()
    
    # Split input into register values and program instructions
    raw_registers, raw_program = raw_text.split("\n\n")
    
    # Extract register values (as integers)
    register_values = extract_integers(raw_registers)
    
    # Extract program instructions (as integers after ':' symbol)
    program_instructions = [int(x) for x in raw_program.split(":")[1].strip().split(",")]
    
    return register_values, program_instructions


# Function to resolve the value of an operand (register or immediate value).
def resolve_operand(registers, operand):
    """
    Resolve the value of the operand based on its type.
    
    Args:
        registers (list): List of register values [A, B, C].
        operand (int): Operand value.
    
    Returns:
        int: The resolved value of the operand.
    """
    if operand < 4:
        return operand  # Direct value if operand is less than 4
    elif operand == 4:
        return registers[0]  # Value of register A
    elif operand == 5:
        return registers[1]  # Value of register B
    elif operand == 6:
        return registers[2]  # Value of register C
    return None


# Function to execute a single instruction in the program.
def execute_instruction(registers, instruction_pointer, program):
    """
    Execute a single instruction in the program.
    
    Args:
        registers (list): List of register values [A, B, C].
        instruction_pointer (int): Current position in the program.
        program (list): List of program instructions.
    
    Returns:
        tuple: Updated register values and instruction pointer.
    """
    # Get the current instruction's opcode and operand
    opcode = program[instruction_pointer]
    operand = program[instruction_pointer + 1]
    operand_value = resolve_operand(registers, operand)
    
    # Perform different operations based on the opcode
    if opcode == 0:
        registers[0] //= pow(2, operand_value)  # A = A // 2^operand_value
    elif opcode == 1:
        registers[1] ^= operand  # B = B XOR operand
    elif opcode == 2:
        registers[1] = operand_value % 8  # B = operand_value % 8
    elif opcode == 3:
        if registers[0] != 0:
            instruction_pointer = operand  # Jump to the operand location if A != 0
            return None, registers, instruction_pointer
    elif opcode == 4:
        registers[1] ^= registers[2]  # B = B XOR C
    elif opcode == 5:
        return operand_value % 8, registers, instruction_pointer + 2  # Output the result
    elif opcode == 6:
        registers[1] = registers[0] // pow(2, operand_value)  # B = A // 2^operand_value
    elif opcode == 7:
        registers[2] = registers[0] // pow(2, operand_value)  # C = A // 2^operand_value
    
    # Move to the next instruction
    return None, registers, instruction_pointer + 2


# Function to run the entire program and collect output values.
def run_program(registers, program):
    """
    Execute the entire program and collect output values.
    
    Args:
        registers (list): Initial register values [A, B, C].
        program (list): List of program instructions.
    
    Returns:
        list: Collected output values during program execution.
    """
    instruction_pointer = 0
    output_values = []
    
    # Continue executing instructions until we reach the end of the program
    while instruction_pointer < len(program) - 1:
        output, registers, instruction_pointer = execute_instruction(registers, instruction_pointer, program)
        
        if output is not None:
            output_values.append(output)  # Collect output
    
    return output_values


# Function to find the optimal input that generates the desired output in the program.
def find_optimal_input(program, cursor, current_value):
    """
    Recursively find the best input that generates a specific program output.
    
    Args:
        program (list): List of program instructions.
        cursor (int): Current position in the program to match.
        current_value (int): Current accumulated value.
    
    Returns:
        int or None: Best input value that matches program requirements.
    """
    # Try all possible values (0 to 7) for the current input
    for candidate in range(8):
        # Run the program with the current input value
        if run_program([current_value * 8 + candidate, 0, 0], program) == program[cursor:]:
            if cursor == 0:
                return current_value * 8 + candidate  # If we are at the start, return the value
            
            # Otherwise, continue searching recursively
            result = find_optimal_input(program, cursor - 1, current_value * 8 + candidate)
            if result is not None:
                return result
    
    return None


# Main function to solve the problem for both parts.
def solve(registers, program):
    """
    Solve the problem by running the program and finding the best input.
    
    Args:
        registers (list): Initial register values [A, B, C].
        program (list): List of program instructions.
    """
    # Part 1: Print program output
    print("Part 1:", ",".join(map(str, run_program(registers, program))))
    
    # Part 2: Find the best input and print it
    best_input = find_optimal_input(program, len(program) - 1, 0)
    print("Part 2:", best_input)


# Main entry point
if __name__ == "__main__":
    registers, program = read_input_file("./Day 17/input.txt")  # Read input file
    solve(registers, program)  # Solve the problem
