from intcode import Intcode


# one example doesn't output right value so there's still some bug in code
def main():
    f = open("../5_test.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])
    # id code input
    id_code = 0
    # make original tuplelist to list for editing
    original_copy = list(int_code)
    computer = Intcode(original_copy, id_code)
    while not computer.ready:
        computer.step()
    end_list = computer.int_codes
    result = computer.return_code
    print("Input:", int_code)
    print("Output:", end_list)
    print("Error codes:", result)


if __name__ == '__main__':
    main()



