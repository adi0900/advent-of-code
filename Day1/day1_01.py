import numpy as np

# Initialize empty lists for X and Y
X = []
Y = []

# Read data from the file
with open("day1.txt", "r") as file:
    for row in file:
        x, y = row.split()
        X.append(int(x))
        Y.append(int(y))

# Convert lists to numpy arrays
X = np.array(X)
Y = np.array(Y)

# Sort the arrays
x_sort = np.sort(X)
y_sort = np.sort(Y)

# Calculate the absolute difference at each position
dist = np.abs(x_sort - y_sort)

# Find the total distance
total_dist = np.sum(dist)

# Print the total distance
print("Total distance:", total_dist)
