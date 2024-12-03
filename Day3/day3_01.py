import re

filename = 'Day3/input.txt'

# Read the input file
with open(filename, 'r') as file:
    data = file.read()

# Part-1: Calculate the sum of products from 'mul(x, y)' patterns
def calculate_multiplications(text):
    """
    Calculates the sum of products from 'mul(x, y)' patterns in the text.

    Args:
        text (str): The input text.

    Returns:
        int: The sum of products.
    """
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, text)

    total_product = sum(int(num1) * int(num2) for num1, num2 in matches)
    return total_product

# Part-2: Calculate the sum with 'do()' and 'don't()' control
def calculate_multiplications_with_control(text):
    """
    Calculates the sum of products from 'mul(x, y)' patterns in the text, 
    considering 'do()' and 'don't()' instructions.

    Args:
        text (str): The input text.

    Returns:
        int: The sum of products.
    """
    pattern = r"(do\(\)|don't\(\))|mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, text)

    mul_enabled = True
    total_product = 0

    for match in matches:
        control, num1, num2 = match[0], match[1], match[2]
        if control == "do()":
            mul_enabled = True
        elif control == "don't()":
            mul_enabled = False
        elif mul_enabled and num1 and num2:
            total_product += int(num1) * int(num2)

    return total_product

# Execute Part-1
part1_result = calculate_multiplications(data)
print(f"Part 1 Result: {part1_result}")

# Execute Part-2
part2_result = calculate_multiplications_with_control(data)
print(f"Part 2 Result: {part2_result}")
