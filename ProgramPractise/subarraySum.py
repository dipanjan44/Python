


def check_subarray (inputList, sum):
    sum_dict = {}
    current_sum = 0
    count=0
    for i in range (0, len (inputList)):
        if len (inputList) == 0:
            return "Input list is empty"

        current_sum = current_sum + inputList[i]

        if current_sum - sum == 0:
            count=count+1
            #return (0, i)
        if (current_sum - sum) in sum_dict.keys ():
            count=count+1
            #return (sum_dict[current_sum - sum] + 1, i)
        sum_dict[current_sum] = i

    if count ==0:
        return ("Subarray not found")
    else:
        return ("No of subarray: " +str(count))




def main ():
    inputList = [1, 2, 4, 5, 3,6]
    sum = 9
    print (check_subarray(inputList,sum))


if __name__== "__main__" :main()
