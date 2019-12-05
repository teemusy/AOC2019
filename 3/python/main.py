import numpy as np
from tqdm import tqdm, trange
from time import time

start_time = time()

# get input data to tuples
puzzle_input = open("../3_input.txt", "r").readlines()
first_wire = tuple(puzzle_input[0].strip().split(","))
second_wire = tuple(puzzle_input[1].strip().split(","))
# then add them to dictionary
wires = (first_wire, second_wire)


"""class MapElement:
    def __init__(self, element, position=None):
        self.element = element
        self.position = position
        # number of steps
        self.steps = []
        # distance from start in manhattan
        self.distance = None"""

# too slow to use object, moving to list
# [name, steps[], distance]


def find_dimensions(input_wires):
    min_hor = 0
    max_hor = 0
    min_ver = 0
    max_ver = 0

    print("Finding out map dimensions")
    for wire in input_wires:
        horizontal = 0
        vertical = 0
        for element in tqdm(wire):
            if "R" in element:
                horizontal += int(element.strip("R"))
            elif "L" in element:
                horizontal -= int(element.strip("L"))
            elif "U" in element:
                vertical += int(element.strip("U"))
            elif "D" in element:
                vertical -= int(element.strip("D"))
            if horizontal > max_hor:
                max_hor = horizontal
            elif horizontal < min_hor:
                min_hor = horizontal
            if vertical > max_ver:
                max_ver = vertical
            elif vertical < min_ver:
                min_ver = vertical

    rows = abs(max_ver - min_ver) + 1
    columns = abs(max_hor - min_hor) + 1
    start_position = (max_ver, -min_hor)

    return {"rows": rows, "columns": columns, "start_position": start_position}


def build_map(input_wiredata, input_wires):

    def build(wire_number, wire_type):
        temp_map = np.full((wiredata["rows"], wiredata["columns"]), "", dtype=object)
        temp_map.fill(".")
        row = input_wiredata["start_position"][0]
        column = input_wiredata["start_position"][1]
        steps = 0
        print("Building wiremaps")
        for element in tqdm(input_wires[wire_number]):
            if "R" in element:
                value = int(element.strip("R"))
                for _ in range(value):
                    steps += 1
                    column += 1
                    temp_map[row][column] = [wire_type, steps, None]
            if "L" in element:
                value = int(element.strip("L"))
                for _ in range(value):
                    steps += 1
                    column -= 1
                    temp_map[row][column] = [wire_type, steps, None]
            if "U" in element:
                value = int(element.strip("U"))
                for _ in range(value):
                    steps += 1
                    row -= 1
                    temp_map[row][column] = [wire_type, steps, None]
            if "D" in element:
                value = int(element.strip("D"))
                for _ in range(value):
                    steps += 1
                    row += 1
                    temp_map[row][column] = [wire_type, steps, None]
        return temp_map

    def compare(input_first, input_second):
        output_map = np.full((wiredata["rows"], wiredata["columns"]), None, dtype=object)
        output_map.fill([".", None, None])
        output_map[input_wiredata["start_position"][0]][input_wiredata["start_position"][1]] = ["O", None, None]
        print("Comparing wiremaps")
        for i in trange(len(input_first)):
            for j in range(len(input_first[0])):
                if input_first[i][j][0] == input_second[i][j][0] and input_first[i][j][0] == "+":
                    dist = abs(input_wiredata["start_position"][0] - i) + abs(input_wiredata["start_position"][1] - j)
                    output_map[i][j] = ["X", [input_first[i][j][1], input_second[i][j][1]], dist]

        return output_map

    wire_marker = "+"
    # build first wiremap
    first_map = build(0, wire_marker)
    # build second wiremap and count steps and compare it to first wiremap at the same time
    second_map = build(1, wire_marker)
    # compare and add crosspoints
    return_map = compare(first_map, second_map)

    return return_map


# find out how large array we need to create
wiredata = find_dimensions(wires)
print("Dimensions:", wiredata)
# create 2d array where to store wiredata
wiremap = np.full((wiredata["rows"], wiredata["columns"]), "", dtype=object)
wiremap.fill([".", None, None])
# add starting position to map as "O"
wiremap[wiredata["start_position"][0]][wiredata["start_position"][1]] = ["O", None, None]
# building wires to map
wiremap = build_map(wiredata, wires)
# find all crossings and their manhattan distances
manhattan_distances = []
step_amounts = []
for i in range(len(wiremap)):
    for j in range(len(wiremap[0])):
        if wiremap[i][j][0] == "X":
            manhattan_distances.append(wiremap[i][j][2])
            step_amounts.append((wiremap[i][j][1]))
        #print(wiremap[i][j][0], end="")
    #print("\n")

crossing_points = np.where(wiremap[0] == "X")
print("Closesti point:", min(manhattan_distances))
smallest_value = min(step_amounts)
smallest_value = smallest_value[0] + smallest_value[1]
print("Smallest amount of steps:", smallest_value)
print("Finished in {} seconds".format(round(time() - start_time), 3))