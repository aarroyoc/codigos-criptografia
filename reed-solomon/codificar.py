# CODIFICAR
# El programa codifica un texto según el código Reed-Solomon
from solomon_op import *

NUMS = [
    "0000",
    "0001",
    "0010",
    "0011",
    "0100",
    "0101",
    "0110",
    "0111",
    "1000",
    "1001",
    "1010",
    "1011",
    "1100",
    "1101",
    "1110",
    "1111"
]
def read_file():
    fichero_in = input("Fichero a codificar: ")
    f = open(fichero_in,"r")
    texto = f.readlines()[0]
    f.close()

    b = bytearray()
    b.extend(texto.encode("ascii"))
    return b

def codificar_letra(letra):
    upper = (letra & 0b11110000) >> 4
    lower = letra & 0b00001111
    upper = NUMS[upper]
    lower = NUMS[lower]
    letra = [[upper,lower]]
    return matrixmult(letra,GENERATRIZ)

def codificar_texto(texto):
    codificado = ""
    for letra in texto:
        print("ASCII Code: %d" % letra)
        c_letra = codificar_letra(letra)[0]
        codificado += "%s %s %s %s;" % (c_letra[0],c_letra[1],c_letra[2],c_letra[3])
    return codificado

def escribir_codificado(codificado):
    fichero_out = input("Fichero de salida: ")
    with open(fichero_out,"w") as f:
        f.write(codificado)

POLINOMIO = [1,0,0,1,1]

GENERATRIZ = [
    ["0011","0010","0001","0000"],
    ["0101","0100","0000","0001"]
]

CONTROL = [
    ["0001","0001","0001","0001"],
    ["0000","0010","0100","1000"]
]

def main():
    texto = read_file()
    codificado = codificar_texto(texto)
    escribir_codificado(codificado)

if __name__ == "__main__":
    main()