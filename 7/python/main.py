from intcode import *
from itertools import permutations


def main():
    f = open("../7_test.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])
    highest_value = first_part(int_code)
    print("Highest output value:", highest_value)


def first_part(int_code, phase_code=None):
    # get all permutations of phase codes
    phase_permutations = permutations([0, 1, 2, 3, 4])
    # give possibility to override phase code sequence for testing
    if phase_code:
        phase_permutations = [phase_code]
    highest_value = 0
    for row in phase_permutations:
        phase_setting = row
        error_codes = [0]
        for i in range(5):
            original_copy = list(int_code)
            final_list, error_codes = process_code(original_copy, phase_setting[i], error_codes[0])
        if error_codes[0] > highest_value:
            highest_value = error_codes[0]
    return highest_value


if __name__ == '__main__':
    main()
