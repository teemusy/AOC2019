from intcode import *


def main():
    f = open("../7_test.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])

    phase_setting = [1,0,4,3,2]
    error_codes = [0]
    for i in range(5):
        original_copy = list(int_code)
        final_list, error_codes = process_code(original_copy, phase_setting[i], error_codes[0])
        print(final_list)

    print(error_codes)


if __name__ == '__main__':
    main()