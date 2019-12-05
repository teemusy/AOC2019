from tqdm import tqdm, trange
from time import time
import numpy as np

start_time = time()

# get input data to tuples
puzzle_input = open("../3_test.txt", "r").readlines()
first_wire = tuple(puzzle_input[0].strip().split(","))
second_wire = tuple(puzzle_input[1].strip().split(","))
# then add them to dictionary
wires = (first_wire, second_wire)


def add_wires(wire_input):
    """
    Adds wire locations to list
    Args:
        wire_input: tuple that contains wire addresses

    Returns: List that contains wire locations and step count

    """
    wire_list = []
    # row, column
    location = [0, 0]
    steps = 0
    print("Finding wire locations")
    for element in tqdm(wire_input):
        step_count = int(element.strip("RLUD"))
        for _ in range(step_count):
            if "R" in element:
                location[1] += 1
                steps += 1
                wire_list.append((location.copy(), steps))
            if "L" in element:
                location[1] -= 1
                steps += 1
                wire_list.append((location.copy(), steps))
            if "U" in element:
                location[0] -= 1
                steps += 1
                wire_list.append((location.copy(), steps))
            if "D" in element:
                location[0] += 1
                steps += 1
                wire_list.append((location.copy(), steps))

    return wire_list


def compare(first_input, second_input):
    found_elements = []
    # finding out duplicates
    print("Comparing wires")
    first_input = np.array(first_input)
    second_input = np.array(second_input)
    testi = np.logical_and.reduce(first_input == second_input, axis=1)



    """manhattan_distance = abs(0 - first_input[i][0][0]) + abs(0 - first_input[i][0][1])
    found_elements.append((first_input[i][0], (first_input[i][1], second_input[j][1]), manhattan_distance))"""

    return testi


# create 2 lists that contain wire locations and step count
first_wire = add_wires(first_wire)
second_wire = add_wires(second_wire)



print(first_wire)
# compare where wires cross
crossings = compare(first_wire, second_wire)
print(crossings)
exit()
# find out manhattan distance
closest_crossing = crossings[0][2]
for element in crossings:
    if element[2] < closest_crossing:
        closest_crossing = element[2]
print("Closest crossing point in manhattan distance:", closest_crossing)

# find out closest crossing in steps
lovest_steps = crossings[0][1][0] + crossings[0][1][1]
for element in crossings:
    if element[1][0] + element[1][1] < lovest_steps:
        lovest_steps = element[1][0] + element[1][1]

print("Closest crossing in steps:", lovest_steps)

print("Finished in {} seconds".format(round(time() - start_time), 3))