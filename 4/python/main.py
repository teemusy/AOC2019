from tqdm import trange
import numpy as np
start = 234208
end = 765869
possible_passwords_1 = []
possible_passwords_2 = []

for x in trange(start, end + 1):
    # split x into list of integers
    x = np.array(list(str(x)))
    # make ordered list from x and invert it to be from small to large
    ordered = np.sort(x)[::-1]
    # if x is equal to ordered list than it matches the requirement that numbers never decrease
    # and if unique numbers is smaller than the length of x than there's at least 1 pair
    if np.array_equal(x, ordered) and len(x) != len(np.unique(x)):
        possible_passwords_1.append(x)
        # check if x contains at least 1 pair
        if 2 in np.unique(x, return_counts=True)[1]:
            possible_passwords_2.append(x)

print(len(possible_passwords_1))
print(len(possible_passwords_2))
