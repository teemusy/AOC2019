import numpy as np
DEBUG = 0


class Intcode:

    def __init__(self, int_code, id_code=None, second_input=None):
        self.index = 0
        self.int_codes = int_code
        self.id_code = id_code
        self.second_input = second_input
        self.return_code = None
        self.ready = False
        self.relative = 0
        self.output_list = []

    def step(self):
        self.process_code()
        return self.return_code

    def process_code(self):
        # init op code
        opcode = self.int_codes[self.index]
        raw_opcode = opcode  # for debugging
        # check for additional parameters
        hundreds, thousands, tenthousands = False, False, False
        if len(str(opcode)) > 2:
            hundreds = int(str(opcode)[-3])
        if len(str(opcode)) > 3:
            thousands = int(str(opcode)[-4])
        if len(str(opcode)) > 4:
            tenthousands = int(str(opcode)[-5])
        opcode = int(str(opcode)[-2:])
        try:
            if opcode == 99:
                if DEBUG:
                    print("Exit code 99, end index: {}, list length: {}".format(self.index, len(self.int_codes)))
                self.ready = True
            elif opcode == 1:
                self.opcode_add(hundreds, thousands, tenthousands)
            elif opcode == 2:
                self.opcode_multiply(hundreds, thousands, tenthousands)
            elif opcode == 3:
                self.opcode_input(hundreds)
                if self.second_input is not None:
                    self.id_code = self.second_input
                    self.second_input = None
            elif opcode == 4:
                self.opcode_output(hundreds)
            elif opcode == 5:
                self.opcode_jumpiftrue(hundreds, thousands)
            elif opcode == 6:
                self.opcode_jumpiffalse(hundreds, thousands)
            elif opcode == 7:
                self.opcode_lessthan(hundreds, thousands, tenthousands)
            elif opcode == 8:
                self.opcode_equals(hundreds, thousands, tenthousands)
            elif opcode == 9:
                self.opcode_relative(hundreds)
            else:
                print("Error in opcode: {}, index: {}, list length: {}".
                      format(raw_opcode, self.index, len(self.int_codes)))
                return self.int_codes
        except IndexError:
            # in case list is too small extend it with 100 elements and try again
            self.extend_list(100)
            self.step()

    def extend_list(self, value):
        extra = np.full(value, 0, dtype=int)
        self.int_codes.extend(extra)

    def opcode_add(self, hundreds, thousands, tenthousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        position = self.int_codes[self.index + 3]

        if hundreds == 1:
            first_value = noun
        elif hundreds == 2:
            first_value = self.int_codes[noun + self.relative]
        else:
            first_value = self.int_codes[noun]
        if thousands == 1:
            second_value = verb
        elif thousands == 2:
            second_value = self.int_codes[verb + self.relative]
        else:
            second_value = self.int_codes[verb]
        if tenthousands == 1:
            third_value = self.int_codes[position]
        elif tenthousands == 2:
            third_value = position + self.relative
        else:
            third_value = position
        self.int_codes[third_value] = first_value + second_value
        self.index += 4

    def opcode_multiply(self, hundreds, thousands, tenthousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        position = self.int_codes[self.index + 3]
        if hundreds == 1:
            first_value = noun
        elif hundreds == 2:
            first_value = self.int_codes[noun + self.relative]
        else:
            first_value = self.int_codes[noun]
        if thousands == 1:
            second_value = verb
        elif thousands == 2:
            second_value = self.int_codes[verb + self.relative]
        else:
            second_value = self.int_codes[verb]
        if tenthousands == 1:
            third_value = self.int_codes[position]
        elif tenthousands == 2:
            third_value = position + self.relative
        else:
            third_value = position
        self.int_codes[third_value] = first_value * second_value
        self.index += 4

    def opcode_input(self, hundreds):
        noun = self.int_codes[self.index + 1]
        if hundreds == 1:
            output_position = self.int_codes[noun]
        elif hundreds == 2:
            output_position = noun + self.relative
        else:
            output_position = noun
        input_value = self.id_code
        self.int_codes[output_position] = input_value
        self.index += 2

    def opcode_output(self, hundreds):
        noun = self.int_codes[self.index + 1]
        if hundreds == 1:
            input_value = noun
        elif hundreds == 2:
            input_value = self.int_codes[noun + self.relative]
        else:
            input_value = self.int_codes[noun]
        self.return_code = input_value
        self.output_list.append(input_value)
        self.index += 2

    def opcode_jumpiftrue(self, hundreds, thousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        if hundreds == 1:
            first_value = noun
        elif hundreds == 2:
            first_value = self.int_codes[noun + self.relative]
        else:
            first_value = self.int_codes[noun]
        if thousands == 1:
            second_value = verb
        elif thousands == 2:
            second_value = self.int_codes[verb + self.relative]
        else:
            second_value = self.int_codes[verb]
        if first_value != 0:
            self.index = second_value
        else:
            self.index += 3

    def opcode_jumpiffalse(self, hundreds, thousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        if hundreds == 1:
            first_value = noun
        elif hundreds == 2:
            first_value = self.int_codes[noun + self.relative]
        else:
            first_value = self.int_codes[noun]
        if thousands == 1:
            second_value = verb
        elif thousands == 2:
            second_value = self.int_codes[verb + self.relative]
        else:
            second_value = self.int_codes[verb]
        if first_value == 0:
            self.index = second_value
        else:
            self.index += 3

    def opcode_lessthan(self, hundreds, thousands, tenthousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        position = self.int_codes[self.index + 3]
        if hundreds == 1:
            first_value = noun
        elif hundreds == 2:
            first_value = self.int_codes[noun + self.relative]
        else:
            first_value = self.int_codes[noun]
        if thousands == 1:
            second_value = verb
        elif thousands == 2:
            second_value = self.int_codes[verb + self.relative]
        else:
            second_value = self.int_codes[verb]
        if tenthousands == 1:
            third_value = self.int_codes[position]
        elif tenthousands == 2:
            third_value = position + self.relative
        else:
            third_value = position
        if first_value < second_value:
            self.int_codes[third_value] = 1
        else:
            self.int_codes[third_value] = 0
        self.index += 4

    def opcode_equals(self, hundreds, thousands, tenthousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        position = self.int_codes[self.index + 3]
        if hundreds == 1:
            first_value = noun
        elif hundreds == 2:
            first_value = self.int_codes[noun + self.relative]
        else:
            first_value = self.int_codes[noun]
        if thousands == 1:
            second_value = verb
        elif thousands == 2:
            second_value = self.int_codes[verb + self.relative]
        else:
            second_value = self.int_codes[verb]
        if tenthousands == 1:
            third_value = self.int_codes[position]
        elif tenthousands == 2:
            third_value = position + self.relative
        else:
            third_value = position
        if first_value == second_value:
            self.int_codes[third_value] = 1
        else:
            self.int_codes[third_value] = 0
        self.index += 4

    def opcode_relative(self, hundreds):
        noun = self.int_codes[self.index + 1]
        if hundreds == 1:
            first_value = noun
        elif hundreds == 2:
            first_value = self.int_codes[noun + self.relative]
        else:
            first_value = self.int_codes[noun]
        self.relative += first_value
        self.index += 2
