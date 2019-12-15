from intcode import Intcode
import numpy as np
from matplotlib import pyplot, colors
import pygame


class Tile:
    def __init__(self, position, tile):
        self.position = position
        self.tile = tile


def main():
    f = open("../13_input.txt", "r")
    int_code = f.read()
    f.close()
    int_code = list([int(n) for n in int_code.split(",")])

    computer = Intcode(int_code, 2)
    tiles = []
    x, y, tile_type = None, None, None
    current_score = None

    pygame.init()
    pygame.display.set_caption("Day 13")
    screen = pygame.display.set_mode((840, 480))
    screen.fill((255, 255, 255))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            while not computer.ready:
                computer.return_code = None
                while computer.return_code is None and not computer.ready:
                    computer.step()
                if computer.ready:
                    break
                assert computer.return_code is not None
                if x is None:
                    x = computer.return_code
                elif y is None:
                    y = computer.return_code
                elif tile_type is None:
                    tile_type = computer.return_code

                paddle_location = [n for n in tiles if n.tile == 3]
                ball_location = [n for n in tiles if n.tile == 4]
                if len(paddle_location) > 0 and len(ball_location) > 0:
                    # 21 for x is neutral for paddle
                    assert len(paddle_location) == 1
                    assert len(ball_location) == 1
                    if paddle_location[0].position[0] == ball_location[0].position[0]:
                        computer.id_code = 0
                    elif paddle_location[0].position[0] < ball_location[0].position[0]:
                        computer.id_code = 1
                    elif paddle_location[0].position[0] > ball_location[0].position[0]:
                        computer.id_code = -1

                if x == -1 and y == 0 and tile_type is not None:
                    current_score = tile_type
                    block_tiles = [n for n in tiles if n.tile == 2]
                    if len(block_tiles) == 0:
                        break
                    x, y, tile_type = None, None, None

                elif x is not None and y is not None and tile_type is not None:
                    assert x >= 0
                    assert y >= 0
                    assert tile_type >= 0
                    old_tile = [n for n in tiles if n.position == (x, y)]
                    if len(old_tile):
                        assert len(old_tile) == 1
                        old_tile[0].tile = tile_type
                    else:
                        tiles.append(Tile((x, y), tile_type))

                    colors = {
                        0: (0, 0, 255),
                        1: (255, 0, 0),
                        2: (0, 255, 0),
                        3: (100, 0, 100),
                        4: (0, 100, 255)
                    }
                    block_x = 20
                    block_y = 20
                    pygame.draw.rect(screen, colors[tile_type], (x * block_x, y * block_y, block_x, block_y))
                    x, y, tile_type = None, None, None

                pygame.display.update()

    print("Final score:", current_score)


if __name__ == '__main__':
    main()