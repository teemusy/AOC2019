def main():
    f = open("../6_input.txt", "r")
    planet_list = f.readlines()
    f.close()
    # create tuple from integers in int file
    planet_list = [n.rstrip() for n in planet_list]
    planet_list_copy = planet_list.copy()
    # central object that all other objects orbit
    central_object = "COM"
    # insert central object in 2d list as starting point
    celestial_objects = [[central_object]]
    # find all objects that loop around central object and add them to next index, than do the same to them
    index = 0
    while len(planet_list):
        orbiters, planet_list = find_orbiters(celestial_objects[index], planet_list)
        celestial_objects.append(orbiters)
        index += 1

    # count orbits
    orbits = calculate_orbits(celestial_objects)
    print("Number of combined orbits:", orbits)
    # find shortest route to santa
    planet_list = planet_list_copy.copy()
    shortest_route = find_route(planet_list)
    print("Minimum orbital transfers required:", shortest_route)


def find_route(planet_list):
    planet_list_copy = planet_list.copy()

    # find your route to start
    starting_point = "YOU"
    you = []
    i = 0
    while starting_point != "COM":
        if starting_point in planet_list[i].split(")")[1]:
            you.append(planet_list[i])
            starting_point = planet_list[i].split(")")[0]
            # remove from list to make loops faster
            planet_list.pop(i)
            i = 0
        else:
            i += 1

    # find santas route to start
    planet_list = planet_list_copy.copy()
    starting_point = "SAN"
    santa = []
    i = 0
    while starting_point != "COM":
        if starting_point in planet_list[i].split(")")[1]:
            santa.append(planet_list[i])
            starting_point = planet_list[i].split(")")[0]
            # remove from list to make loops faster
            planet_list.pop(i)
            i = 0
        else:
            i += 1

    # split lists so only starting points are left, then reverse lists
    you = [item.split(")")[0] for item in you]
    santa = [item.split(")")[0] for item in santa]
    you.reverse()
    santa.reverse()

    # loop lists and find the last common origo
    for i in range(len(you)):
        if you[i] != santa[i]:
            break
        else:
            common_origo = you[i]

    # reverse lists again and count steps until common origo
    you.reverse()
    santa.reverse()
    your_steps = you.index(common_origo)
    santas_steps = santa.index(common_origo)

    step_count = your_steps + santas_steps

    return step_count


def find_orbiters(celestial_objects, planet_list):
    orbiters = []
    # for loop in reverse so we can remove values from it
    for i in range(len(planet_list) - 1, -1, -1):
        left, right = planet_list[i].split(")")
        if left in celestial_objects:
            orbiters.append(right)
            planet_list.pop(i)
    return orbiters, planet_list


def calculate_orbits(celestial_objects):
    orbits = 0
    for i in range(1, len(celestial_objects)):
        # exclude YOU and SAN
        if "YOU" in celestial_objects[i] or "SAN" in celestial_objects[i]:
            orbits += (len(celestial_objects[i]) - 1) * i
        else:
            orbits += len(celestial_objects[i]) * i
    return orbits


if __name__ == '__main__':
    main()