

def find_duplicates(input):
    seen = {}
    dupes = []
    for entry in input:
        if entry not in seen.keys():
            seen[entry]=1
        else:
            seen[entry] += 1
            dupes.append(entry)
    return dupes


def main():
    inputList=[1,3,1,2]
    print(find_duplicates(inputList))

if __name__=="__main__":
    main()