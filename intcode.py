from tqdm import tqdm


def opcode_add(index, hundreds, thousands, tenthousands, input_list):
    noun = input_list[index + 1]
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
    input_list[position] = first_value + second_value

    return input_list


def opcode_multiply(index, hundreds, thousands, tenthousands, input_list):
    noun = input_list[index + 1]
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

    input_list[position] = first_value * second_value

    return input_list


def opcode_input(index, input_id_code, input_list, hundreds):
    noun = input_list[index + 1]
    if hundreds:
        print("OPCODE 3, IMMEDIATE MODE, POSSIBLE ERROR!")
        output_position = input_list[noun]
    else:
        output_position = noun
    input_value = input_id_code
    input_list[output_position] = input_value

    return input_list


def opcode_output(index, output_list, input_list, hundreds):
    noun = input_list[index + 1]
    if hundreds:
        input_value = noun
    else:
        input_value = input_list[noun]
    output_list.append(input_value)

    return output_list


def opcode_jumpiftrue(index, hundreds, thousands, input_list):
    noun = input_list[index + 1]
    verb = input_list[index + 2]
    if hundreds:
        first_value = noun
    else:
        first_value = input_list[noun]
    if thousands:
        second_value = verb
    else:
        second_value = input_list[verb]
    if first_value != 0:
        index = second_value
    else:
        index += 3

    return index


def opcode_jumpiffalse(index, hundreds, thousands, input_list):
    noun = input_list[index + 1]
    verb = input_list[index + 2]
    if hundreds:
        first_value = noun
    else:
        first_value = input_list[noun]
    if thousands:
        second_value = verb
    else:
        second_value = input_list[verb]
    if first_value == 0:
        index = second_value
    else:
        index += 3

    return index


def opcode_lessthan(index, hundreds, thousands, tenthousands, input_list):
    noun = input_list[index + 1]
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
    if first_value < second_value:
        input_list[position] = 1
    else:
        input_list[position] = 0
    return input_list


def opcode_equals(index, hundreds, thousands, tenthousands, input_list):
    noun = input_list[index + 1]
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
    if first_value == second_value:
        input_list[position] = 1
    else:
        input_list[position] = 0
    return input_list


def process_code(input_list, input_id_code, second_input=None):
    index = 0
    pbar = tqdm(total=len(input_list), desc="Prosessing code")
    output_list = []
    while index < len(input_list):
        pbar.update(1)
        # init op code
        opcode = input_list[index]
        raw_opcode = opcode  # for debugging
        # check for additional parameters
        hundreds, thousands, tenthousands = False, False, False
        if len(str(opcode)) > 2 and int(str(opcode)[-3]) > 0:
            hundreds = True
        if len(str(opcode)) > 3 and int(str(opcode)[-4]) > 0:
            thousands = True
        if len(str(opcode)) > 4 and int(str(opcode)[-5]) > 0:
            tenthousands = True
        opcode = int(str(opcode)[-2:])

        if input_list[index] == 99:
            print("Exit code 99, end index: {}, list length: {}".format(index, len(input_list)))
            pbar.close()
            return input_list, output_list

        if opcode == 1:
            input_list = opcode_add(index, hundreds, thousands, tenthousands, input_list)
            index += 4
        elif opcode == 2:
            input_list = opcode_multiply(index, hundreds, thousands, tenthousands, input_list)
            index += 4
        elif opcode == 3:
            input_list = opcode_input(index, input_id_code, input_list, hundreds)
            if second_input:
                input_id_code = second_input
                second_input = None
            index += 2
        elif opcode == 4:
            output_list = opcode_output(index, output_list, input_list, hundreds)
            index += 2
        elif opcode == 5:
            index = opcode_jumpiftrue(index, hundreds, thousands, input_list)
        elif opcode == 6:
            index = opcode_jumpiffalse(index, hundreds, thousands, input_list)
        elif opcode == 7:
            input_list = opcode_lessthan(index, hundreds, thousands, tenthousands, input_list)
            index += 4
        elif opcode == 8:
            input_list = opcode_equals(index, hundreds, thousands, tenthousands, input_list)
            index += 4
        else:
            print("Error in opcode: {}, index: {}, list length: {}".format(raw_opcode, index, len(input_list)))
            return input_list, output_list
    print("List ended with no exit code, list length:", len(input_list))
    return input_list, output_list