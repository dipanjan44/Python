inputString="aabcccccaaa"


char_map={}
for entry in inputString:
    if entry in char_map:
        char_map[entry]=char_map.get(entry)+1
    else:
        char_map[entry]=1

if len(inputString) < len(char_map):
    print(inputString)
else:
    for k,v in char_map.items():
        print("The char is : "  +k +" and the value is : " +str(v))