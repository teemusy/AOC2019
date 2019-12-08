from intcode import *
from itertools import permutations


def main():
    f = open("../7_input.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])
    highest_value = first_part(int_code)
    print("Highest output value:", highest_value)


def second_part(int_code, phase_code=None):
    # get all permutations of phase codes
    phase_permutations = permutations([0, 1, 2, 3, 4])
    # give possibility to override phase code sequence for testing
    if phase_code:
        phase_permutations = [phase_code]
    highest_value = 0
    for row in phase_permutations:
        phase_setting = row
        error_code = 0
        original_copy = list(int_code)
        for i in range(5):
            amplification_ready = False
            while not amplification_ready:

                a = Intcode(original_copy, phase_setting[i], error_code)
                b = Intcode(original_copy, phase_setting[i], error_code)
                c = Intcode(original_copy, phase_setting[i], error_code)
                d = Intcode(original_copy, phase_setting[i], error_code)
                e = Intcode(original_copy, phase_setting[i], error_code)
                amplification_ready = e.ready
            while computer.ready is False:
                computer.step()
            error_code = computer.return_code

        if error_code > highest_value:
            highest_value = error_code
    return highest_value

def first_part(int_code, phase_code=None):
    # get all permutations of phase codes
    phase_permutations = permutations([0, 1, 2, 3, 4])
    # give possibility to override phase code sequence for testing
    if phase_code:
        phase_permutations = [phase_code]
    highest_value = 0
    for row in phase_permutations:
        phase_setting = row
        error_code = 0
        for i in range(5):
            original_copy = list(int_code)
            computer = Intcode(original_copy, phase_setting[i], error_code)
            while computer.ready is False:
                computer.step()
            error_code = computer.return_code
            del computer
        if error_code > highest_value:
            highest_value = error_code
    return highest_value


if __name__ == '__main__':
    main()
