from itertools import permutations
from tqdm import tqdm
import math
import numpy as np


class Asteroid:

    def __init__(self, position):
        self.position = position
        self.detected = 0
        self.blocking = []


def main():
    with open('../10_input.txt') as f:
        input_asteroids = [line.rstrip() for line in f]
    input_asteroids = [[char for char in n] for n in input_asteroids]

    # create list of asteroid and append Asteroid objects into it with their locations
    asteroids = []
    for i in range(len(input_asteroids)):
        for j in range(len(input_asteroids[0])):
            if input_asteroids[i][j] == "#":
                location = (j, i)
                asteroids.append(Asteroid(location))

    print("Number of asteroids:", len(asteroids))
    # compare every asteroid to all the other asteroids
    for start in tqdm(asteroids):
        for end in asteroids:
            # make sure we're not comparing to itself
            if start != end:
                blocking_element = is_between(start, end, asteroids)
                if blocking_element:
                    start.blocking.append(blocking_element.position)
                else:
                    start.detected += 1

    for i in range(len(input_asteroids)):
        for j in range(len(input_asteroids[0])):
            for row in asteroids:
                if row.position == (j, i):
                    print(row.detected, end="")
                else:
                    print(".", end="")
        print("\n")

    best_asteroid = 0
    for element in asteroids:
        print("Position: {}, detected: {}, blocking: {}".format(element.position, element.detected, element.blocking))
        if element.detected > best_asteroid:
            best_asteroid = element.detected
    print("Best asteroid count:", best_asteroid)


def is_between(start_object, end_object, asteroids):
    start = np.array(start_object.position)
    end = np.array(end_object.position)
    start_end_angle = math.atan2(end[1] - start[1], end[0] - start[0])
    start_end_distance = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - [start[1]]) ** 2)
    for asteroid in asteroids:
        element = np.array(asteroid.position)
        start_element_angle = math.atan2(element[1] - start[1], element[0] - start[0])
        start_element_distance = math.sqrt((element[0] - start[0]) ** 2 + (element[1] - [start[1]]) ** 2)
        if start_end_angle == start_element_angle and start_end_distance > start_element_distance and \
                asteroid.position != start_object.position:
            return asteroid
    return False


def check_sloped(start, end, asteroids):
    slope = calculate_slope(start, end)
    for element in asteroids:
        if start.position[0] > element.position[0] > end.position[0] or \
                start.position[0] < element.position[0] < end.position[0] and \
                start.position[1] > element.position[1] > end.position[1] or \
                start.position[1] < element.position[1] < end.position[1]:
            # calculate distance between start and end
            distance_x = abs(start.position[0] - end.position[0])
            distance_y = abs(start.position[1] - end.position[1])
            possible_locations = []
            location_permutations = permutations([distance_x, distance_y], 2)
            for perm in location_permutations:
                x = slope * perm[0]
                y = slope * perm[1]
                if math.floor(x == int(x) and math.floor(y == int(y))):
                    possible_locations.append((math.floor(x), math.floor(y)))
            if element.position in possible_locations:
                return False

    return True


def check_between(start, end, asteroids):
    # check if there's something in between x or y direction in case the asteroids are on same x or y
    for element in asteroids:
        # check if there's something between x direction
        if element.position[1] == start.position[1] and (start.position[0] > element.position[0] > end.position[0] or
                                                         start.position[0] < element.position[0] < end.position[0]):
            return False
        # check if there's something between y direction
        elif element.position[0] == start.position[0] and (start.position[1] > element.position[1] > end.position[1] or
                                                           start.position[1] < element.position[1] < end.position[1]):
            return False

    return True


def calculate_slope(start, end):
    y = (end.position[1] - start.position[1])
    x = (end.position[0] - start.position[0])
    if y == 0:
        raise ZeroDivisionError
    slope = y / x
    return slope


if __name__ == '__main__':
    main()
