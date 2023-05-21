# Debido al formato de entrada, por ejemplo:
#         #alphabet
#         a-c
# Se debe usar un FOR para generar un arreglo de simbolos usando la numeracion ASCII
# para ir desde (int) ASCII(a) hasta (int) ASCII(b) incluido
# Ese arreglo se llamará simbolos[]
# luego se usa ese arreglo para generar cadenas--> generarCadenaAleatoria(int n)

import random
import re


class Alfabeto:
    simbolos = []
    formato_entrada=None

    def __init__(self, a_c):
        if a_c=='' or a_c==None:
            pass
        else:
            self.formato_entrada=a_c
            for i in a_c:
                if ("$" in i):
                    raise ValueError(
                        "Lambda no permitido como simbolo para el alfabeto")
                elif (len(i) == 1):
                    self.simbolos.append(i[0])
                elif (i[1] == "-"):
                    self.generarListaSimbolos(i[0], i[2])
                else:
                    raise ValueError("Entrada de simbolos", i,
                                    "no permitida para el alfabeto")
            (self.simbolos).sort()

    def generarListaSimbolos(self, min, max):
        if(ord(max) - ord(min)==1):
            self.simbolos=[min, max]
        else:
            for i in range(ord(min), ord(max)+1):
                self.simbolos.append(chr(i))

    def generarCadenaAleatoria(self, n: int):
        string = ""
        for i in range(n):
            string += self.simbolos[random.randint(0, len(self.simbolos)-1)]
        return string

    @staticmethod
    def validate_regex(cadena, expresion_regular) -> bool:
        return (re.match(expresion_regular, cadena))

    def toStringEntrada(self) -> str:
        S=""
        for i in self.formato_entrada:
            if(self.formato_entrada.index(i)==0):
                S=S+i
            else:
                S=S+"\n"+i
        return S
    def prueba (self, otro_alfabeto: "Alfabeto"):
        pass

# ejemplo = ["z", "0-5", "a", "b", "p", "k-o"]
# alf1 = Alfabeto(ejemplo)
# #print(alf1.simbolos)

# print(alf1.toStringEntrada())
# # alf = Alfabeto("a-f")
# # print(alf.generarCadenaAleatoria(12))

# # alf2 = Alfabeto("0-3")
# # print(alf2.generarCadenaAleatoria(12))
