from intcode import Intcode
import numpy as np
from matplotlib import pyplot, colors


class Robot:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def move(self, direction):
        assert direction is not None
        move = {
            "up": (lambda n: n + np.array([-1, 0])),
            "down": (lambda n: n + np.array([1, 0])),
            "left": (lambda n: n + np.array([0, -1])),
            "right": (lambda n: n + np.array([0, 1]))}
        if direction == 0:
            if self.direction == 0:
                self.position = move["left"](self.position)
            elif self.direction == 180:
                self.position = move["right"](self.position)
            elif self.direction == 270:
                self.position = move["down"](self.position)
            elif self.direction == 90:
                self.position = move["up"](self.position)
            self.direction -= 90
        elif direction == 1:
            if self.direction == 0:
                self.position = move["right"](self.position)
            elif self.direction == 180:
                self.position = move["left"](self.position)
            elif self.direction == 270:
                self.position = move["up"](self.position)
            elif self.direction == 90:
                self.position = move["down"](self.position)
            self.direction += 90
        if self.direction >= 360:
            self.direction = 0
        elif self.direction < 0:
            self.direction = 270
        self.position = list(self.position)


class Panel:
    def __init__(self, position, color=0):
        self.position = position
        self.color = color
        self.times_painted = 0

    def paint(self, color):
        self.color = color
        self.times_painted += 1


def main():
    f = open("../11_input.txt", "r")
    int_code = f.read()
    f.close()
    int_code = list([int(n) for n in int_code.split(",")])

    starting_row = 75
    starting_column = 75
    robot = Robot([starting_row, starting_column], 0)
    computer = Intcode(int_code, 0)
    panels = {"[{}, {}]".format(starting_row, starting_column): Panel([starting_row, starting_column])}

    command_type = "color"
    while not computer.ready:
        computer.return_code = None
        while computer.return_code is None and not computer.ready:
            computer.step()
        if computer.ready:
            break
        assert computer.return_code == 1 or computer.return_code == 0
        if command_type == "color":
            panels[str(robot.position)].paint(computer.return_code)
            command_type = "move"
        else:
            robot.move(computer.return_code)
            if str(robot.position) not in panels.keys():
                panels.update({str(robot.position): Panel(robot.position)})
            computer.id_code = panels[str(robot.position)].color
            command_type = "color"

    # find panels painted only once
    once_painted = [n for n in panels.values() if n.times_painted >= 1]
    print("Panels painted at least once:", len(once_painted))

    grid_map = np.full((150, 150), 0, dtype=int)
    for element in panels.values():
        if element.color == 1:
            grid_map[element.position[1]][element.position[0]] = 1
        else:
            grid_map[element.position[1]][element.position[0]] = 0
    create_visual_map(grid_map)


def create_visual_map(input_data, override_colors=False):
    cmap = colors.ListedColormap(['black', 'white'])
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
