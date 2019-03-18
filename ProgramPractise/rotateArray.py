def leftShift (inputList, noOfMoves):
    count=0
    while count < noOfMoves:
        item=inputList.pop(0)
        inputList.append(item)
        count=count+1
    return inputList

def rightShift (inputList, noOfMoves):
    count=0
    while count < noOfMoves:
        item=inputList.pop()
        inputList.insert(0,item)
        count=count+1
    return inputList

def main():

    inputList=[1,2,3,4,5,6,7,8,9]
    noOfMoves=4
    print(leftShift(inputList,noOfMoves))
    print (rightShift (inputList, noOfMoves))

if __name__ == "__main__": main ()