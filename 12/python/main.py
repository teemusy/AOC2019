import numpy as np
import copy
from time import time


class Moon:
    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = np.array([0, 0, 0])


def main():
    start_time = time()
    moon_list = [Moon([-1, 0, 2]), Moon([2, -10, -7]), Moon([4, -8, 8]), Moon([3, 5, -1])]
    # 179 after 10 steps, 2772
    #moon_list = [Moon([-8, -10, 0]), Moon([5, 5, 10]), Moon([2, -7, 3]), Moon([9, -8, -3])]
    # 1940 after 100, 4686774924
    #moon_list = [Moon([-6, -5, -8]), Moon([0, -3, -13]), Moon([-15, 10, -11]), Moon([-3, -8, 3])]  # input
    steps = 100

    total = calculate_kinetical(moon_list, steps)
    print("Total energy in system after {} steps: {}".format(steps, total))
    start = find_position(moon_list, start_time)
    print("Steps needed to return to starting position and velocity:", start)
    print("Time used:", time() - start_time)


def find_position(moon_list, start_time):
    # get staring positions and velocity
    start_pos = []
    start_vel = []
    for element in moon_list:
        temp_pos = element.position.copy()
        temp_vel = element.velocity.copy()
        start_pos.append(temp_pos)
        start_vel.append(temp_vel)

    steps = 0
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
        if steps % 1000000 == 0 and steps != 0:
            print("Current step: {}, time: {}".format(steps, time() - start_time))
        # get current position and velocity
        current_pos = []
        current_vel = []
        for element in moon_list:
            temp_pos = element.position.copy()
            temp_vel = element.velocity.copy()
            current_pos.append(temp_pos)
            current_vel.append(temp_vel)

        # compare position and velocity
        if np.array_equal(start_pos, current_pos) and np.array_equal(start_vel, current_vel):
            break
        else:
            continue

    return steps


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