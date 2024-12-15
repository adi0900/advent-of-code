import re
import numpy as np

def parse_input(filename):
    positions = []
    directions = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            p_match = re.search(r"p=(-?\d+),(-?\d+)", line)
            v_match = re.search(r"v=(-?\d+),(-?\d+)", line)

            p_x, p_y = int(p_match.group(1)), int(p_match.group(2))
            v_x, v_y = int(v_match.group(1)), int(v_match.group(2))

            positions.append((p_x, p_y))
            directions.append((v_x, v_y))

    return positions, directions

MAP_WIDTH = 101
MAP_HEIGHT = 103
TIMESTEPS = 100

def mod_calc(a, b):
    result = a % b
    if result < 0:
        result += b
    return result

def solve1(positions, directions):
    final_positions = list()
    for position, direction in zip(positions, directions):
        x, y = position
        dx, dy = direction
        x = mod_calc((x + TIMESTEPS * dx), MAP_WIDTH)
        y = mod_calc((y + TIMESTEPS * dy), MAP_HEIGHT)
        final_positions.append( (x,y) )
    
    result = [0,0,0,0] #q1,...q4

    for fp in final_positions:
        if fp[0] > MAP_WIDTH//2 and fp[1] > MAP_HEIGHT//2:
            result[0] += 1
        elif fp[0] < MAP_WIDTH//2 and fp[1] > MAP_HEIGHT//2:
            result[1] += 1
        elif fp[0] < MAP_WIDTH//2 and fp[1] < MAP_HEIGHT//2:
            result[2] += 1
        elif fp[0] > MAP_WIDTH//2 and fp[1] < MAP_HEIGHT//2:
            result[3] += 1

    return result[0] * result[1] * result[2] * result[3]

def solve2(positions, directions):
    final_positions = list()

    best_xt = 0
    best_yt = 0
    min_std_x = 1e5
    min_std_y = 1e5
    # find smallest stdev because tree is "concentrated"
    for t in range(max(MAP_WIDTH, MAP_HEIGHT)):
        X = np.zeros(len(positions))
        Y = np.zeros(len(positions))
        for i, (position, direction) in enumerate(zip(positions, directions)):
            x, y = position
            dx, dy = direction
            X[i] = mod_calc((x + t * dx), MAP_WIDTH)
            Y[i] = mod_calc((y + t * dy), MAP_HEIGHT)
        
        if X.std() < min_std_x:
            min_std_x = X.std()
            best_xt = t
        if Y.std() < min_std_y:
            min_std_y = Y.std()
            best_yt = t
        # final_positions.append( (x,y) 
    print(best_xt, best_yt)

    # https://www.reddit.com/r/adventofcode/comments/1hdvhvu/comment/m1zws1g/
    # crazy application of Chinese Remainder Thm
    return best_xt + ((pow(MAP_WIDTH, -1, MAP_HEIGHT)*(best_yt-best_xt)) % MAP_HEIGHT) * MAP_WIDTH

positions, directions = parse_input('Day14/input.txt')
ans1 = solve1(positions, directions)
print('part one -', ans1)
ans2 = solve2(positions, directions)
print('part two -', ans2)