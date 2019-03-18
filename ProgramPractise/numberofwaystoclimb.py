
def count_ways_recursive(n):
    if n < 0:
        return 0

    if n==0:
        return 1
    else :
        return count_ways_recursive(n-1) + count_ways_recursive(n-3) +count_ways_recursive(n-2)




def no_of_ways(n):
    count = [0 for i in range(n + 1)]

    count[0] = 1
    count[1] = 1
    count[2] = 2

    for i in range(3, n + 1):
        count[i] = count[i - 1] + count[i - 2] + count[i - 3]

    return count[n]


def main():
    steps = input("Enter the desired no of steps:" +"\n")
    print(" Recursive solution : " + str(count_ways_recursive(int(steps))))
    print(" Iterative solution : " + str(no_of_ways(int(steps))))


if __name__ == "__main__": main()
