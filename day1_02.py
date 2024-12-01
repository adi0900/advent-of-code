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

# Count the frequency of each number in the sorted list
frequencies = []
for x in x_sort:
    frequency = np.sum(y_sort == x)
    frequencies.append(frequency)

# Convert the frequencies list to a numpy array
frequencies = np.array(frequencies)

# Calculate the similarity by multiplying the number and its frequency
similarity = np.multiply(x_sort, frequencies)

# Find the total similarity
total_similarity = np.sum(similarity)

# Print the total similarity
print("Total similarity:", total_similarity)
