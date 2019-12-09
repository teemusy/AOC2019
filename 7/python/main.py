from intcode import *
from itertools import permutations
from tqdm import tqdm


def main():
    f = open("../7_test.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])
    highest_value = first_part(int_code)
    print("Highest output value:", highest_value)
    #highest_feedback_loop = second_part(int_code, [9, 8, 7, 6, 5])  # should be 139629729
    #highest_feedback_loop = second_part(int_code)
    #print("Highest feedback loop value:", highest_feedback_loop)


def second_part(int_code, phase_code=None):
    # get all permutations of phase codes
    phase_permutations = permutations([5, 6, 7, 8, 9])
    # give possibility to override phase code sequence for testing
    if phase_code:
        phase_permutations = [phase_code]
    highest_value = 0
    highest_permutation = None
    for phase_input in tqdm(phase_permutations, desc="Solving second part"):
        final_output = False
        a, b, c, d, e = None, None, None, None, None
        a_input = phase_input[0]
        while not final_output:
            a = continue_computer(int_code, a_input, None, True, None)

        error_code = e.return_code
        if error_code > highest_value:
            highest_value = error_code
            highest_permutation = phase_input

    print("Highest permutation:", highest_permutation)
    return highest_value


def continue_computer(int_code, id_code, computer=None, create_new=False, second_input=None):
    if create_new:
        int_code_copy = list(int_code)
        computer = Intcode(int_code_copy, id_code, second_input)
    else:
        computer.id_code = id_code
        computer.return_code = None
    while computer.return_code is None:
        computer.step()
    return computer


def first_part(int_code, phase_code=None):
    # get all permutations of phase codes
    phase_permutations = permutations([0, 1, 2, 3, 4])
    # give possibility to override phase code sequence for testing
    if phase_code:
        phase_permutations = [phase_code]
    highest_value = 0
    for row in tqdm(phase_permutations, desc="Solving first part"):
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
