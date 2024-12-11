import os

MAX_STONES = 100_000_000

def main():
    try:
        # Read input file
        with open("Day11/input.txt", "r") as file:
            initial_stones = file.readlines()
        
        num_of_blinks = 75
        
        # Parse the first line
        stone_values = initial_stones[0].strip().split()
        stones = list(map(int, stone_values))

        print("Initial arrangement:")
        print_stones(stones)

        for blink in range(1, num_of_blinks + 1):
            stones = transform_stones(stones)

            print(f"\nAfter {blink} blink{'s' if blink > 1 else ''}:")
            print(f"Number of stones: {len(stones)}")

            if len(stones) > MAX_STONES:
                print(f"Stopped at blink {blink} due to stone count exceeding {MAX_STONES}")
                break

        print(f"\nTotal number of stones after {num_of_blinks} blinks: {len(stones)}")

    except FileNotFoundError:
        print("File not found. Please ensure the input file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_stones(stones):
    # Print only the first 100 stones as a preview
    print(" ".join(map(str, stones[:100])), end="")
    if len(stones) > 100:
        print("... (more stones)")
    print()

def transform_stones(current_stones):
    new_stones = []

    for stone in current_stones:
        if stone == 0:
            new_stones.append(1)
        elif has_even_digits(stone):
            stone_str = str(stone)
            mid = len(stone_str) // 2
            left_stone = int(stone_str[:mid])
            right_stone = int(stone_str[mid:])
            new_stones.append(left_stone)
            new_stones.append(right_stone)
        else:
            new_stones.append(stone * 2024)

        # Limit the number of stones to MAX_STONES
        if len(new_stones) > MAX_STONES:
            new_stones = new_stones[:MAX_STONES]
            break

    return new_stones

def has_even_digits(number):
    return len(str(number)) % 2 == 0

if __name__ == "__main__":
    main()
