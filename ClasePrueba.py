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
    afd2 = None
    afn_lambda = None
    afn_conversion = None

    def __init__(self, *args):
        #self.interfaz = args[0]
        pass
    
    def main(self, metodo = None, args = None):
        tipoAutomata = metodo[0]
        metodoAutomata = metodo[1]
        if tipoAutomata == 'AFD':
            self.probarAFD(metodoAutomata, args)
        elif tipoAutomata == 'AFN':
            if metodoAutomata == 'AFNtoAFD':
                self.probarAFNtoAFD(args)
            else:
                self.probarAFN(metodoAutomata, args)
        elif tipoAutomata == 'AFNLambda':
            if metodoAutomata == 'AFNLambdaToAFD':
                self.probarAFNLambdaToAFD(args)
            else:
                self.probarAFNLambda(metodoAutomata, args)

    def probarAFD(self, metodo = None, args = None):
        if metodo == None:
            if self.afd is not None:
                if len(args) == 1:
                    self.afd2 = AFD(args[0])
                else:
                    self.afd2 = AFD(args[0], args[1], args[2], args[3], args[4])
                self.probarProductoCartesiano()
            elif len(args) == 1:
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
            print(self.afd.toString(False))
        elif metodo == 'Graficar':
            self.afd.toString(True)
    
    def probarAFN(self, metodo = None, args = None):
        if metodo == None:
            if len(args) == 1:
                self.afn = AFN(args[0])
            else:
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
            print(self.afn.toString(False))
        elif metodo== 'Graficar':
            self.afn.toString(True)

    def probarAFNLambda(self,  metodo = None, args = None):
        if metodo == None:
            if len(args) == 1:
                self.afn_lambda = AFN_Lambda(args[0])
            else:
                self.afn_lambda = AFN_Lambda(args[0], args[1], args[2], args[3], args[4])
        if metodo == 'Procesar cadena':
            cadena = args
            aceptada = self.afn_lambda.procesarCadena(cadena)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            cadena = args
            aceptada = self.afn_lambda.procesarCadenaConDetalles(cadena)
            return print(aceptada)
        elif metodo == 'Procesar lista de cadenas':
            lista = args[0]
            archivo = args[1]
            self.afn_lambda.procesarListaCadenas(lista, archivo, True)
        elif metodo == 'Exportar':
            archivo = args
            self.afn_lambda.exportar(archivo)
        elif metodo == 'Imprimir':
            print(self.afn_lambda.toString(False))
        elif metodo == 'Graficar':
            self.afn_lambda.toString(True)

    def probarAFNtoAFD(self, args = None):
        self.afn_conversion = self.afn.AFNtoAFD(self.afn)
        cadena = args
        print('AFN \n', self.afn.toString(), '\n')
        print('procesamiento AFN \n',self.afn_conversion.procesarCadenaConDetalles(cadena), '\n')
        print('AFN convertido \n', self.afn_conversion.toString(), '\n')
        print('procesamiento AFN convertido a AFD \n',self.afn.procesarCadena(cadena))
        pass

    def probarAFNLambdaToAFD(self, args = None):
        cadena = args
        
        self.afn_lambda_conversion_AFN = self.afn_lambda.AFN_LambdaToAFN(self.afn_lambda)
        print('Convertido a AFN \n',self.afn_lambda_conversion_AFN.toString(), '\n')
        
        self.afn_lambda_conversion_AFD = self.afn_lambda.AFN_LambdaToAFD(self.afn_lambda)
        print('Convertido a AFD \n',self.afn_lambda_conversion_AFD.toString(), '\n')

        print('Procesamiento AFN_ lambda \n', self.afn_lambda.procesarCadenaConDetalles(cadena), '\n')
        print('procesamiento AFN \n',self.afn_lambda_conversion_AFN.procesarCadenaConDetalles(cadena), '\n')
        print('procesamiento AFD \n',self.afn_lambda_conversion_AFD.procesarCadenaConDetalles(cadena))

    def probarComplemento(self):
        print(self.afd.toString(False))
        comp = self.afd.AFD_hallarComplemento(self.afd)
        print(comp.toString())

    def probarProductoCartesiano(self):
        print('---------------------------------------------------------------- \n ∩ \n')
        y = self.afd.AFD_hallarProductoCartesianoY(self.afd, self.afd2)
        print(y.toString())
        print('---------------------------------------------------------------- \n ∪ \n')
        o = self.afd.AFD_hallarProductoCartesianoO(self.afd, self.afd2)
        print(o.toString())
        print('---------------------------------------------------------------- \n − \n')
        dif = self.afd.AFD_hallarProductoCartesianoDiferencia(self.afd, self.afd2)
        print(dif.toString())
        print('---------------------------------------------------------------- \n △ \n')
        sim = self.afd.AFD_hallarProductoCartesianoDiferenciaSimetrica(self.afd, self.afd2)
        print(sim.toString())
    
    def probarSimplificacion(self):
        print(self.afd.AFD_simplificarAFD(self.afd))
