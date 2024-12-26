import heapq
import copy

def parse_input(filename, size=7):
    grid = []
    for _ in range(size):
        grid.append(['.']*size)
    
    obstacles = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = line.strip().split(',')
            obstacles.append((int(y),int(x)))

    return grid, obstacles


def solve1(grid, obs, step=12):
    N = len(grid)
    M = len(grid[0])
    def is_inside(i, j):
        return 0 <= i < N and 0 <= j < M

    for i in range(step):
        grid[obs[i][0]][obs[i][1]] = '#'

    h = [(0,0,0,-1,0)] # dist,curi,curj,previ,prevj
    heapq.heapify(h)
    visited = set()

    while h:
        d,i,j,pi,pj = heapq.heappop(h)
        di = i-pi
        dj = j-pj
        
        if not is_inside(i,j) or (i,j,pi,pj) in visited:
            continue
        if grid[i][j] == '#':
            continue
        if i == N-1 and j == M-1:
            return d
        # print(d,i,j,pi,pj,'|',di,dj)
        visited.add((i,j,pi,pj))
        for (ii,jj) in [(-1,0),(1,0),(0,1),(0,-1)]:
            if (ii,jj) == (-di,-dj): continue
            heapq.heappush(h, (d+1, i+ii, j+jj, i, j))

    raise ValueError('Check the grid :(')

def solve2(grid, obs):
    left = 0
    right = len(obs)-1
    while (left < right):
        mid = (left + right) // 2
        try:
            ans = solve1(copy.deepcopy(grid), obs, step=mid)
            left = mid+1
            print(mid, ans)
        except ValueError:
            right = mid

    y, x = obs[left-1]
    return f"{x},{y}"

        

grid, obstacles = parse_input('Day18/input.txt', size=71)
# grid, obstacles = parse_input('./inputs/day18toy.txt')

ans = solve1(copy.deepcopy(grid), obstacles, step=1024)
# ans = solve1(copy.deepcopy(grid), obstacles)
print(f'Part one - {ans}')
ans = solve2(grid, obstacles)
print(f'Part two - {ans}')