from comun import *

def cifrar_bloque(clave,matrix):
    #matrix = sustitucion_afin(clave,matrix,1)
    matrix = permutacion_filas(matrix)
    #matrix = permutacion_columnas(clave,matrix)
    matrix = suma_xor(clave,matrix)
    #matrix = sustitucion_afin(clave,matrix,2)
    matrix = permutacion_filas(matrix)
    #matrix = permutacion_columnas(clave,matrix)
    return matrix


if __name__ == "__main__":
    clave_file = input("Fichero de la clave: ")
    input_file = input("Fichero a cifrar: ")
    output_file = input("Fichero de salida: ")
    clave_bytes = open(clave_file,"rb").read()
    input_bytes = open(input_file,"rb").read()
    clave = bytearray(16)
    clave[0] = (clave_bytes[0] & 0b11110000) >> 4
    clave[1] = clave_bytes[0] & 0b00001111
    clave[2] = (clave_bytes[1] & 0b11110000) >> 4
    clave[3] = clave_bytes[1] & 0b00001111
    clave[4] = (clave_bytes[2] & 0b11110000) >> 4
    clave[5] = clave_bytes[2] & 0b00001111
    clave[6] = (clave_bytes[3] & 0b11110000) >> 4
    clave[7] = clave_bytes[3] & 0b00001111
    clave[8] = (clave_bytes[4] & 0b11110000) >> 4
    clave[9] = clave_bytes[4] & 0b00001111
    clave[10] = (clave_bytes[5] & 0b11110000) >> 4
    clave[11] = clave_bytes[5] & 0b00001111
    clave[12] = (clave_bytes[6] & 0b11110000) >> 4
    clave[13] = clave_bytes[6] & 0b00001111
    clave[14] = (clave_bytes[7] & 0b11110000) >> 4
    clave[15] = clave_bytes[7] & 0b00001111
    # Cada matriz es de 8 bytes
    # 16 bloques
    # Bloques de 4 BITS
    if len(input_bytes) % 8 != 0:
        raise Error("El tamaño del texto no es válido")
    i = 0
    with open(output_file,"wb") as f:
        while i < len(input_bytes):
            matrix = bytearray(16)
            matrix[0] = (input_bytes[i] & 0b11110000) >> 4
            matrix[1] = input_bytes[i] & 0b00001111
            matrix[2] = (input_bytes[i+1] & 0b11110000) >> 4
            matrix[3] = input_bytes[i+1] & 0b00001111
            matrix[4] = (input_bytes[i+2] & 0b11110000) >> 4
            matrix[5] = input_bytes[i+2] & 0b00001111
            matrix[6] = (input_bytes[i+3] & 0b11110000) >> 4
            matrix[7] = input_bytes[i+3] & 0b00001111
            matrix[8] = (input_bytes[i+4] & 0b11110000) >> 4
            matrix[9] = input_bytes[i+4] & 0b00001111
            matrix[10] = (input_bytes[i+5] & 0b11110000) >> 4
            matrix[11] = input_bytes[i+5] & 0b00001111
            matrix[12] = (input_bytes[i+6] & 0b11110000) >> 4
            matrix[13] = input_bytes[i+6] & 0b00001111
            matrix[14] = (input_bytes[i+7] & 0b11110000) >> 4
            matrix[15] = input_bytes[i+7] & 0b00001111

            matrix = cifrar_bloque(clave,matrix)

            j = 0
            write = bytearray(8)
            while j < len(matrix):
                letra = (matrix[j] << 4) + matrix[j+1]
                write[j // 2] = letra
                j += 2
            f.write(write)
            i += 8
    print("CIFRADO EXITOSO")
    