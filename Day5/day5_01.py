import os
from collections import defaultdict, deque

def split(string, delimiter):
    """Splits a string by the given delimiter."""
    return [part.strip() for part in string.split(delimiter) if part.strip()]

def trim(string):
    """Trims whitespace from both ends of the string."""
    return string.strip()

def is_update_ordered(update, rules):
    """Checks if an update is ordered according to the rules."""
    index_map = {value: idx for idx, value in enumerate(update)}
    for x, y in rules:
        if x in index_map and y in index_map:
            if index_map[x] > index_map[y]:
                return False
    return True

def topological_sort_update(update, rules):
    """Performs topological sorting on the update according to the rules."""
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    nodes = set(update)

    for x, y in rules:
        if x in nodes and y in nodes:
            graph[x].append(y)
            in_degree[y] += 1
            in_degree.setdefault(x, 0)

    queue = deque([node for node in nodes if in_degree[node] == 0])
    sorted_update = []

    while queue:
        current = queue.popleft()
        sorted_update.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_update) != len(nodes):
        return []  # Cycle detected or unable to sort
    return sorted_update

def get_middle_page(update):
    """Gets the middle page of an update."""
    return update[len(update) // 2]

def main():
    file_path = "Day5/input.txt"

    if not os.path.exists(file_path):
        print(f"Error: Unable to open the file {file_path}")
        return

    with open(file_path, "r") as file:
        content = trim(file.read())

    sections = split(content, "\n\n")
    if len(sections) != 2:
        print("Invalid input format. Expected two sections separated by two newlines.")
        return

    rules_section, updates_section = sections

    rules = []
    for rule_line in split(rules_section, "\n"):
        try:
            x, y = map(int, split(rule_line, "|"))
            rules.append((x, y))
        except ValueError:
            print(f"Invalid rule format: {rule_line}")

    updates = []
    for update_line in split(updates_section, "\n"):
        try:
            updates.append([int(page) for page in split(update_line, ",")])
        except ValueError:
            print(f"Invalid update format: {update_line}")

    correct_updates = []
    middle_pages = []

    for update in updates:
        if is_update_ordered(update, rules):
            correct_updates.append(update)
            middle_pages.append(get_middle_page(update))

    sum_middle_pages = sum(middle_pages)
    print(f"Sum of middle pages for correctly ordered updates: {sum_middle_pages}")

    incorrect_updates = []
    incorrect_middle_pages = []

    for update in updates:
        if not is_update_ordered(update, rules):
            corrected_update = topological_sort_update(update, rules)
            if not corrected_update:
                print("Cycle detected or unable to sort update:", ", ".join(map(str, update)))
                continue
            incorrect_updates.append(corrected_update)
            incorrect_middle_pages.append(get_middle_page(corrected_update))

    sum_incorrect_middle_pages = sum(incorrect_middle_pages)
    print(f"Sum of middle pages for corrected updates: {sum_incorrect_middle_pages}")

if __name__ == "__main__":
    main()
