from time import time
from matplotlib import pyplot, colors
import numpy as np

start_time = time()
f = open("../3_input.txt", "r")
inputs = f.readlines()
first_wire = inputs[0].split(",")
second_wire = inputs[1].split(",")


def find_dimensions(input_list):
    """
    Find max dimensions needed to create list where to write wire locations

    """
    horizontal = 0
    vertical = 0
    max_hor = 0
    max_ver = 0
    min_hor = 0
    min_ver = 0
    for row in input_list:
        if "R" in row:
            horizontal += int(row.strip("R"))
        elif "L" in row:
            horizontal -= int(row.strip("L"))
        elif "U" in row:
            vertical += int(row.strip("U"))
        elif "D" in row:
            vertical -= int(row.strip("D"))
        if horizontal > max_hor:
            max_hor = horizontal
        elif horizontal < min_hor:
            min_hor = horizontal
        if vertical > max_ver:
            max_ver = vertical
        elif vertical < min_ver:
            min_ver = vertical

    return {"max_ver": max_ver, "min_ver": min_ver, "max_hor": max_hor, "min_hor": min_hor}


def create_map(input_1, input_2):
    print("Creating map")
    first = find_dimensions(input_1)
    second = find_dimensions(input_2)

    find_bigger = lambda x, y: x if x > y else y
    find_smaller = lambda x, y: x if x < y else y
    max_hor = find_bigger(first["max_hor"], second["max_hor"])
    min_hor = find_smaller(first["min_hor"], second["min_hor"])
    max_ver = find_bigger(first["max_ver"], second["max_ver"])
    min_ver = find_smaller(first["min_ver"], second["min_ver"])

    width = max_hor - min_hor + 1
    height = max_ver - min_ver + 1

    # map that is filled with zeroes
    wiremap_temp = []
    for _ in range(height):
        map_row = []
        for _ in range(width):
            map_row.append(".")
        wiremap_temp.append(map_row)

    # find starting location where we won't hit the wall
    start_x = -min_hor
    start_y = max_ver

    print("StartX = {}, StartY = {}".format(start_x, start_y))

    # add it to map
    wiremap_temp[start_y][start_x] = "O"

    return [wiremap_temp, {"y": start_y, "x": start_x}]


def create_wires(input_map, first, second):
    print("Creating wires")
    current_location = [input_map[1]["y"], input_map[1]["x"]]

    # second pass overload so we won't count the same wire crossing itself
    def add_wires(wire, second_pass=False):
        for row in wire:
            if "R" in row:
                for _ in range(int(row.strip("R"))):
                    current_location[1] += 1
                    if input_map[0][current_location[0]][current_location[1]] == "+" and second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "X"
                    elif second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "-"
                    else:
                        input_map[0][current_location[0]][current_location[1]] = "+"
            if "L" in row:
                for _ in range(int(row.strip("L"))):
                    current_location[1] -= 1
                    if input_map[0][current_location[0]][current_location[1]] == "+" and second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "X"
                    elif second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "-"
                    else:
                        input_map[0][current_location[0]][current_location[1]] = "+"
            if "U" in row:
                for _ in range(int(row.strip("U"))):
                    current_location[0] -= 1
                    if input_map[0][current_location[0]][current_location[1]] == "+" and second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "X"
                    elif second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "-"
                    else:
                        input_map[0][current_location[0]][current_location[1]] = "+"
            if "D" in row:
                for _ in range(int(row.strip("D"))):
                    current_location[0] += 1
                    if input_map[0][current_location[0]][current_location[1]] == "+" and second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "X"
                    elif second_pass:
                        input_map[0][current_location[0]][current_location[1]] = "-"
                    else:
                        input_map[0][current_location[0]][current_location[1]] = "+"

    add_wires(first)
    current_location = [input_map[1]["y"], input_map[1]["x"]]
    add_wires(second, True)

    return input_map


def find_x_locations(input_map, return_x=False):
    print("Finding x locations")
    x_locations = []
    start_location = []
    for y in range(len(input_map[0])):
        for x in range(len(input_map[0][0])):
            if input_map[0][y][x] == "X":
                x_locations.append((x, y))
            elif input_map[0][y][x] == "O":
                start_location = (x, y)
    if return_x:
        return x_locations

    print("Finding manhattan distances")
    manhattan_distances = []
    lowest = 10000000
    lovest_position = []
    for row in x_locations:
        manhattan_distances.append(find_distance(start_location, row))
        if find_distance(start_location, row) < lowest:
            lovest_position = row

    print(manhattan_distances)
    print("Lowest manhattan distance: {}".format(min(manhattan_distances)))

    return lovest_position


def find_distance(start, end):

    return abs(start[0]-end[0]) + abs(start[1]-end[1])


def create_visual_map(input_data, override_colors=False):
    index = 0
    # red for start and finish
    for _ in input_data:
        input_data[index] = [0 if element == "X" else element for element in input_data[index]]
        input_data[index] = [1 if element == "." else element for element in input_data[index]]
        input_data[index] = [2 if element == "+" else element for element in input_data[index]]
        input_data[index] = [3 if element == "-" else element for element in input_data[index]]
        input_data[index] = [4 if element == "O" else element for element in input_data[index]]
        input_data[index] = [5 if element == "G" else element for element in input_data[index]]
        index += 1
    cmap = colors.ListedColormap(['blue', 'white', 'green', 'black', 'red', 'red'])
    rm = np.array(input_data)
    if override_colors:
        pyplot.imshow(rm, interpolation='nearest')
    else:
        pyplot.imshow(rm, interpolation='nearest', cmap=cmap)
    pyplot.title('Wiregrid')
    pyplot.tight_layout()
    pyplot.grid()
    pyplot.show()


def find_shortest_path(input_map, location):
    start_x = input_map[1]["x"]
    start_y = input_map[1]["y"]
    end_x = location[0]
    end_y = location[1]

    distance_map = [[0 for x in range(len(input_map[0][0]))] for y in range(len(input_map[0]))]

    input_map = input_map[0]
    # solve for first wire "+"
    current_steps = 0
    found_goal = False
    # add starting and ending point
    distance_map[start_y][start_x] = 1
    current_loc = [start_y, start_x]

    print("starting loc", current_loc)
    while not found_goal:
        # check north
        if mover(current_loc, "north"):
            if distance_map[current_loc[0] - 1][current_loc[1]] and input_map[current_loc[0] - 1][current_loc[1]] == "+":
                current_loc = mover(current_loc, "north")
                distance_map[current_loc[0] - 1][current_loc[1]] = distance_map[current_loc[0]][current_loc[1]] + 1
        # check south
        if mover(current_loc, "south"):
            if distance_map[current_loc[0] + 1][current_loc[1]] and input_map[current_loc[0] + 1][current_loc[1]] == "+":
                current_loc = mover(current_loc, "south")
                distance_map[current_loc[0] + 1][current_loc[1]] = distance_map[current_loc[0]][current_loc[1]] - 1

        if current_loc == [end_x, end_y]:
            found_goal = True

    return distance_map


def mover(loc, direction):
    if direction == "north":
        loc[0] -= 1
    elif direction == "south":
        loc[0] +=1
    elif direction == "west":
        loc[1] -= 1
    elif direction == "east":
        loc[1] += 1

    if loc[0] < 0 or loc[1] < 0:
        return False
    else:
        return loc



print("Finding dimensions")
print(find_dimensions(first_wire))
print(find_dimensions(second_wire))

wiremap = create_map(first_wire, second_wire)
#print('\n'.join(map(''.join, create_map(first_wire, second_wire)[0])))
wiremap = create_wires(wiremap, first_wire, second_wire)
#print('\n'.join(map(''.join, wiremap[0])))
goal = find_x_locations(wiremap)
print("Goal location:", goal)
wiremap[0][goal[1]][goal[0]] = "G"

# crate list of x locations and add goal location as one
#x_loc = find_x_locations(wiremap, True)
#x_loc.append(goal)
#print("X locations:", x_loc)

"""shortest_paths = []
print("finding shortest paths")
for row in x_loc:
    shortest_paths.append(find_shortest_path(wiremap, row))

print(shortest_paths)"""

print("Finished in {} seconds".format(round(time() - start_time), 3))
print("Creating visual map")
#create_visual_map(wiremap[0])
#create_visual_map(shortest_paths[0], True)
