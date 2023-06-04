import sys
from Alfabeto import Alfabeto
from AFD import AFD
class ClasePrueba:
    def __init__(self, *args):
        pass

    def probarAFD(self):
        #Crear AFD
        alfabeto = (str(input("Ingrese el alfabeto del AFD (ej: a-c, 0-9):\n")))
        alfabeto = alfabeto.split(",")
        alfabeto = Alfabeto(alfabeto)   #Generar alfabeto
        
        nroEstados = int(input("Ingrese el numero de estados del AFD: \n"))
        estados = list()
        print("Ingrese los estados del AFD:")
        for i in range(nroEstados):
            estados.append(input())   #Agregar estados ingresados
        estados = set(sorted(estados))
        print(estados)
        
        inicial = input("Ingrese el estado inicial: \n")
        if inicial not in estados:  #Verificar que el estado inicial se encuentra en los estados ingresados
            raise ValueError("El estado inicial no se encuentra en la lista de estados")
        
        nroAceptacion = int(input("Ingrese el numero de estados de aceptacion: \n"))
        print("Ingrese los estados de aceptacion:")
        aceptacion = set()
        for i in range(nroAceptacion):
            inp = input()
            if inp in estados:
                aceptacion.add(inp)
            else:
                raise ValueError("El estado de aceptacion "+aceptacion+ " no se encuentra en la lista de estados")
        
        transiciones = dict()
        print("Ingrese las transiciones del AFD:")
        for estado in estados:
            transiciones[estado] = dict()
            for simbolo in alfabeto.simbolos:       #Ingresar transicion de cada estado para cada uno de los simbolos
                transicion = input("Ingrese transicion de "+estado+" con "+simbolo+":\n")
                if transicion == "No":              #Ingresar "No" si no hay transicion
                    next
                elif transicion not in estados:
                    raise ValueError("La transicion de "+estado+" con "+simbolo+" no se encuentra en la lista de estados")
                else:
                    transicion = list(transicion)
                    transicion = "".join(transicion)
                    transiciones[estado][simbolo] = transicion
        
        AFDCreado = AFD(alfabeto, estados, inicial, aceptacion, transiciones)
        #print(AFDCreado.procesarCadenaConDetalles('aaabbb'))
        
    def probarAFN(self):
        pass
    def probarAFNLambda(self):
        pass
    def main(self): # invoca a los otros para que puedan ser comentados facilmente y poder escoger cual se va a probar.
        opcion = input(
            "--------------------------------------- \n"
            "Seleccione metodo a probar \n"
            "1. AFD \n"
            "2. AFN \n"
            "3. AFN Lambda \n"
            "4. Salir \n"
            "--------------------------------------- \n"
            )
        
        if opcion == "1":
            self.probarAFD()
        elif opcion == "2":
            self.probarAFN()
        elif opcion == "3":
            self.probarAFNLambda()
        elif opcion == "4":
            sys.exit()

    def probarAFNtoAFD(self):
        pass
    def probarAFNLambdaToAFN(self):
        pass
    def probarAFNLambdaToAFN(self):
        pass
    def probarComplemento(self):
        pass
    def probarProductoCartesiano(self):
        pass
    def probarSimplificacion(self):
        pass

Start = ClasePrueba()

Start.main()