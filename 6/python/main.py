import numpy as np
from string import ascii_letters


def main():
    f = open("../6_input.txt", "r")
    int_code = f.readlines()
    f.close()
    # create tuple from integers in int file
    int_code = tuple(n.rstrip() for n in int_code)
    # find central object
    central_object = find_central(int_code)
    print("Central object that the rest of the planets orbit:", central_object)


def find_central(int_code):
    # divide input into 2 list, origo and orbiter
    origo, orbiter = [], []
    for row in int_code:
        left, right = row.split(")")
        origo.append(left)
        orbiter.append(right)

    # find unique values in origo list
    origo = np.array(origo)
    origo = np.unique(origo, return_counts=True)
    unique_origos = []
    for i in range(len(origo[0])):
        if origo[1][i] == 1:
            unique_origos.append(origo[0][i])
    origo = unique_origos

    # find which unique value is not in the orbiter list
    orbiter = np.array(orbiter)
    unique = set(origo) - set(orbiter)
    assert len(unique) == 1, "Found more than one central object!"
    unique = str(unique).strip("{'}")
    return unique


if __name__ == '__main__':
    main()