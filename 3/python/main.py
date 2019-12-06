from tqdm import tqdm, trange
from time import time
from collections import Counter
import numpy as np

start_time = time()

# get input data to tuples
puzzle_input = open("../3_input.txt", "r").readlines()
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
    print("Finding wire locations")
    for element in tqdm(wire_input):
        step_count = int(element.strip("RLUD"))
        for _ in range(step_count):
            if "R" in element:
                location[1] += 1
                wire_list.append((location.copy()))
            if "L" in element:
                location[1] -= 1
                wire_list.append((location.copy()))
            if "U" in element:
                location[0] -= 1
                wire_list.append((location.copy()))
            if "D" in element:
                location[0] += 1
                wire_list.append((location.copy()))

    return wire_list


def compare(first_input, second_input):
    # finding out duplicates
    print("Comparing wires")
    first_input = np.array(first_input)
    second_input = np.array(second_input)
    both_wires = np.concatenate((first_input, second_input), axis=0)
    duplicates, count = np.unique(both_wires, axis=0, return_counts=True)
    duplicates = duplicates[count > 1]
    # create list with steps and manhattan distance
    output_data = []
    print("Finding duplicates")
    for element in tqdm(duplicates):
        index = 0
        steps = 0
        first = False
        second = False
        for row in first_input:
            if np.array_equal(row, element):
                steps = index + 1
                first = True
                break
            index += 1
        index = 0
        for row in second_input:
            if np.array_equal(row, element):
                steps += index + 1
                second = True
                break
            index += 1
        manhattan_distance = abs(element[0]) + abs(element[1])
        if first and second:
            output_data.append((element, manhattan_distance, steps))

    return output_data


# create 2 lists that contain wire locations
first_wire = add_wires(first_wire)
second_wire = add_wires(second_wire)

# compare where wires cross
crossings = compare(first_wire, second_wire)
# find out manhattan distance
closest_crossing = crossings[0][1]
for element in crossings:
    if element[1] < closest_crossing:
        closest_crossing = element[1]
print("Closest crossing point in manhattan distance:", closest_crossing)

# find out closest crossing in steps
lowest_steps = crossings[0][2]
for element in crossings:
    if element[2] < lowest_steps:
        lowest_steps = element[2]

print("Closest crossing in steps:", lowest_steps)
print("Finished in {} seconds".format(round(time() - start_time), 3))
