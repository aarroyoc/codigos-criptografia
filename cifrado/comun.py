# SEGUIR EL ORDEN DE BITS DEL AES
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
    matrix_mult = bytearray(16)
    matrix_mult[0] = clave[0] & 0b0001
    matrix_mult[1] = clave[0] & 0b0010
    matrix_mult[2] = clave[0] & 0b0100
    matrix_mult[3] = clave[0] & 0b1000
    matrix_mult[4] = clave[1] & 0b0001
    matrix_mult[5] = clave[1] & 0b0010
    matrix_mult[6] = clave[1] & 0b0100
    matrix_mult[7] = clave[1] & 0b1000
    matrix_mult[8] = clave[2] & 0b0001
    matrix_mult[9] = clave[2] & 0b0010
    matrix_mult[10] = clave[2] & 0b0100
    matrix_mult[11] = clave[2] & 0b1000
    matrix_mult[12] = clave[3] & 0b0001
    matrix_mult[13] = clave[3] & 0b0010
    matrix_mult[14] = clave[3] & 0b0100
    matrix_mult[15] = clave[3] & 0b1000

    suma = bytearray(4)
    suma[0] = clave[4] & 0b0001
    suma[1] = clave[4] & 0b0010
    suma[2] = clave[4] & 0b0100
    suma[3] = clave[4] & 0b1000

    for block in range(0,len(matrix)):
        b = bytearray(4)
        b[0] = matrix[block] & 0b0001
        b[1] = matrix[block] & 0b0010
        b[2] = matrix[block] & 0b0100
        b[3] = matrix[block] & 0b1000

        # (MATRIX_MULT * B) 
        b[0] = matrix_mult[0]*b[0] ^ matrix_mult[4]*b[1] ^ matrix_mult[8]*b[2] ^ matrix_mult[12]*b[3]
        b[1] = matrix_mult[1]*b[0] ^ matrix_mult[5]*b[1] ^ matrix_mult[9]*b[2] ^ matrix_mult[13]*b[3]
        b[2] = matrix_mult[2]*b[0] ^ matrix_mult[6]*b[1] ^ matrix_mult[10]*b[2] ^ matrix_mult[14]*b[3]
        b[3] = matrix_mult[3]*b[0] ^ matrix_mult[7]*b[1] ^ matrix_mult[11]*b[2] ^ matrix_mult[15]*b[3]

        # + SUMA
        b = suma_xor(b,suma) # b es bytearray y debería ser int
        b = b[0]*8 + b[1]*4 + b[2]*2 + b[3]*1
        matrix[block] = b



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

