

def find_element (arr, size, element):
    pivot = get_pivot_element (arr,size - 1);

    # If we didn't find a pivot,
    # then array is not rotated at all
    if pivot == -1:
        return binarySearch (arr, 0, size - 1, element);
    if arr[pivot] == element:
        return pivot
    if arr[0] <= element:
        return binarySearch (arr, 0, pivot - 1, element);
    return binarySearch (arr, pivot + 1, size - 1, element);


def get_pivot_element (arr,length):
    count=0
    while count < length:
        if arr[count] > arr[count+1]:
            return count
        else:
            count=count+1
    return -1

# Standard Binary Search function*/
def binarySearch (arr, low, high, key):
    if high < low:
        return -1

    mid = int ((low + high) / 2)

    if key == arr[mid]:
        return mid
    if key > arr[mid]:
        return binarySearch (arr, (mid + 1), high,
                             key);
    return binarySearch (arr, low, (mid - 1), key);


# Driver program to check above functions */
# Let us search 3 in below array
rsa = [3, 4, 5, 6, 1, 2]
n = len (rsa)
#print(len(arr1))
key = 4
print ("Index of the element is : ",
       find_element (rsa, n, key))
