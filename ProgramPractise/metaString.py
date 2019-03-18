# Returns true if str1 and str2 are meta strings
def areMetaStrings(str1, str2):
    len1 = len(str1)
    len2 = len(str2)

    # Return false if both are not of equal length
    if (len1 != len2):
        return False

    # To store indexes of previously mismatched
    # characters
    prev = -1
    curr = -1

    count = 0
    i = 0
    while i < len1:

        # If current character doesn't match
        if (str1[i] != str2[i]):

            # Count number of unmatched character
            count = count + 1

            # If unmatched are greater than 2,
            # then return false
            if (count > 2):
                return False

            # Store both unmatched characters of
            # both strings
            prev = curr
            curr = i

        i = i + 1

    # Check if previous unmatched of string1
    # is equal to curr unmatched of string2
    # and also check for curr unmatched character,
    # if both are same, then return true
    return (count == 2 and str1[prev] == str2[curr]
            and str1[curr] == str2[prev])


# Driver method
str1 = "sgeek"
str2 = "geeks"
if (areMetaStrings(str1, str2)):
    print("Yes")
else:
    print("No")
