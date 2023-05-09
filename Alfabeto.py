#Debido al formato de entrada, por ejemplo:
#         #alphabet
#         a-c
# Se debe usar un FOR para generar un arreglo de simbolos usando la numeracion ASCII
# para ir desde (int) ASCII(a) hasta (int) ASCII(b) incluido
# Ese arreglo se llamará simbolos[]
#luego se usa ese arreglo para generar cadenas--> generarCadenaAleatoria(int n)

import random


class Alfabeto:
    simbolos = []
    def __init__(self, a_c):
        char = a_c.split("-")
        self.min=char[0]
        self.max=char[1]
        if(self.min=="$" or self.max=="$"): raise ValueError("Rango de caracteres no valido, no se acepta lambda como uno de los rangos")
        self.generarListaSimbolos(self.min, self.max)

    def generarListaSimbolos(self, min, max):
        for i in range (ord(min) , ord(max)+1):
            self.simbolos.append(chr(i))
        # print("min: ", self.min, "\nmax: ", self.max, "\nsimbolos: ", self.simbolos)
        # print("min-num: ", ord(self.min), "\nmax-num: ", ord(self.max))
    
    def generarCadenaAleatoria(self, n: int):
        string=""
        for i in range (n):
            string += self.simbolos[random.randint(0, len(self.simbolos)-1)]
        return string

# alf = Alfabeto("a-f")
# print(alf.generarCadenaAleatoria(12))

# alf2 = Alfabeto("0-3")
# print(alf2.generarCadenaAleatoria(12))