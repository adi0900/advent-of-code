def parse_input(filename):
    resources = []
    targets = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            line = line.strip()
            if i == 0:
                resources = [x.strip() for x in line.split(',')]
            elif i > 1:
                targets.append(line)

    return resources, targets

def solve1(resources, targets):
    output = []
    memo = {} # memoized
    for target in targets:
        ans = 0
        def recursion(partial_target):
            if partial_target in memo:
                return memo[partial_target]
            if len(partial_target) == 0:
                return True

            possibilities = 0
            for r in resources:
                l = len(r)
                if partial_target.startswith(r): # if partial_target[:l] == r:
                    possibilities += recursion(partial_target[l:])
            
            memo[partial_target] = possibilities
            return possibilities
        
        ans += recursion(target)
        output.append(ans)

    return output

# resources, targets = parse_input('./inputs/day19toy.txt')
resources, targets = parse_input('Day19/input.txt')

ans = solve1(resources, targets)
print(f"Part One - {sum(1 if x>0 else 0 for x in ans)}")
print(f"Part Two - {sum(ans)}")