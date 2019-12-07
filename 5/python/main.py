from tqdm import tqdm


def main():
    f = open("../5_test.txt", "r")
    int_code = f.read()
    f.close()
    # create tuple from integers in int file
    int_code = tuple([int(n) for n in int_code.split(",")])
    # id code input
    id_code = 1
    # make original tuplelist to list for editing
    original_copy = list(int_code)
    first_result = process_code(original_copy, id_code)
    print("Input:", int_code)
    print("Output:", first_result)


def process_code(input_list, input_id_code):
    index = 0
    pbar = tqdm(total=len(input_list), desc="Prosessing code")
    output_list = []
    while index < len(input_list):
        pbar.update(1)
        # init op code
        opcode = input_list[index]
        hundreds, thousands, tenthousands = False, False, False
        if len(str(opcode)) > 2 and int(str(opcode)[-3]) > 0:
            hundreds = True
        if len(str(opcode)) > 3 and int(str(opcode)[-4]) > 0:
            thousands = True
        if len(str(opcode)) > 4 and int(str(opcode)[-5]) > 0:
            tenthousands = True
        opcode = int(str(opcode)[-2:])
        if input_list[index] == 99:
            print("Exit code 99, end index:", index)
            pbar.close()
            return output_list

        noun = input_list[index + 1]

        if opcode == 1 or opcode == 2:
            verb = input_list[index + 2]
            position = input_list[index + 3]
            if hundreds:
                first_value = noun
            else:
                first_value = input_list[noun]
            if thousands:
                second_value = verb
            else:
                second_value = input_list[verb]
            if tenthousands:
                print("Tenthousands")
                exit()

            if opcode == 1:
                input_list[position] = first_value + second_value
            elif opcode == 2:
                input_list[position] = first_value * second_value
            index += 4
        elif opcode == 3:
            output_position = noun
            input_value = input_id_code
            input_list[output_position] = input_value
            index += 2
        elif opcode == 4:
            input_value = input_list[noun]
            output_list.append(input_value)
            index += 2


if __name__ == '__main__':
    main()


