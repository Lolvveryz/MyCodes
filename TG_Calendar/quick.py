import random

array = [random.randint(0, 15) for i in range(10)]


def quick(arr):
    if len(arr) == 1:
        return arr[0]

    less = []
    biger = []

    for i in range(len(arr) - 1):
        if arr[i] <= arr[-1]:
            less.append(i)
        else:
            biger.append(i)

    le = quick(less)
    big = quick(biger)

    return arr[*le, arr[-1], *big]


print(quick(array))
