#Operaciones SUMA/MULTIPLICACION codigo REED-SOLOMON de 16 elementos

elements=[
"0010", #1
"0100", #2
"1000", #3
"0011", #4
"0110", #5
"1100", #6
"1011", #7
"0101", #8
"1010", #9
"0111", #10
"1110", #11
"1111", #12
"1101", #13
"1001", #14
"0001"] # 15


def suma(a,b):
    c = ""
    def suma_binaria(c,d):
        if c == "0" and d == "0":
            return "0"
        elif c == "1" and d == "0":
            return "1"
        elif c == "0" and d == "1":
            return "1"
        else:
            return "0"
    c += suma_binaria(a[0],b[0])
    c += suma_binaria(a[1],b[1])
    c += suma_binaria(a[2],b[2])
    c += suma_binaria(a[3],b[3])
    return c

def producto(a,b):
    if a == "0000" or b == "0000":
        return "0000"
    ia = elements.index(a)+1
    ib = elements.index(b)+1
    producto = (ia+ib) % 15
    return elements[producto-1]

def matrixmult(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
      print("No se pueden multiplicar las matrices")
      return

    C = [["0000" for row in range(cols_B)] for col in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j]=suma(C[i][j],producto(A[i][k],B[k][j]))
    return C

def sindrome(u,H):
    HT = list(map(list, zip(*H)))
    return matrixmult(u,HT)
