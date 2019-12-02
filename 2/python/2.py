f = open("../2_input.txt", "r")
int_code = f.read()
int_code = tuple([int(n) for n in int_code.split(",")])
f.close()


def process_code(input_list):
    output_list = input_list
    index = 0
    for position in input_list:
        first = input_list[index + 1]
        second = input_list[index + 2]
        third = input_list[index + 3]
        if index % 4 == 0:
            if position == 99:
                return output_list
            elif position == 1:
                output_list[third] = \
                    input_list[first] + input_list[second]
            elif position == 2:
                output_list[third] = \
                    input_list[first] * input_list[second]
            else:
                break
        index += 1


def second_stage(input_list):

    index = 0
    try:
        for _ in input_list:
            if index % 4 == 0:
                noun = input_list[index + 1]
                verb = input_list[index + 2]
                if 100 * noun + verb == expected_output:
                    print("Found second result")
                    return "{}{}".format(noun, verb)
            index += 1
    except IndexError:
        return False


# replace values for first run
# make original tuplelist to list for editing
original_copy = list(int_code)
original_copy[1] = 12
original_copy[2] = 2
print("First result:")
first_result = process_code(original_copy)
print(first_result[0])

# replace values for second stage, brute forcing result
expected_output = 19690720
for i in range(100):
    for j in range(100):
        original_copy = list(int_code)
        original_copy[1] = i
        original_copy[2] = j
        second_result = process_code(original_copy)
        current_input = 100 * i + j
        if second_result[0] == expected_output:
            print("Second result:")
            print(current_input)
