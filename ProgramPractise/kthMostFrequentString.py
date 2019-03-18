
import operator


input = (["a", "b", "c", "a", "b", "a"], 1)

string_dict = {}
frequency=input[1]

for char in input[0]:

    if char not in string_dict.keys ():
        string_dict[char] = 1
    else:
        count = string_dict[char]
        count = count + 1
        string_dict[char] = count


for k,v in string_dict.items():
    out_list=[]
    if (v == frequency):
        out_string=k+ ": " +str(v)
        out_list.append(out_string)

print(out_list)
