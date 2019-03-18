
import os
# pass the fully qualified path for your root directory
parent_dir= "/Users/dipanjan/Desktop/AIbooks"
dir_dict={}


# check whether parent dictionary is empty
if len(os.listdir(parent_dir)) == 0:
    print ("Parent Directory is empty")
else:
    sub_dirs=[d[0] for d in os.walk(parent_dir)]
    for dir in sub_dirs:
        #print (dir)
        # 0 value in the dictionary indicates it is empty
        if not os.listdir(dir):
            dir_dict[dir]=0
        # 1 value in the dictionary indicates it is non-empty
        else:
            dir_dict[dir]=1
            #print(os.path.basename(dir))

for k,v in dir_dict.items():
    #print(str(k) + " => " + str(v))
    if v==0:
        print (str(k))











