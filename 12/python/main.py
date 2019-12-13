import numpy as np
import copy
from time import time
from math import gcd
from functools import reduce


class Moon:
    def __init__(self, name, position):
        self.name = name
        self.position = np.array(position)
        self.velocity = np.array([0, 0, 0])
        self.start = np.array(position)


def main():
    start_time = time()
    #moon_list = [Moon("Io", [-1, 0, 2]), Moon("Europa", [2, -10, -7]), Moon("Ganymede", [4, -8, 8]), Moon("Callisto", [3, 5, -1])]
    # 179 after 10 steps, 2772
    #moon_list = [Moon("Io", [-8, -10, 0]), Moon("Europa", [5, 5, 10]), Moon("Ganymede", [2, -7, 3]), Moon("Callisto", [9, -8, -3])]
    # 1940 after 100, 4686774924
    moon_list = [Moon("Io", [-6, -5, -8]), Moon("Europa", [0, -3, -13]), Moon("Ganymede", [-15, 10, -11]), Moon("Callisto", [-3, -8, 3])]
    # input
    steps = 1000

    copy_moon_list = copy.deepcopy(moon_list)
    total = calculate_kinetical(copy_moon_list, steps)
    print("Total energy in system after {} steps: {}".format(steps, total))

    copy_moon_list = copy.deepcopy(moon_list)
    pattern = find_pattern(copy_moon_list)
    pattern = [pattern[0][0], pattern[1][0], pattern[2][0]]
    common = find_smallest_common_denominator(pattern)
    print("Steps needed to return to starting position and velocity:", common)
    print("Time used:", time() - start_time)


def find_smallest_common_denominator(pattern):
    return reduce(lambda a, b: a * b // gcd(a, b), pattern)


def find_pattern(moon_list):
    # find how many steps it takes to orbit for each moon
    steps = 0
    found = [[], [], []]
    while True:
        copy_moon_list = copy.deepcopy(moon_list)
        for i in range(len(moon_list)):
            velocity = [0, 0, 0]
            for j in range(len(moon_list)):
                if i == j:
                    continue
                # calculate velocity
                for k in range(len(moon_list[i].position)):
                    if copy_moon_list[i].position[k] > copy_moon_list[j].position[k]:
                        velocity[k] -= 1
                    elif copy_moon_list[i].position[k] < copy_moon_list[j].position[k]:
                        velocity[k] += 1

            moon_list[i].velocity += velocity
            # apply velocity to position
            moon_list[i].position += moon_list[i].velocity
        steps += 1
        for n in range(len(moon_list[0].position)):
            if moon_list[0].position[n] == moon_list[0].start[n] and moon_list[0].velocity[n] == 0 \
                    and moon_list[1].position[n] == moon_list[1].start[n] and moon_list[1].velocity[n] == 0 \
                    and moon_list[2].position[n] == moon_list[2].start[n] and moon_list[2].velocity[n] == 0 \
                    and moon_list[3].position[n] == moon_list[3].start[n] and moon_list[3].velocity[n] == 0:
                found[n].append(steps)

        if steps % 10000 == 0 and steps > 0:
            print("Current step:", steps)
        if steps > 500000 or (len(found[0]) > 0 and len(found[1]) > 0 and len(found[2]) > 0):
            return found


def calculate_kinetical(moon_list, steps):

    for _ in range(steps):
        copy_moon_list = copy.deepcopy(moon_list)
        for i in range(len(moon_list)):
            velocity = [0, 0, 0]
            for j in range(len(moon_list)):
                if i == j:
                    continue
                # calculate velocity
                for k in range(len(moon_list[i].position)):
                    if copy_moon_list[i].position[k] > copy_moon_list[j].position[k]:
                        velocity[k] -= 1
                    elif copy_moon_list[i].position[k] < copy_moon_list[j].position[k]:
                        velocity[k] += 1

            moon_list[i].velocity += velocity
            # apply velocity to position
            moon_list[i].position += moon_list[i].velocity

    # calculate total energy
    total = 0
    for element in moon_list:
        pos = 0
        vel = 0
        for position in element.position:
            pos += abs(position)
        for velocity in element.velocity:
            vel += abs(velocity)
        total += pos * vel
    return total


if __name__ == '__main__':
    main()
