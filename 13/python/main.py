from intcode import Intcode
import numpy as np
from matplotlib import pyplot, colors


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
        if x is not None and y is not None and tile_type is not None:
            old_tile = [n for n in tiles if n.position == (x, y)]
            if len(old_tile):
                assert len(old_tile) == 1
                old_tile[0].tile = tile_type
            else:
                tiles.append(Tile((x, y), tile_type))
            x, y, tile_type = None, None, None

    block_tiles = [n for n in tiles if n.tile == 2]
    print("Number of block tiles:", len(block_tiles))

    grid_map = np.full((24, 42), 0, dtype=int)
    for element in tiles:
        grid_map[element.position[1]][element.position[0]] = element.tile

    create_visual_map(grid_map)


def create_visual_map(input_data, override_colors=False):
    cmap = colors.ListedColormap(['black', 'white', 'red', 'blue', 'yellow'])
    rm = np.array(input_data)
    if override_colors:
        pyplot.imshow(rm, interpolation='nearest')
    else:
        pyplot.imshow(rm, interpolation='nearest', cmap=cmap)
    pyplot.title('Wiregrid')
    pyplot.tight_layout()
    pyplot.grid()
    pyplot.show()


if __name__ == '__main__':
    main()