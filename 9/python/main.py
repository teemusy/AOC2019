from intcode import Intcode
import numpy as np


def main():
    f = open("../9_input.txt", "r")
    int_code = f.read()
    f.close()
    int_code = tuple([int(n) for n in int_code.split(",")])
    int_code_copy = list(int_code)

    computer = Intcode(int_code_copy, 2)
    while not computer.ready:
        computer.step()
    print(computer.return_code)
    print(computer.int_codes)
    print(computer.output_list)


if __name__ == '__main__':
    main()
