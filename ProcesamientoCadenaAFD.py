import sys
from Graph import graficarAutomata
class ProcesamientoCadenaAFD:
    cadena=None
    esAceptada=None
    listaEstadoSimboloDeProcesamiento=None
    afd = None
    def __init__(self, afd):
        self.afd = afd
        self.cadena = input("--------------------------------------------"+
                            "Ingrese una cadena:")

    def elegirMetodo(self):
        opcion = input(
            "--------------------------------------- \n"
            "Elija el metodo de procesamiento: \n"
            "1. Procesamiento \n"
            "2. Procesamiento con detalles \n"
            "3. Hallar complemento \n"
            "4. Simplificar AFD \n"
            "G. Graficar automata \n"
            "0. Salir \n"
            "--------------------------------------- \n"
        )
        if opcion == "1":
            esAceptada = self.afd.procesarCadena(self.cadena)
            return print(esAceptada)

        elif opcion == "2":
            esAceptada = self.afd.procesarCadenaConDetalles(self.cadena)
            return print(esAceptada)

        elif opcion == "3":
            pass

        elif opcion == "4":
            pass

        elif opcion == "G":
            grafo = graficarAutomata()
            grafo.mostrarGrafo(self.afd)

        elif opcion == "0":
            sys.exit()