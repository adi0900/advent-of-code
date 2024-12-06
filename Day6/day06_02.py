class D6Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class D6Direction(D6Point):
    pass

class D6MapPoint(D6Point):
    def __init__(self, x: int, y: int, type: str, visited: bool = False):
        super().__init__(x, y)
        self.type = type
        self.visited = visited

class Solution:
    def __init__(self, input_lines):
        self.m = []
        self.starting_position = D6Point(0, 0)
        self.height = len(input_lines)
        self.width = len(input_lines[0])
        self.visited = 0
        self.possible_obstructions = 0
        self.obstruction_map = {}

        # Parse input
        for y, row in enumerate(input_lines):
            for x, cell_type in enumerate(row):
                if len(self.m) <= x:
                    self.m.append([])
                point = D6MapPoint(x, y, cell_type)
                self.m[x].append(point)
                if cell_type == "^":
                    self.starting_position = point
                    point.type = "."

    def is_out_of_bounds(self, point: D6Point):
        return point.x < 0 or point.x >= self.width or point.y < 0 or point.y >= self.height

    def turn_right(self, direction: D6Direction):
        if direction.y == -1:
            return D6Direction(1, 0)
        if direction.y == 1:
            return D6Direction(-1, 0)
        if direction.x == 1:
            return D6Direction(0, 1)
        return D6Direction(0, -1)

    def get_key(self, point: D6Point, direction: D6Direction = None):
        if direction:
            return f"{point.x};{point.y}|{direction.x};{direction.y}"
        return f"{point.x};{point.y}"

    def move(self, position: D6Point, direction: D6Direction):
        new_pos = D6Point(position.x + direction.x, position.y + direction.y)

        if self.is_out_of_bounds(new_pos):
            return False

        map_point = self.m[new_pos.x][new_pos.y]

        if map_point.type == ".":
            if not map_point.visited:
                self.visited += 1
                map_point.visited = True

                if not self.obstruction_map.get(self.get_key(new_pos)) and self.check_for_obstruction_placement(position, direction):
                    self.possible_obstructions += 1
                    self.obstruction_map[self.get_key(new_pos)] = True

            return new_pos, direction

        elif map_point.type == "#":
            return position, self.turn_right(direction)

        else:
            raise ValueError("Unexpected map point type.")

    def check_for_nearest_obstruction(self, pos: D6Point, direction: D6Direction, fake_obstruction: D6Point = None):
        new_pos = D6Point(pos.x, pos.y)

        while True:
            new_pos.x += direction.x
            new_pos.y += direction.y

            if self.is_out_of_bounds(new_pos):
                return False

            if self.m[new_pos.x][new_pos.y].type == "#":
                return D6Point(new_pos.x - direction.x, new_pos.y - direction.y)

            if fake_obstruction and fake_obstruction.x == new_pos.x and fake_obstruction.y == new_pos.y:
                return D6Point(new_pos.x - direction.x, new_pos.y - direction.y)

    def check_for_obstruction_placement(self, position: D6Point, direction: D6Direction):
        new_obstruction_position = D6Point(position.x + direction.x, position.y + direction.y)

        if self.is_out_of_bounds(new_obstruction_position):
            return False

        if self.m[new_obstruction_position.x][new_obstruction_position.y].type == "#":
            return False

        new_pos = D6Point(position.x, position.y)
        new_dir = D6Direction(direction.x, direction.y)

        obstruction_hit_map = {}

        while True:
            new_pos = self.check_for_nearest_obstruction(new_pos, new_dir, new_obstruction_position)

            if not new_pos:
                return False

            key = self.get_key(D6Point(new_pos.x + new_dir.x, new_pos.y + new_dir.y), new_dir)

            if obstruction_hit_map.get(key):
                return True

            obstruction_hit_map[key] = True
            new_dir = self.turn_right(new_dir)

    def solve(self):
        position = D6Point(self.starting_position.x, self.starting_position.y)
        direction = D6Direction(0, -1)

        moved = self.move(position, direction)

        while moved:
            position, direction = moved
            moved = self.move(position, direction)

        print("Start:", vars(self.starting_position))
        print("Obstacle on start:", self.get_key(self.starting_position) in self.obstruction_map)

        if self.get_key(self.starting_position) in self.obstruction_map:
            self.possible_obstructions -= 1
            print("Reduced 1 from possible obstructions")

        print("Part 1:", self.visited)
        print("Part 2:", self.possible_obstructions)

# Function to read input from a file
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Example usage
file_path = 'Day6/input.txt'  # Specify your input file path here
input_lines = read_input_file(file_path)
solution = Solution(input_lines)
solution.solve()
