f = open("../1_input.txt", "r")
mass_list = f.readlines()


def calc_fuel(input_list):
    total_fuel = 0
    extra_fuel = 0
    for row in input_list:
        mass = int(row.rstrip())
        fuel = int(mass / 3 - 2)
        total_fuel += fuel
        extra_fuel += calc_extra_fuel(fuel)

    print("First result: {}".format(total_fuel))
    print("Second result: {}".format(total_fuel + extra_fuel))


def calc_extra_fuel(input_fuel):
    extra_fuel = 1
    fuel = 0
    while extra_fuel > 0:
        extra_fuel = int(input_fuel / 3 - 2)
        if extra_fuel > 0:
            fuel += extra_fuel
            input_fuel = extra_fuel
    return fuel


calc_fuel(mass_list)
