from tqdm import tqdm
import math
import numpy as np


class Asteroid:

    def __init__(self, position):
        self.position = position
        self.detected = 0
        self.blocking = []
        self.base = False
        self.direction = None
        self.distance = None


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

    best_asteroid = asteroids[0]
    for element in asteroids:
        if element.detected > best_asteroid.detected:
            best_asteroid = element
    print("Best asteroid count:", best_asteroid.detected)
    best_asteroid.base = True

    # add direction and distance of asteroid relative to base
    asteroids = get_direction(best_asteroid, asteroids)
    for row in asteroids:
        print(row.direction, row.distance, row.base, row.position)
    last_asteroid = use_laser(best_asteroid, asteroids)
    print("200th asteroid:", last_asteroid.position)
    print("Value:", last_asteroid.position[0] * 100 + last_asteroid.position[1])


def use_laser(best_asteroid, asteroids):
    index = 0
    last_degree = -1
    # remove base
    for i in range(len(asteroids)):
        if asteroids[i].base:
            asteroids.pop(i)
            break
    last_asteroid = None
    while True:
        if len(asteroids) == 0 or index == 200:
            return last_asteroid
        # find next asteroid to destroy
        smallest_value = 360

        for i in range(len(asteroids)):
            if asteroids[i].direction <= smallest_value and asteroids[i].direction > last_degree:
                smallest_value = asteroids[i].direction
        possible_asteroids = []
        for i in range(len(asteroids)):
            if asteroids[i].direction == smallest_value:
                possible_asteroids.append(i)
        smallest_value = 100000
        next_target = None
        for row in possible_asteroids:
            if asteroids[row].distance < smallest_value:
                smallest_value = asteroids[row].distance
                next_target = row
        # use laser
        last_degree = asteroids[next_target].direction
        last_asteroid = asteroids[next_target]
        print("Index: {}, position: {}".format(index + 1, last_asteroid.position))
        asteroids.pop(next_target)
        index += 1


def get_direction(best_asteroid, asteroids):
    start_vector = np.array(best_asteroid.position)
    for asteroid in asteroids:
        asteroid_vector = np.array(asteroid.position)
        # using degrees to make it mentally easier
        angle = math.degrees(math.atan2(asteroid_vector[1] - start_vector[1], asteroid_vector[0] - start_vector[0])) + 90
        # normalize angles
        if angle < 0:
            angle += 360
        distance = math.sqrt((asteroid_vector[0] - start_vector[0]) ** 2 + (asteroid_vector[1] - start_vector[1]) ** 2)
        asteroid.direction = angle
        asteroid.distance = distance
    return asteroids


def is_between(start_object, end_object, asteroids):
    start = np.array(start_object.position)
    end = np.array(end_object.position)
    start_end_angle = math.atan2(end[1] - start[1], end[0] - start[0])
    start_end_distance = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - [start[1]]) ** 2)
    for asteroid in asteroids:
        # TODO: skip asteroids that cannot be in between
        element = np.array(asteroid.position)
        start_element_angle = math.atan2(element[1] - start[1], element[0] - start[0])
        start_element_distance = math.sqrt((element[0] - start[0]) ** 2 + (element[1] - [start[1]]) ** 2)
        if start_end_angle == start_element_angle and start_end_distance > start_element_distance and \
                asteroid.position != start_object.position:
            return asteroid
    return False


if __name__ == '__main__':
    main()
