from collections import Counter, OrderedDict
from huffman import huffman, Palabra

texto = input("Introduce un texto: ")
count = Counter(texto)
count = OrderedDict(count)
frecuencias = [Palabra(int(x),posicion) for posicion,x in enumerate(count.values())]
x = huffman(frecuencias)
result = zip(count.keys(),[e.code for e in x])
for r in result:
    print("Palabra: %s\tCódigo: %s" % (r[0],r[1]))


