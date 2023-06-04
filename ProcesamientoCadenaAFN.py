from AFN import nfa1
import sys

class ProcesamientoCadenaAFN:
    cadena = None
    esAceptada = None
    listaProcesamientosAbortados = None
    listaProcesamientosAceptacion = None
    listaProcesamientosRechazados = None
    procesamiento = True
    def __init__(self):
        self.cadena = input("Ingrese una cadena:")

    def elegirMetodo(self):
        opcion = input(
            "--------------------------------------- \n"
            "Elija el metodo de procesamiento: \n"
            "1. Procesamiento \n"
            "2. Procesamiento con detalles \n"
            "3. Computar Todos los procesamientos \n"
            "0. Salir \n"
            "--------------------------------------- \n"
        )
        if opcion == "1":
            esAceptada = nfa1.procesarCadena(self.cadena)
            return print(esAceptada)

        elif opcion == "2":
            esAceptada = nfa1.procesarCadenaConDetalles(self.cadena)
            return print(esAceptada)

        elif opcion == "3":
            procesamientos = nfa1.computarTodosLosProcesamientos(self.cadena, "procesamientoAFN.txt")
            self.listaProcesamientosAbortados = nfa1.abortadas
            self.listaProcesamientosAceptacion = nfa1.aceptacion
            self.listaProcesamientosRechazados = nfa1.rechazadas
            return print(procesamientos)

        elif opcion == "0":
            sys.exit()


