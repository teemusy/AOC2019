import numpy as np
from tqdm import tqdm

# get input data to tuples
puzzle_input = open("../3_test.txt", "r").readlines()
first_wire = tuple(puzzle_input[0].strip().split(","))
second_wire = tuple(puzzle_input[1].strip().split(","))
# then add them to dictionary
wires = (first_wire, second_wire)


class MapElement:
    def __init__(self, element, position=None):
        self.element = element
        self.position = position
        # number of steps
        self.steps = []
        # distance from start in manhattan
        self.distance = None


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


def build_map(input_wiremap, input_wiredata, input_wires):

    def build(wire_number, wire_type):
        temp_map = input_wiremap
        row = input_wiredata["start_position"][0]
        column = input_wiredata["start_position"][1]
        steps = 0
        for element in input_wires[wire_number]:
            if "R" in element:
                value = int(element.strip("R"))
                for _ in range(value):
                    steps += 1
                    column += 1
                    temp_map[row][column] = MapElement(wire_type, (row, column))
                    temp_map[row][column].steps.append(steps)
            if "L" in element:
                value = int(element.strip("L"))
                for _ in range(value):
                    steps += 1
                    column -= 1
                    temp_map[row][column] = MapElement(wire_type, (row, column))
                    temp_map[row][column].steps.append(steps)
            if "U" in element:
                value = int(element.strip("U"))
                for _ in range(value):
                    steps += 1
                    row -= 1
                    temp_map[row][column] = MapElement(wire_type, (row, column))
                    temp_map[row][column].steps.append(steps)
            if "D" in element:
                value = int(element.strip("D"))
                for _ in range(value):
                    steps += 1
                    row += 1
                    temp_map[row][column] = MapElement(wire_type, (row, column))
                    temp_map[row][column].steps.append(steps)
        return temp_map

    def compare(input_first, input_second):
        output_map = np.full((wiredata["rows"], wiredata["columns"]), MapElement("."), dtype=object)
        for i in range(len(input_first)):
            for j in range(len(input_first[0])):
                if input_first[i][j].element == input_second[i][j].element:
                    output_map[i][j] = MapElement("+", (i, j))
                    output_map[i][j].steps.append(input_first[i][j].steps)
                    output_map[i][j].steps.append(input_second[i][j].steps)
                    output_map[i][j].distance = abs(input_wiredata["start_position"][0] -
                                                    input_wiredata["start_position"][1] +
                                                    output_map[i][j].position[0] - output_map[i][j].position[1])
                elif input_first[i][j].element != ".":
                    output_map[i][j] = input_first[i][j]
                elif input_second[i][j].element != ".":
                    output_map[i][j] = input_second[i][j]

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
wiremap = np.full((wiredata["rows"], wiredata["columns"]), MapElement("."), dtype=object)
# add starting position to map as "O"
wiremap[wiredata["start_position"][0]][wiredata["start_position"][1]] = MapElement("O")
# building wires to map
wiremap = build_map(wiremap, wiredata, wires)
# find all crossings and their manhattan distances
#crossing_points = np.where(wiremap.element == "X")
