import sys


def minimum_floor(n, k):
    if (k == 0) or (k == 1):
        return k

    if (n == 1):
        return k

    min = sys.maxsize
    for x in range(1, k + 1):
        res = max(minimum_floor(n, k - x), minimum_floor(n - 1, x - 1))

        if res < min:
            min = res
    return min + 1


def main():
    input = [2, 10]
    no_of_eggs = input[0]
    no_of_floor = input[1]

    print(minimum_floor(no_of_eggs, no_of_floor))


if __name__ == "__main__": main()
