from tqdm import tqdm


class Intcode:

    def __init__(self, int_code, id_code, second_input=None):
        self.index = 0
        self.int_codes = int_code
        self.id_code = id_code
        self.second_input = second_input
        self.return_code = None
        self.ready = False

    def step(self):
        self.process_code()
        if self.return_code is not None:
            return self.return_code
        else:
            return None

    def process_code(self):
        pbar = tqdm(total=len(self.int_codes), desc="Prosessing code")
        output_list = []
        while self.index < len(self.int_codes):
            if self.int_codes[self.index] == 99:
                print("Exit code 99, end index: {}, list length: {}".format(self.index, len(self.int_codes)))
                pbar.close()
                self.ready = True
                return self.return_code
            # init op code
            opcode = self.int_codes[self.index]
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

            if opcode == 1:
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
            else:
                print("Error in opcode: {}, index: {}, list length: {}".
                      format(raw_opcode, self.index, len(self.int_codes)))
                return self.int_codes, output_list
            pbar.update(1)
        print("List ended with no exit code, list length:", len(self.int_codes))
        return self.return_code

    def opcode_add(self, hundreds, thousands, tenthousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        position = self.int_codes[self.index + 3]
        if hundreds:
            first_value = noun
        else:
            first_value = self.int_codes[noun]
        if thousands:
            second_value = verb
        else:
            second_value = self.int_codes[verb]
        self.int_codes[position] = first_value + second_value
        self.index += 4

    def opcode_multiply(self, hundreds, thousands, tenthousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        position = self.int_codes[self.index + 3]
        if hundreds:
            first_value = noun
        else:
            first_value = self.int_codes[noun]
        if thousands:
            second_value = verb
        else:
            second_value = self.int_codes[verb]

        self.int_codes[position] = first_value * second_value
        self.index += 4

    def opcode_input(self, hundreds):
        noun = self.int_codes[self.index + 1]
        if hundreds:
            print("OPCODE 3, IMMEDIATE MODE, POSSIBLE ERROR!?")
            output_position = self.int_codes[noun]
        else:
            output_position = noun
        input_value = self.id_code
        self.int_codes[output_position] = input_value
        self.index += 2

    def opcode_output(self, hundreds):
        noun = self.int_codes[self.index + 1]
        if hundreds:
            input_value = noun
        else:
            input_value = self.int_codes[noun]
        self.return_code = input_value
        self.index += 2

    def opcode_jumpiftrue(self, hundreds, thousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        if hundreds:
            first_value = noun
        else:
            first_value = self.int_codes[noun]
        if thousands:
            second_value = verb
        else:
            second_value = self.int_codes[verb]
        if first_value != 0:
            self.index = second_value
        else:
            self.index += 3

    def opcode_jumpiffalse(self, hundreds, thousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        if hundreds:
            first_value = noun
        else:
            first_value = self.int_codes[noun]
        if thousands:
            second_value = verb
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
        if hundreds:
            first_value = noun
        else:
            first_value = self.int_codes[noun]
        if thousands:
            second_value = verb
        else:
            second_value = self.int_codes[verb]
        if tenthousands:
            print("Tenthousands")
            exit()
        if first_value < second_value:
            self.int_codes[position] = 1
        else:
            self.int_codes[position] = 0
        self.index += 4

    def opcode_equals(self, hundreds, thousands, tenthousands):
        noun = self.int_codes[self.index + 1]
        verb = self.int_codes[self.index + 2]
        position = self.int_codes[self.index + 3]
        if hundreds:
            first_value = noun
        else:
            first_value = self.int_codes[noun]
        if thousands:
            second_value = verb
        else:
            second_value = self.int_codes[verb]
        if tenthousands:
            print("Tenthousands")
            exit()
        if first_value == second_value:
            self.int_codes[position] = 1
        else:
            self.int_codes[position] = 0
        self.index += 4
