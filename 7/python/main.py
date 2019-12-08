from intcode import *


def main():
    f = open("../7_test.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])

    phase_setting = 4
    original_copy = list(int_code)
    first_result, error_codes = process_code(original_copy, phase_setting, 0)

    phase_setting = 3

    original_copy = list(int_code)
    first_result, error_codes = process_code(original_copy, phase_setting, error_codes[0])

    phase_setting = 2

    original_copy = list(int_code)
    first_result, error_codes = process_code(original_copy, phase_setting, error_codes[0])

    phase_setting = 1

    original_copy = list(int_code)
    first_result, error_codes = process_code(original_copy, phase_setting, error_codes[0])
    phase_setting = 0

    original_copy = list(int_code)
    first_result, error_codes = process_code(original_copy, phase_setting, error_codes[0])

    print(error_codes)



if __name__ == '__main__':
    main()