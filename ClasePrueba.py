import sys
from Alfabeto import Alfabeto
from AFD import AFD
from AFN import AFN
from AFN_e import AFN_Lambda
from ProcesamientoCadenaAFD import ProcesamientoCadenaAFD
from ProcesamientoCadenaAFN import ProcesamientoCadenaAFN
class ClasePrueba:
    def __init__(self, *args):
        pass
    
    def crearAutomata(self):

        opcion = input(
            "--------------------------------------- \n"
            "Seleccione el tipo de automata \n"
            "1. AFD \n"
            "2. AFN \n"
            "3. AFN Lambda \n"
            "4. Salir \n"
            "--------------------------------------- \n"
            )
        #Crear AFD
        alfabeto = (str(input("Ingrese el alfabeto del automata (ej: a-c, 0-9):\n")))
        alfabeto = alfabeto.split(",")
        alfabeto = Alfabeto(alfabeto)   #Generar alfabeto
        
        nroEstados = int(input("Ingrese el numero de estados del automata: \n"))
        estados = list()
        print("Ingrese los estados del automata:")
        for i in range(nroEstados):
            estados.append(input())   #Agregar estados ingresados
        estados = set(sorted(estados))
        print(estados)
        
        inicial = input("Ingrese el estado inicial: \n")
        if inicial not in estados:  #Verificar que el estado inicial se encuentra en los estados ingresados
            raise ValueError("El estado inicial no se encuentra en la lista de estados")
        
        nroAceptacion = int(input("Ingrese el numero de estados de aceptacion: \n"))
        if nroAceptacion > nroEstados:
            raise ValueError("El numero de estados de aceptacion no puede ser mayor al numero de estados")
        print("Ingrese los estados de aceptacion:")
        aceptacion = set()
        for i in range(nroAceptacion):
            inp = input()
            if inp in estados:
                aceptacion.add(inp)
            else:
                raise ValueError("El estado de aceptacion "+aceptacion+ " no se encuentra en la lista de estados")
        
        transiciones = dict()
        print("Ingrese las transiciones del automata:")
        for estado in estados:
            transiciones[estado] = dict()
            for simbolo in alfabeto.simbolos:       #Ingresar transicion de cada estado para cada uno de los simbolos
                transicion = input("Ingrese transicion de "+estado+" con "+simbolo+":\n")
                if transicion == "No":              #Ingresar "No" si no hay transicion
                    next
                elif transicion not in estados:
                    raise ValueError("La transicion de "+estado+" con "+simbolo+" no se encuentra en la lista de estados")
                else:
                    transiciones[estado][simbolo] = set()
                    transiciones[estado][simbolo].add(transicion)
        print(transiciones)

        if opcion == '1':
            self.probarAFD(alfabeto, estados, inicial, aceptacion, transiciones)
        elif opcion == '2':
            self.probarAFN(alfabeto, estados, inicial, aceptacion, transiciones)

    def probarAFD(self, alfabeto, estados, inicial, aceptacion, transiciones):
        
        AFDCreado = AFD(alfabeto, estados, inicial, aceptacion, transiciones)
        procesar = ProcesamientoCadenaAFD(AFDCreado)
        while True:
            procesar.elegirMetodo()
        
    def probarAFN(self, alfabeto, estados, inicial, aceptacion, trancisiones):
        
        AFNCreado = AFN(alfabeto, estados, inicial, aceptacion, trancisiones)
        procesar = ProcesamientoCadenaAFN(AFNCreado)
        while True:
            procesar.elegirMetodo()


    def probarAFNLambda(self):
        pass
    def main(self): # invoca a los otros para que puedan ser comentados facilmente y poder escoger cual se va a probar.
        opcion = input(
            "--------------------------------------- \n"
            "Seleccione una opcion \n"
            "1. Construir automata \n"
            "2. Importar desde archivo \n"
            "4. Salir \n"
            "--------------------------------------- \n"
            )
        
        if opcion == "1":
            self.crearAutomata()
        elif opcion == "2":
            pass
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