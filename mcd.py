import pdb

print("Máximo Común Divisor")
a = input("Primer número: ")
b = input("Segundo número: ")
a = int(a)
b = int(b)

def mcd(a,b):
    #m = max(a,b)
    m = a
    #n = min(a,b)
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

m,x,y = mcd(a,b)
print("MCD: %d" % m)
print("Bezout: %d*%d + %d*%d = %d" % (x,a,y,b,m))