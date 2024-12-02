import numpy as np

# Read the input file and parse it into a list of lists of integers
with open("Day2/input.txt") as f:
    arr = [[int(i) for i in l.split()] for l in f]

def is_safe(diffs):
    """
    Check if the differences array is safe.
    A report is safe if all differences are either:
    - Positive and between 1 and 3 inclusive, or
    - Negative and between -3 and -1 inclusive.
    """
    return len(diffs[(diffs > 0) & (diffs <= 3)]) == len(diffs) or \
           len(diffs[(diffs < 0) & (diffs >= -3)]) == len(diffs)

# Initialize counters for Part 1 and Part 2
p1, p2 = 0, 0

# Process each report
for a in arr:
    # Compute differences between consecutive elements
    diffs = np.diff(a)
    
    # Part 1: Check if the report is safe
    if is_safe(diffs):
        p1 += 1
        p2 += 1  # Safe reports also contribute to Part 2
    else:
        # Part 2: Try fixing the report by removing one element
        for i in range(len(a)):
            # Compute differences excluding the i-th element
            fixed_diffs = np.diff(a[:i] + a[i+1:])
            if is_safe(fixed_diffs):
                p2 += 1
                break

# Print the results for Part 1 and Part 2
print(p1)
print(p2)
