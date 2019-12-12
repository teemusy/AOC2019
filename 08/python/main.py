import textwrap
from collections import Counter
import numpy as np


def main():
    f = open("../8_input.txt", "r")
    picture = f.read()
    f.close()

    width = 25
    height = 6
    size = int(len(picture) / (len(picture) / (width * height)))
    print("Layer size:", size)
    rows = textwrap.wrap(picture, size)
    most_nulls = float('inf')
    layer = None
    for i in range(len(rows)):
        nullcount = Counter(rows[i])['0']
        if nullcount < most_nulls:
            most_nulls = nullcount
            layer = i
    print("Least nulls in layer: {} of {}".format(layer, len(rows) - 1))

    ones = Counter(rows[layer])["1"]
    twos = Counter(rows[layer])["2"]
    result = ones * twos
    print("Ones: {}, twos: {}".format(ones, twos))
    print("First result:", result)

    # reshape layars into 2d and the size of the picture
    layers = []
    rows = [[char for char in n] for n in rows]
    for row in rows:
        row = np.array(row)
        layers.append(np.reshape(row, (height, width)))

    # add spaces to init picture
    picture = np.full((height, width), None, dtype=object)
    for i in range(len(layers)):
        for j in range(len(layers[0])):
            for k in range(len(layers[0][0])):
                if layers[i][j][k] in ("0", "1") and picture[j][k] is None:
                    picture[j][k] = layers[i][j][k]

    for i in range(len(picture)):
        for j in range(len(picture[0])):
            if picture[i][j] == "0":
                picture[i][j] = " "
            else:
                picture[i][j] = 0
            print(picture[i][j], end="")
        print("\n")


if __name__ == '__main__':
    main()