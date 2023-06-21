from AFPN import AFPN
from AFD import AFD
import sys

class PruebaAFPN():
    afpn = None

    def __init__(self):
        archivo = input('Ingrese el nombre del archivo \n')
        self.afpn = AFPN(archivo)
    
    def main(self):
        print('---------------------------------------------------- \n')
        opcion = input('Seleccione una opcion: \n'
                       '1. Imprimir automata \n'
                       '2. Exportar a archivo \n'
                       '3. Procesar en detalle \n'
                       '4. Computar todos los procesamientos \n'
                       '5. Procesar lista de cadenas \n'
                       '6. Hallar producto cartesiano con AFD \n'
                       's. Salir \n')
        print('---------------------------------------------------- \n')
        if opcion == '1':
            print(self.afpn.toString())
        elif opcion == '2':
            archivo = input('Ingrese el nombre del archivo\n')
            self.afpn.exportar(archivo)
        elif opcion == '3':
            cadena = input('Ingrese la cadena \n')
            print(self.afpn.procesarCadenaConDetalles(cadena))
        
        elif opcion == '4':
            cadena = input('Ingrese la cadena \n')
            archivo = input('ingrese nombre archivo \n')
            self.afpn.computarTodosLosProcesamientos(cadena, archivo)
        
        elif opcion == '5':
            lista = input('Ingrese lista de cadenas (separadas por coma) \n').split(',')
            archivo = input('Ingrese nombre del archivo \n')
            self.afpn.procesarListaCadenas(lista, archivo, True)
        
        elif opcion == '6':
            archivoAFD = input('Ingrese nombre del archivo AFD: \n')
            afd = AFD(archivoAFD)
            cartesiano = self.afpn.hallarProductoCartesianoConAFD(afd)
            print(cartesiano.toString())
        
        elif opcion == 's':
            sys.exit()

prueba = PruebaAFPN()

while True:
    prueba.main()