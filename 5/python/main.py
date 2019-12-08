from intcode import *


# one example doesn't output right value so there's still some bug in code
def main():
    f = open("../5_input.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])
    # id code input
    id_code = 5
    # make original tuplelist to list for editing
    original_copy = list(int_code)
    first_result, error_codes = process_code(original_copy, id_code)
    print("Input:", int_code)
    print("Output:", first_result)
    print("Error codes:", error_codes)


if __name__ == '__main__':
    main()



