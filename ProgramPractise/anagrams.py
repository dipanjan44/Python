
def checkanagram(str1,str2):
    if len(str1) != len(str2):
        return False
    for i in range(0, len(str1)):
        if str1[i]!= str2[i]:
            return False
    return True

def main():
    input = ["abcg", "bcg"]
    string1 = ''.join(sorted(input[0].lower()))
    string2 = ''.join(sorted(input[1].lower()))
    print(checkanagram (string1, string2))

if __name__=="__main__": main()


