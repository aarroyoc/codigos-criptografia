from comun import *

def test_poly_mult():
    poly1 = bytearray([1,5,2])
    poly2 = bytearray([6,1,4,3])
    final = bytearray([6,31,21,25,23,6])
    assert poly_mult(poly1,poly2) == final

def test_sumar():
    clave = bytearray([1,1,1,1,1])
    texto = bytearray([2,2,2,2,2])
    final = bytearray([3,3,3,3,3])
    assert suma_xor(clave,texto) == final

def test_permutacion_filas():
    matrix = bytearray([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    final = bytearray([0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11])
    assert permutacion_filas(matrix) == final

def test_permutacion_columnas():
    matrix = bytearray([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    clave = bytearray([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    res = permutacion_columnas(clave,matrix)
    assert len(res) == 16

def test_permutacion_filas_inv():
    matrix = bytearray([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    cifrado = permutacion_filas(matrix)
    descifrado = permutacion_filas_inv(cifrado)
    assert matrix == descifrado