from intcode import *
from itertools import permutations
from tqdm import tqdm


def main():
    f = open("../7_input.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])
    highest_value = first_part(int_code)
    print("Highest output value:", highest_value)
    highest_feedback_loop = second_part(int_code)  # should be 139629729
    #highest_feedback_loop = second_part(int_code)
    print("Highest feedback loop value:", highest_feedback_loop)


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
        a_input = None
        try:
            while not final_output:
                if a is None:
                    a = Intcode(list(int_code), phase_input[0], 0)
                    while not a.return_code:
                        a.step()
                else:
                    a.id_code = a_input
                    b_input = a.return_code
                    a.return_code = None
                    while not a.ready and not a.return_code:
                        a.step()
                b_input = a.return_code
                if b is None:
                    b = Intcode(list(int_code), phase_input[1], b_input)
                    while not b.return_code:
                        b.step()
                else:
                    b.id_code = b_input
                    c_input = b.return_code
                    b.return_code = None
                    while not b.ready and not b.return_code:
                        b.step()
                c_input = b.return_code
                if c is None:
                    c = Intcode(list(int_code), phase_input[2], c_input)
                    while not c.return_code:
                        c.step()
                else:
                    c.id_code = c_input
                    d_input = c.return_code
                    c.return_code = None
                    while not c.ready and not c.return_code:
                        c.step()
                d_input = c.return_code
                if d is None:
                    d = Intcode(list(int_code), phase_input[3], d_input)
                    while not d.return_code:
                        d.step()
                else:
                    d.id_code = d_input
                    e_input = d.return_code
                    d.return_code = None
                    while not d.ready and not d.return_code:
                        d.step()
                e_input = d.return_code
                if e is None:
                    e = Intcode(list(int_code), phase_input[4], e_input)
                    while not e.return_code:
                        e.step()
                else:
                    e.id_code = e_input
                    a_input = e.return_code
                    e.return_code = None
                    while not e.ready and not e.return_code:
                        e.step()
                a_input = e.return_code
                final_output = e.ready
                try:
                    if a_input > highest_value:
                        highest_value = a_input
                        highest_permutation = phase_input
                except TypeError:
                    break
        except TypeError:
            continue

    print("Highest permutation:", highest_permutation)
    return highest_value


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
