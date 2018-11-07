from solomon_op import *

GENERATRIZ = [
    ["0011","0010","0001","0000"],
    ["0101","0100","0000","0001"]
]

CONTROL = [
    ["0001","0001","0001","0001"],
    ["0000","0010","0100","1000"]
]

def decodificar_letra(code):
    code = code.split(" ")
    s = sindrome([code],CONTROL)
    if s[0][0] != "0000" or s[0][1] != "0000":
        raise Exception("Ha ocurrido un fallo en la transmisión del mensaje")
    letra = int(code[2]+code[3],2)
    return bytes([letra])

def main():
    fichero = input("Fichero codificado: ")
    with open(fichero,"r") as f:
        texto = f.read()
    blocks = texto.split(";")
    texto = bytes()
    for block in blocks:
        if len(block) == 0:
            continue
        letra = decodificar_letra(block)
        texto += letra
    print(texto.decode("ascii"))
    

if __name__ == "__main__":
    main()

