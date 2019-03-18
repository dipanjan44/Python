
def fib_recur(n):

  if (n == 0):
      return 0
  if (n == 1):
      return 1
  else:
      return fib_recur(n-1) + fib_recur(n-2)


def fib_calc_iterative(n):

    result=[0 for x in range (n+1)]
    result[0]=0
    result[1]=1
    for i in range (2,n+1):
        result[i]=result[i-1]+result[i-2]
    return result[n]

print("Printing from the iterative method:" +str(fib_calc_iterative(8)))
print("Printing from the recursive method:" +str(fib_recur(8)))