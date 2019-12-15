import re
from time import time
import math
from math import gcd
from functools import reduce


class Reaction:
    def __init__(self, input_reaction=None, output=None):
        self.input_reaction = input_reaction
        self.input = []
        self.output = output
        if input_reaction is not None:
            self.parse_input()
        self.needed = 0

    def parse_input(self):
        input = self.input_reaction.split("=>")[0]
        output = self.input_reaction.split("=>")[1]
        if "," in input:
            input = input.split(",")
            for element in input:
                amount = int(re.findall(r"[\d]+", element)[0])
                material = re.findall(r"[a-zA-Z]+", element)
                self.input.append((amount, material[0]))
        else:
            amount = int(re.findall(r"[\d]+", input)[0])
            material = re.findall(r"[a-zA-Z]+", input)
            self.input.append((amount, material[0]))
        amount = int(re.findall(r"[\d]+", output)[0])
        material = re.findall(r"[a-zA-Z]+", output)
        self.output = (amount, material[0])


def main():
    start_time = time()
    f = open("../14_test.txt", "r")
    reactions = f.readlines()
    f.close()

    # create objects for reactions
    reaction_list = {}
    for row in reactions:
        reaction_name = re.findall(r"[a-zA-Z]+", row.split("=>")[1])[0]
        reaction_list.update({reaction_name: Reaction(row)})
    # add fuel needed and ore object manually
    fuel = 1

    reaction_list["FUEL"].needed = fuel
    reaction_list.update({"ORE": Reaction(output=(1, "ORE"))})
    # find out how much we need every element
    needed = True
    trillion = 1000000000000
    make_one = True
    can_make = 0
    index = 0
    pattern = []
    while index < fuel:
        while needed:
            needed = [n for n in reaction_list.values() if n.needed > 0]
            if len(needed) == 0:
                break
            if needed[0].output[1] == "ORE" and len(needed) == 1:
                break
            for element in reaction_list.values():
                if element.needed > 0 and element.output[1] != "ORE":
                    # how many times we need to produce reaction to create needed amount of material
                    reactions_needed = element.needed // element.output[0]
                    if reactions_needed == 0:
                        reactions_needed = 1
                    for _ in range(reactions_needed):
                        for input in element.input:
                            reaction_list[input[1]].needed += input[0]
                        element.needed -= element.output[0]
        all_zero = True
        for element in reaction_list.values():
            if element.needed != 0:
                all_zero = False
        if all_zero:
            pattern.append(index)
            break
        index += 1



    ore_needed =  reaction_list["ORE"].needed
    if make_one:
        print("Amount of ore needed:", ore_needed)
    else:
        print("Amount of fuel that can be made with 1 trillion ore:", can_make)
    print(pattern)

    pattern = []
    for element in reaction_list.values():
        if element.needed and element.output[1] != "ORE":
            pattern.append(element.needed)
    print(pattern)

    if can_make == 82892753:
        print("GREAT SUCCESS!")
    finish_time = round(time() - start_time, 5)
    print("Finished in time: {}\n".format(finish_time))

    print("PATTERN:", find_smallest_common_denominator(pattern))

    result = (trillion / -find_smallest_common_denominator(pattern)) / 43426211
    print(result)


def find_smallest_common_denominator(pattern):
    return reduce(lambda a, b: a * b // gcd(a, b), pattern)


if __name__ == '__main__':
    main()