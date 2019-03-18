
import sys

def floor(n,fl):
    eggfloor=[[0 for x in range(fl+1)] for x in range(n+1)]
    for i in range (1,n+1):
        eggfloor[i][1]=1
        eggfloor[i][0]=0

    for j in range (1, fl+1):
        eggfloor[1][j]=j

    for i in range (2,n+1):
        for j in range (2,fl+1):
            eggfloor[i][j]=sys.maxsize
            for x in range (1,j+1):
                res=1+ max(eggfloor[i-1][x-1],eggfloor[i][j-x])
                if res < eggfloor[i][j]:
                    eggfloor[i][j]=res
    return eggfloor[n][fl]


def main():

    input = [2,10]

    n= input[0]
    fl=input[1]

    print(floor(n,fl))

if __name__=="__main__": main()