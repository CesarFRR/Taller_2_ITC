import sys
from Graph import graficarAutomata

class ProcesamientoCadenaAFN:
    cadena = None
    esAceptada = None
    listaProcesamientosAbortados = None
    listaProcesamientosAceptacion = None
    listaProcesamientosRechazados = None
    procesamiento = True
    AFN = None
    def __init__(self, afn):
        self.AFN = afn
        self.cadena = input("--------------------------------------------"+
                            "Ingrese una cadena:")

    def elegirMetodo(self):
        opcion = input(
            "--------------------------------------- \n"
            "Elija el metodo de procesamiento: \n"
            "1. Procesamiento \n"
            "2. Procesamiento con detalles \n"
            "3. Computar Todos los procesamientos \n"
            "G. Graficar automata \n"
            "0. Salir \n"
            "--------------------------------------- \n"
        )
        if opcion == "1":
            esAceptada = self.AFN.procesarCadena(self.cadena)
            return print(esAceptada)

        elif opcion == "2":
            esAceptada = self.AFN.procesarCadenaConDetalles(self.cadena)
            return print(esAceptada)

        elif opcion == "3":
            procesamientos = self.AFN.computarTodosLosProcesamientos(self.cadena, "procesamientoAFN.txt")

            return print(procesamientos)
        
        elif opcion == "G":
            grafo = graficarAutomata()
            grafo.mostrarGrafo(self.AFN)

        elif opcion == "0":
            sys.exit()

