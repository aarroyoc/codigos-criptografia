def mcd(a,b):
    m = a
    n = b

    x = list()
    y = list()

    step = 1
    r = -1
    while r != 0:
        r = m % n
        c = m // n
        #pdb.set_trace()
        if step == 1:
            x.append(1)
            y.append(0)
            step = 2
        if step == 2:
            x.append(0)
            y.append(1)
            step = 3
        if step > 2:
            x.append(x[-2]-c*x[-1])
            y.append(y[-2]-c*y[-1])
        m = n
        n = r

    if m < 0:
        m = -m
        x[-2] = -x[-2]
        y[-2] = -y[-2]
    return (m,x[-2],y[-2])


a = input("Introduzca N números separados por comas: ")
num = a.split(",")
num = [ int(x) for x in num]
original_num = list(num)

bezout = list()
mcd_list = list()

for i in range(len(num)-1):
    m,x,y = mcd(num[i],num[i+1])
    num[i+1] = m
    if i == 0:
        bezout.append(x)
        bezout.append(y)
    else:
        bezout = [x*n for n in bezout]
        bezout.append(y)

print("MCD: %d" % num[-1])
t = list(zip(bezout,original_num))
for e in t:
    print("%d*%d +" % (e[0],e[1]),end="")
print(" = %d" % num[-1])