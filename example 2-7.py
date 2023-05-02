max=int(input())
value=list(range(1, max+1))
for i in range(2,max//2+1):
    j=1
    while(j<len(value)):
        if value[j]<=i:
            j+=1
            continue
        if value[j]%i==0:
            del value[j]
        else:
            j+=1

print(value)