from solomon_op import *
import itertools
import pdb

NUMS = [
    "0000",
    "0001",
    "0010",
    "0100",
    "1000"
]

GENERATRIZ = [
    ["0011","0010","0001","0000"],
    ["0101","0100","0000","0001"]
]

CONTROL = [
    ["0001","0001","0001","0001"],
    ["0000","0010","0100","1000"]
]

def corregir_letra(code):
    code = code.split(" ")
    fixcodes = list()
    s = sindrome([code],CONTROL)
    if s[0][0] != "0000" or s[0][1] != "0000":
        print("Error encontrado")
        # GENERAR TODOS LOS VECTORES LIDERES Y SUS SINDROMES
        everything = itertools.product(NUMS,NUMS,NUMS,NUMS)
        for vector in everything:
            if sindrome([[vector[0],vector[1],vector[2],vector[3]]],CONTROL) == s:
                fixcodes.append(vector)
        fixcodes.sort(key=lambda x: NUMS.index(x[0])+NUMS.index(x[1])+NUMS.index(x[2])+NUMS.index(x[3]))
        fixcode = fixcodes[0]
        print(fixcode)
        return "%s %s %s %s" % (
            suma(code[0],fixcode[0]),
            suma(code[1],fixcode[1]),
            suma(code[2],fixcode[2]),
            suma(code[3],fixcode[3])
        )
    else:
        return "%s %s %s %s" % (code[0],code[1],code[2],code[3])


def main():
    fichero_in = input("Fichero a corregir: ")
    fichero_out = input("Fichero de salida: ")
    with open(fichero_in,"r") as f:
        texto = f.read()
    codes = texto.split(";")
    with open(fichero_out,"w") as f:
        for code in codes:
            if len(code) < 15:
                continue
            letra = corregir_letra(code)
            f.write(letra+";")
        

if __name__ == '__main__':
    main()