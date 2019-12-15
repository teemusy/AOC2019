from intcode import Intcode
import numpy as np
import pygame


class Tile:
    def __init__(self, position, tile):
        self.position = position
        self.tile = tile
        self.is_start = None


class Robot:
    def __init__(self, position):
        self.position = position


def main():
    f = open("../15_input.txt", "r")
    int_code = f.read()
    f.close()
    int_code = list([int(n) for n in int_code.split(",")])

    computer = Intcode(int_code)
    # init map, using 1d array
    tiles = [Tile([0, 0], 1)]
    tiles[0].is_start = True
    robot = Robot([0, 0])

    pygame.init()
    pygame.display.set_caption("Day 15")
    width = 600
    height = 600
    screen = pygame.display.set_mode((width, height))
    running = True

    while running:
        while not computer.ready:
            # draw screen
            colors = {
                0: (0, 0, 0),  # wall
                1: (255, 255, 255),  # empty
                2: (0, 255, 0),  # oxygen
                3: (100, 100, 100),  # robot
                4: (255, 0, 0)  # start
            }
            block_x = 20
            block_y = 20
            start_x = int(width / 2)
            start_y = int(height / 2)
            screen.fill((255, 255, 255))
            for element in tiles:
                x = element.position[0] * block_x + start_x - robot.position[0] * block_x
                y = element.position[1] * block_y + start_y - robot.position[1] * block_y
                if element.is_start:
                    pygame.draw.rect(screen, colors[4], (x, y, block_x, block_y))
                else:
                    pygame.draw.rect(screen, colors[element.tile], (x, y, block_x, block_y))
                # draw robot, always in the middle of the screen
                pygame.draw.rect(screen, colors[3], (start_x, start_y, block_x, block_y))
            pygame.display.update()
            # movement control
            key_pressed = False
            while not key_pressed:
                events = pygame.event.get()
                for element in events:
                    # quit doesn't work
                    if element == pygame.QUIT:
                        running = False
                        computer.ready = True
                    if element.type == pygame.KEYDOWN:
                        if element.key == pygame.K_LEFT:
                            print("Left")
                            computer.id_code = 3
                            key_pressed = True
                            break
                        elif element.key == pygame.K_RIGHT:
                            print("Right")
                            computer.id_code = 4
                            key_pressed = True
                            break
                        elif element.key == pygame.K_UP:
                            print("Up")
                            computer.id_code = 1
                            key_pressed = True
                            break
                        elif element.key == pygame.K_DOWN:
                            print("Down")
                            computer.id_code = 2
                            key_pressed = True
                            break

            computer.return_code = None
            while computer.return_code is None and not computer.ready:
                computer.step()
            if computer.ready:
                print("Computer ready")
                break
            move = {
                1: (lambda n: n + np.array([0, -1])),
                2: (lambda n: n + np.array([0, 1])),
                3: (lambda n: n + np.array([-1, 0])),
                4: (lambda n: n + np.array([1, 0]))}
            next_position = move[computer.id_code](robot.position)
            if computer.return_code != 0:
                robot.position = move[computer.id_code](robot.position)

            print("Current: {}, next: {}".format(robot.position, next_position))
            old_tile = [n for n in tiles if n.position[0] == next_position[0] and n.position[1] == next_position[1]]
            print("Found old tile: {}, return code: {}".format(len(old_tile), computer.return_code))
            if len(old_tile) == 0 and computer.return_code != 0:
                tiles.append(Tile(next_position, computer.return_code))
            elif len(old_tile) == 0:
                tiles.append(Tile(next_position, computer.return_code))


if __name__ == '__main__':
    main()
