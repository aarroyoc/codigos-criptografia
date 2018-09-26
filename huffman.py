
class Palabra(object):

    def __init__(self, probabilidad,position):
        self.probabilidad = probabilidad
        self.code = None
        self.position = position

    def __lt__(self,other):
        return self.probabilidad < other.probabilidad

    def unpack(self):
        pass


class Join(object):

    def __init__(self,a,b):
        self.prob_a = a.probabilidad
        self.prob_b = b.probabilidad
        self.probabilidad = self.prob_a + self.prob_b
        self.code = None

        self.a = a
        self.b = b

    def unpack(self):
        self.a.code = self.code + "0"
        self.a.unpack()
        self.b.code = self.code + "1"
        self.b.unpack()

    def __lt__(self,other):
        return self.probabilidad < other.probabilidad

def chose_min_two(lista: list):
    lista.sort(reverse=True)
    x = lista.pop()
    y = lista.pop()
    return (x,y)

def huffman(frecuencias):
    n_palabras = len(frecuencias)

    lista = list(frecuencias)
    while len(lista) > 2:
        x,y = chose_min_two(lista)
        j = Join(x,y)
        lista.append(j)

    lista[0].code = "0"
    lista[0].unpack()
    lista[1].code = "1"
    lista[1].unpack()

    frecuencias.sort(key=lambda x: x.position)
    return frecuencias

if __name__ == "__main__":
    frecuencias = input("Frecuencias de las palabras (separados por coma): ")
    frecuencias = [Palabra(int(x),posicion) for posicion,x in enumerate(frecuencias.split(","))]
    huffman(frecuencias)
    for freq in frecuencias:
        print("Frecuencia: %d\tCódigo: %s" % (freq.probabilidad,freq.code))
