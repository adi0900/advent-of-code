from collections import deque, defaultdict
from itertools import product

def read_input(file_path):
    """Read input data from a file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

class Garden:
    def __init__(self, input_data):
        self.grid = self.parse_input(input_data)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
    
    @staticmethod
    def parse_input(input_data):
        return [list(line) for line in input_data.splitlines()]
    
    def get_plant_types(self):
        plants = set()
        for row in self.grid:
            plants.update(row)
        return plants
    
    def find_plots(self, plant_type):
        visited = set()
        plots = []

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in visited and self.grid[r][c] == plant_type:
                    plot = self._explore_plot(r, c, plant_type, visited)
                    plots.append(plot)

        return plots

    def _explore_plot(self, r, c, plant_type, visited):
        plot = []
        queue = deque([(r, c)])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()
            if (x, y) in visited or not self._is_valid(x, y) or self.grid[x][y] != plant_type:
                continue
            visited.add((x, y))
            plot.append((x, y))

            for dx, dy in directions:
                queue.append((x + dx, y + dy))
        
        return plot
    
    def _is_valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def calculate_area_and_perimeter(self, plot):
        area = len(plot)
        perimeter = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for x, y in plot:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not self._is_valid(nx, ny) or self.grid[nx][ny] != self.grid[x][y]:
                    perimeter += 1

        return area, perimeter

def part_1(input_data):
    garden = Garden(input_data)
    total = 0

    for plant_type in garden.get_plant_types():
        plots = garden.find_plots(plant_type)
        for plot in plots:
            area, perimeter = garden.calculate_area_and_perimeter(plot)
            total += area * perimeter
    
    return total

def part_2(input_data):
    def find_sides(plot, mask):
        sides = 0
        for plant in plot:
            sides += count_corners(plant, mask, corner_patterns)
        return sides

    garden = Garden(input_data)
    total = 0

    for plant_type in garden.get_plant_types():
        plots = garden.find_plots(plant_type)
        for plot in plots:
            area = len(plot)
            mask = create_mask(plot, garden.rows, garden.cols)
            sides = find_sides(plot, mask)
            total += area * sides

    return total

def create_mask(plot, rows, cols):
    mask = [[0] * cols for _ in range(rows)]
    for x, y in plot:
        mask[x][y] = 1
    return mask

def count_corners(plant, mask, corner_patterns):
    x, y = plant
    count = 0
    for pattern in corner_patterns:
        if is_corner(x, y, mask, pattern):
            count += 1
    return count

def is_corner(x, y, mask, pattern):
    for dx, dy in pattern:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < len(mask) and 0 <= ny < len(mask[0])) or mask[nx][ny] != 1:
            return False
    return True

# Corner patterns for different corner types
corner_patterns = [
    [(-1, 0), (-1, 1), (0, 1)],  # Top-right
    [(0, -1), (-1, -1), (-1, 0)],  # Top-left
    [(1, 0), (1, -1), (0, -1)],  # Bottom-left
    [(0, 1), (1, 1), (1, 0)],  # Bottom-right
]

if __name__ == "__main__":
    file_path = "Day12/input.txt"  # Replace with your file path
    input_data = read_input(file_path)
    
    print("Part 1:", part_1(input_data))
    print("Part 2:", part_2(input_data))
