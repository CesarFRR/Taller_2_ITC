import sys
from Alfabeto import Alfabeto
from AFD import AFD
from AFN import AFN
from AFN_e import AFN_Lambda
from ProcesamientoCadenaAFD import ProcesamientoCadenaAFD
from ProcesamientoCadenaAFN import ProcesamientoCadenaAFN


class ClasePrueba:
    afn = None
    afd = None
    afn_lambda = None

    def __init__(self, *args):
        #self.interfaz = args[0]
        pass
    
    def main(self, metodo = None, args = None):
        tipoAutomata = metodo[0]
        metodoAutomata = metodo[1]
        if tipoAutomata == 'AFD':
            self.probarAFD(metodoAutomata, args)
        elif tipoAutomata == 'AFN':
            self.probarAFN(metodoAutomata, args)
        elif tipoAutomata == 'AFNLambda':
            self.probarAFNLambda(metodoAutomata, args)

    def probarAFD(self, metodo = None, args = None):
        if metodo == None:
            if len(args) == 1:
                self.afd = AFD(args[0])
            else:
                self.afd = AFD(args[0], args[1], args[2], args[3], args[4])
        if metodo == 'Procesar cadena':
            aceptada = self.afd.procesarCadena(args)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            aceptada = self.afd.procesarCadenaConDetalles(args)
            return print(aceptada)
        elif metodo == 'Procesar lista de cadenas':
            print(args[0])
            self.afd.procesarListaCadenas(args[0], args[1], True)
        elif metodo == 'Exportar':
            self.afd.exportar(args)
        elif metodo == 'Imprimir':
            self.afd.toString(False)
        elif metodo == 'Graficar':
            self.afd.toString(True)
    
    def probarAFN(self, metodo = None, args = None):
        if metodo == None:
            self.afn = AFN(args[0], args[1], args[2], args[3], args[4])
        if metodo == 'Procesar cadena':
            aceptada = self.afn.procesarCadena(args)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            aceptada = self.afn.procesarCadenaConDetalles(args)
            return print(aceptada)
        elif metodo == 'Procesar lista de cadenas':
            print(args[0])
            self.afn.procesarListaCadenas(args[0], args[1], True)
        elif metodo == 'Exportar':
            self.afn.exportar(args)
        elif metodo== 'Imprimir':
            self.afn.toString(False)
        elif metodo== 'Graficar':
            self.afn.toString(True)

    def probarAFNLambda(self,  metodo = None, args = None):
        if metodo == None:
            self.afn_lambda = AFN_Lambda(args[0], args[1], args[2], args[3], args[4])
        if metodo == 'Procesar cadena':
            aceptada = self.afn_lambda.procesarCadena(args)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            aceptada = self.afn_lambda.procesarCadenaConDetalles(args)
            return print(aceptada)
        elif metodo == 'Procesar lista de cadenas':
            print(args[0])
            self.afn_lambda.procesarListaCadenas(args[0], args[1], True)
        elif metodo == 'Exportar':
            self.afn_lambda.exportar(args)
        elif metodo == 'Imprimir':
            self.afn_lambda.toString(False)
        elif metodo == 'Graficar':
            self.afn_lambda.toString(True)

    def probarAFNtoAFD(self):
        pass

    def probarAFNLambdaToAFD(self):
        pass

    def probarComplemento(self):
        pass

    def probarProductoCartesiano(self):
        pass
    
    def probarSimplificacion(self):
        pass
