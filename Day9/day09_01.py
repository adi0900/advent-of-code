from time import perf_counter
from typing import List, Dict, Union

# Define the D9Type as a dictionary
D9Type = Dict[str, Union[int, str]]

def solution(input: List[str]) -> None:
    numbers = list(map(int, input[0]))

    def run(part: int) -> int:
        t0 = perf_counter()
        data: List[D9Type] = []
        id_counter = 0

        # Populate the data list
        for i, f in enumerate(numbers):
            if i % 2 == 0:
                data.append({"id": id_counter, "size": f, "type": "file"})
                id_counter += 1
            else:
                data.append({"id": 0, "size": f, "type": "space"})

        nearest_space_id = 1
        for i in range(len(data) - 1, -1, -1):
            if part == 2:
                nearest_space_id = 1
            if nearest_space_id > i:
                break

            if data[i]["type"] == "file":
                file = data[i]
                remaining_size = file["size"]

                while remaining_size > 0 and nearest_space_id < i:
                    if data[nearest_space_id]["type"] == "space":
                        space = data[nearest_space_id]

                        if space["size"] > remaining_size:
                            space["size"] -= remaining_size
                            data.insert(nearest_space_id, {"id": file["id"], "size": remaining_size, "type": "file"})
                            file["id"] = 0
                            file["type"] = "space"
                            remaining_size = 0

                        elif space["size"] == remaining_size:
                            remaining_size = 0
                            space["id"] = file["id"]
                            space["type"] = "file"
                            file["id"] = 0
                            file["type"] = "space"

                        elif part == 1:  # checking of the smaller sizes is only in part 1
                            remaining_size -= space["size"]
                            space["type"] = file["type"]
                            space["id"] = file["id"]
                            file["size"] -= space["size"]

                    nearest_space_id += 1

        sum_result = 0
        i = 0

        for f in data:
            if f["type"] == "space":
                i += f["size"]
                continue

            condition = i + f["size"]
            while i < condition:
                sum_result += f["id"] * i
                i += 1

        t1 = perf_counter()
        print(f"Execution time: {t1 - t0:.6f} seconds.")
        return sum_result

    print("Part 1", run(1))
    print("Part 2", run(2))

# Read input from file
with open("Day9/input.txt", "r") as file:
    input_data = [file.read().strip()]

solution(input_data)