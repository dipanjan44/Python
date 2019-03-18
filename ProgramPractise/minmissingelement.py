


def solution(A):
    # write your code in Python 3.6
    new_array = set(sorted(A))
    if (new_array[0] != 1):
        return 1

    for i in range(0, len(new_array)):
        if new_array[i + 1] != new_array[i] + 1:
            return new_array[i] + 1
    return new_array[-1]+1

