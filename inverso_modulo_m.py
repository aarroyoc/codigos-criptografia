num = input("Introduzca el número")
num = int(num)
mod = input("Introduzca el módulo")
mod = int(mod)

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

m,x,y = mcd(num,mod)
if m > 1:
    print("No existe inverso")
else:
    print("El inverso es %d" % x)