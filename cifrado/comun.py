# SEGUIR EL ORDEN DE BITS DEL AES

from numpy.linalg import inv

def poly_mult(pol1,pol2):
    res = [0]*(len(pol1)+len(pol2)-1)
    for o1,i1 in enumerate(pol1):
        for o2,i2 in enumerate(pol2):
            res[o1+o2] += i1*i2
    return bytearray(res)

def poly_mult_modulo(pol1,pol2):
    pol = bytearray(4)
    pol[0] = (pol1[0]*pol2[3]) ^ (pol1[1]*pol2[2]) ^ (pol1[2]*pol2[1]) ^ (pol1[3]*pol2[0])
    pol[1] = (pol1[1]*pol2[3]) ^ (pol1[2]*pol2[2]) ^ (pol1[3]*pol2[1]) ^ (pol1[0]*pol2[0])
    pol[2] = (pol1[2]*pol2[3]) ^ (pol1[3]*pol2[2]) ^ (pol1[0]*pol2[1]) ^ (pol1[1]*pol2[0])
    pol[3] = (pol1[3]*pol2[3]) ^ (pol1[0]*pol2[2]) ^ (pol1[1]*pol2[1]) ^ (pol1[2]*pol2[0])
    return pol

def sustitucion_afin(clave,matrix,ronda=1):
    '''
    Sustitucion afin. Seguir orden de bits de AES
    '''
    i = 0
    if ronda == 2:
        i = 5
    matrix_mult = bytearray(16)
    matrix_mult[0] = clave[i] & 0b0001
    matrix_mult[1] = (clave[i] & 0b0010) >> 1
    matrix_mult[2] = (clave[i] & 0b0100) >> 2
    matrix_mult[3] = (clave[i] & 0b1000) >> 3
    matrix_mult[4] = clave[i+1] & 0b0001
    matrix_mult[5] = (clave[i+1] & 0b0010) >> 1
    matrix_mult[6] = (clave[i+1] & 0b0100) >> 2
    matrix_mult[7] = (clave[i+1] & 0b1000) >> 3
    matrix_mult[8] = clave[i+2] & 0b0001
    matrix_mult[9] = (clave[i+2] & 0b0010) >> 1
    matrix_mult[10] = (clave[i+2] & 0b0100) >> 2
    matrix_mult[11] = (clave[i+2] & 0b1000) >> 3
    matrix_mult[12] = clave[i+3] & 0b0001
    matrix_mult[13] = (clave[i+3] & 0b0010) >> 1
    matrix_mult[14] = (clave[i+3] & 0b0100) >> 2
    matrix_mult[15] = (clave[i+3] & 0b1000) >> 3

    suma = bytearray(4)
    suma[0] = clave[i+4] & 0b0001
    suma[1] = (clave[i+4] & 0b0010) >> 1
    suma[2] = (clave[i+4] & 0b0100) >> 2
    suma[3] = (clave[i+4] & 0b1000) >> 3

    for block in range(0,len(matrix)):
        b = bytearray(4)
        b[0] = matrix[block] & 0b0001
        b[1] = (matrix[block] & 0b0010) >> 1
        b[2] = (matrix[block] & 0b0100) >> 2
        b[3] = (matrix[block] & 0b1000) >> 3

        # (MATRIX_MULT * B)
        p = bytearray(4) 
        p[0] = matrix_mult[0]*b[0] ^ matrix_mult[4]*b[1] ^ matrix_mult[8]*b[2] ^ matrix_mult[12]*b[3]
        p[1] = matrix_mult[1]*b[0] ^ matrix_mult[5]*b[1] ^ matrix_mult[9]*b[2] ^ matrix_mult[13]*b[3]
        p[2] = matrix_mult[2]*b[0] ^ matrix_mult[6]*b[1] ^ matrix_mult[10]*b[2] ^ matrix_mult[14]*b[3]
        p[3] = matrix_mult[3]*b[0] ^ matrix_mult[7]*b[1] ^ matrix_mult[11]*b[2] ^ matrix_mult[15]*b[3]

        # + SUMA
        p = suma_xor(p,suma) # b es bytearray y debería ser int
        b = p[3]*8 + p[2]*4 + p[1]*2 + p[0]*1
        matrix[block] = b


def sustitucion_afin_inv(clave,matrix,ronda=1):
    i = 0
    if ronda == 2:
        i = 5
    matrix_mult = bytearray(16)
    matrix_mult[0] = clave[i] & 0b0001
    matrix_mult[1] = (clave[i] & 0b0010) >> 1
    matrix_mult[2] = (clave[i] & 0b0100) >> 2
    matrix_mult[3] = (clave[i] & 0b1000) >> 3
    matrix_mult[4] = clave[i+1] & 0b0001
    matrix_mult[5] = (clave[i+1] & 0b0010) >> 1
    matrix_mult[6] = (clave[i+1] & 0b0100) >> 2
    matrix_mult[7] = (clave[i+1] & 0b1000) >> 3
    matrix_mult[8] = clave[i+2] & 0b0001
    matrix_mult[9] = (clave[i+2] & 0b0010) >> 1
    matrix_mult[10] = (clave[i+2] & 0b0100) >> 2
    matrix_mult[11] = (clave[i+2] & 0b1000) >> 3
    matrix_mult[12] = clave[i+3] & 0b0001
    matrix_mult[13] = (clave[i+3] & 0b0010) >> 1
    matrix_mult[14] = (clave[i+3] & 0b0100) >> 2
    matrix_mult[15] = (clave[i+3] & 0b1000) >> 3

    suma = bytearray(4)
    suma[0] = clave[i+4] & 0b0001
    suma[1] = (clave[i+4] & 0b0010) >> 1
    suma[2] = (clave[i+4] & 0b0100) >> 2
    suma[3] = (clave[i+4] & 0b1000) >> 3

    for block in range(0,len(matrix)):
        b = bytearray(4)
        b[0] = matrix[block] & 0b0001
        b[1] = (matrix[block] & 0b0010) >> 1
        b[2] = (matrix[block] & 0b0100) >> 2
        b[3] = (matrix[block] & 0b1000) >> 3

        # + SUMA
        b = suma_xor(b,suma) # b es bytearray y debería ser int

        # (INV(MATRIX_MULT) * B)
        mm = [
            [matrix_mult[0],matrix_mult[4],matrix_mult[8],matrix_mult[12]],
            [matrix_mult[1],matrix_mult[5],matrix_mult[9],matrix_mult[13]],
            [matrix_mult[2],matrix_mult[6],matrix_mult[10],matrix_mult[14]],
            [matrix_mult[3],matrix_mult[7],matrix_mult[11],matrix_mult[15]]
        ]
        m = getMatrixInverse(mm)
        matrix_mult = [
            int(m[0][0]),
            int(m[1][0]),
            int(m[2][0]),
            int(m[3][0]),
            int(m[0][1]),
            int(m[1][1]),
            int(m[2][1]),
            int(m[3][1]),
            int(m[0][2]),
            int(m[1][2]),
            int(m[2][2]),
            int(m[3][2]),
            int(m[0][3]),
            int(m[1][3]),
            int(m[2][3]),
            int(m[3][3])
        ]
        p = bytearray(4)
        p[0] = (matrix_mult[0]*b[0] ^ matrix_mult[4]*b[1] ^ matrix_mult[8]*b[2] ^ matrix_mult[12]*b[3]) % 2
        p[1] = (matrix_mult[1]*b[0] ^ matrix_mult[5]*b[1] ^ matrix_mult[9]*b[2] ^ matrix_mult[13]*b[3]) % 2
        p[2] = (matrix_mult[2]*b[0] ^ matrix_mult[6]*b[1] ^ matrix_mult[10]*b[2] ^ matrix_mult[14]*b[3]) % 2
        p[3] = (matrix_mult[3]*b[0] ^ matrix_mult[7]*b[1] ^ matrix_mult[11]*b[2] ^ matrix_mult[15]*b[3]) % 2

        p = p[3]*8 + p[2]*4 + p[1]*2 + p[0]*1
        matrix[block] = p




def permutacion_filas(matrix):
    '''
    Permutacion de filas AES
    '''
    if not len(matrix) == 16:
        raise Exception("Not a matrix")
    new = bytearray(16)
    new[0] = matrix[0]
    new[1] = matrix[5]
    new[2] = matrix[10]
    new[3] = matrix[15]
    new[4] = matrix[4]
    new[5] = matrix[9]
    new[6] = matrix[14]
    new[7] = matrix[3]
    new[8] = matrix[8]
    new[9] = matrix[13]
    new[10] = matrix[2]
    new[11] = matrix[7]
    new[12] = matrix[12]
    new[13] = matrix[1]
    new[14] = matrix[6]
    new[15] = matrix[11]
    return new

def permutacion_filas_inv(matrix):
    '''
    Permutación de filas AES. Inverso
    '''
    if not len(matrix) == 16:
        raise Exception("Not a matrix")
    new = bytearray(16)
    new[0] = matrix[0]
    new[1] = matrix[13]
    new[2] = matrix[10]
    new[3] = matrix[7]
    new[4] = matrix[4]
    new[5] = matrix[1]
    new[6] = matrix[14]
    new[7] = matrix[11]
    new[8] = matrix[8]
    new[9] = matrix[5]
    new[10] = matrix[2]
    new[11] = matrix[15]
    new[12] = matrix[12]
    new[13] = matrix[9]
    new[14] = matrix[6]
    new[15] = matrix[3]
    return new
def permutacion_columnas(clave,matrix):
    '''
    Permutación de columnas. Similar a AES pero con polinomio distinto
    El polinomio viene dado por la clave. Para descencriptar hace falta buscar el polinomio inverso
    '''
    poly = bytearray(4)
    poly[0] = 1
    poly[1] = clave[10]
    poly[2] = clave[11]
    poly[3] = clave[12]

    col1 = bytearray(4)
    col1[0] = matrix[0]
    col1[1] = matrix[1]
    col1[2] = matrix[2]
    col1[3] = matrix[3]

    col2 = bytearray(4)
    col2[0] = matrix[4]
    col2[1] = matrix[5]
    col2[2] = matrix[6]
    col2[3] = matrix[7]

    col3 = bytearray(4)
    col3[0] = matrix[8]
    col3[1] = matrix[9]
    col3[2] = matrix[10]
    col3[3] = matrix[11]

    col4 = bytearray(4)
    col4[0] = matrix[12]
    col4[1] = matrix[13]
    col4[2] = matrix[14]
    col4[3] = matrix[15]
    
    col1 = poly_mult_modulo(col1,poly)
    col2 = poly_mult_modulo(col2,poly)
    col3 = poly_mult_modulo(col3,poly)
    col4 = poly_mult_modulo(col4,poly)

    new = bytearray()
    new.extend(col1)
    new.extend(col2)
    new.extend(col3)
    new.extend(col4)

    return new


def suma_xor(clave,matrix):
    '''
    Suma (XOR) de dos matrices
    '''
    return bytearray([pair[0] ^ pair[1] for pair in zip(clave,matrix)])

'''
Operaciones con matrices
'''
def transposeMatrix(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
            #cofactors[r][c] %= 2
    return cofactors