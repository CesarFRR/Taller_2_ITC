import sys
from Alfabeto import Alfabeto
from AFD import AFD
from AFN import AFN
from AFN_e import AFN_Lambda
from AFPD import AFPD
from AFPN import AFPN
from AF2P import AF2P
from MT import MT
from ProcesamientoCadenaAFD import ProcesamientoCadenaAFD
from ProcesamientoCadenaAFN import ProcesamientoCadenaAFN
import os
from Graph import graficarAutomata



class ClasePrueba:
    afn = None
    afd = None
    afd2 = None
    afn_lambda = None
    afpd=None
    afpn= None
    af2p= None
    mt= None
    afn_conversion = None
    listaAutomatas=None
    listaNombreArchivos=None
    def __init__(self, *args):
        #self.interfaz = args[0]
        pass
    
    def main(self, metodo = None, args = None, afpn = False):
        tipoAutomata = metodo[0]
        metodoAutomata = metodo[1]
        if tipoAutomata == 'AFD':
            if afpn:
                self.probarAFD(metodoAutomata, args, True)
            else:
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

        elif tipoAutomata == 'AFPD':
            self.probarAFPD(metodoAutomata, args)

        elif tipoAutomata == 'AFPN':
            self.probarAFPN(metodoAutomata, args)

        elif tipoAutomata == 'AF2P':
            self.probarAF2P(metodoAutomata, args)
        elif tipoAutomata == 'MT':
            self.probarMT(metodoAutomata, args)
        

    def importarArchivosEntrada(self):
        carpeta= './archivosEntrada'
        nombres_archivos = []
        automatas=[]
        for nombre_archivo in os.listdir(carpeta):
            ruta_archivo = os.path.join(carpeta, nombre_archivo)
            if os.path.isfile(ruta_archivo):
                nombre_archivo_sin_ruta = os.path.basename(ruta_archivo)
                nombres_archivos.append(nombre_archivo_sin_ruta)
        for url in nombres_archivos:
            url=str(url)
            if(url.endswith('dfa')):
                automatas.append(AFD(url))
            elif(url.endswith('nfa')):
                automatas.append(AFN(url))
            elif(url.endswith('nfe')):
                automatas.append(AFN_Lambda(url))
            elif(url.endswith('dpda')):
                automatas.append(AFPD(url))
            elif(url.endswith('pda')):
                automatas.append(AFPN(url))
            elif(url.endswith('msm')):
                automatas.append(AF2P(url))
            elif(url.endswith('tm')):
                automatas.append(MT(url))
        self.listaNombreArchivos= nombres_archivos
        self.listaAutomatas= automatas
        return automatas
    
    def probarAFD(self, metodo = None, args = None, afpn = False):
        if metodo == None:
            if self.afd is not None:
                if len(args) == 1:
                    self.afd2 = AFD(args[0])
                else:
                    self.afd2 = AFD(args[0], args[1], args[2], args[3], args[4])
                if afpn == False:
                    self.probarProductoCartesiano()
            elif len(args) == 1:
                self.afd = AFD(args[0])
            else:
                self.afd = AFD(args[0], args[1], args[2], args[3], args[4])
            if afpn:
                self.probarAFPNcartesiano(self.afd)
            
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
            print(self.afd.imprimirAFDSimplificado())
        elif metodo == 'Graficar':
            print(self.afd.toString(True))
    
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
        elif metodo == 'Computar todos los procesamientos':
            aceptada = self.afn.computarTodosLosProcesamientos(args, 'AFNprocesamientos')
        elif metodo == 'Procesar lista de cadenas':
            print(args[0])
            self.afn.procesarListaCadenas(args[0], args[1], True)
        elif metodo == 'Exportar':
            self.afn.exportar(args)
        elif metodo== 'Imprimir':
            print(self.afn.imprimirAFNSimplificado())
        elif metodo== 'Graficar':
            print(self.afn.toString(True))

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
        elif metodo == 'Computar todos los procesamientos':
            aceptada = self.afn_lambda.computarTodosLosProcesamientos(args, 'AFN_eProcesamientos')
        elif metodo == 'Lamda clausura':
            estados = args
            self.afn_lambda.lambda_clausura(estados, True)
        elif metodo == 'Exportar':
            archivo = args
            self.afn_lambda.exportar(archivo)
        elif metodo == 'Imprimir':
            print(self.afn_lambda.imprimirAFNLSimplificado())
        elif metodo == 'Graficar':
            print(self.afn_lambda.toString(True))
    
    def probarAFPD(self,metodo = None,  args = None):
        if metodo == None:
            if len(args) == 1:
                self.afpd = AFPD(args[0])
            else:
                self.afpd = AFPD(args[0], args[1], args[2], args[3], args[4]) 
        if metodo == 'Procesar cadena':
            cadena = args
            aceptada = self.afpd.procesarCadena(cadena)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            cadena = args
            aceptada = self.afpd.procesarCadenaConDetalles(cadena)
            return print(aceptada)
        elif metodo == 'Procesar lista de cadenas':
            lista = args[0]
            archivo = args[1]
            self.afpd.procesarListaCadenas(lista, archivo, True)
        elif metodo == 'Exportar':
            archivo = args
            self.afpd.exportar(archivo)
        elif metodo == 'Imprimir':
            print(self.afpd.toString())
        elif metodo == 'Graficar':
            print(self.afpd.toString(True))
    
    def probarAFPN(self,metodo = None,  args = None):
        if metodo == None:
            if len(args) == 1:
                self.afpn = AFPN(args[0])
            else:
                self.afpn = AFPN(args[0], args[1], args[2], args[3], args[4]) 
        if metodo == 'Procesar cadena':
            cadena = args
            aceptada = self.afpn.procesarCadena(cadena)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            cadena = args
            aceptada = self.afpn.procesarCadenaConDetalles(cadena)
            return print(aceptada)
        elif metodo == 'Computar todos los procesamientos':
            aceptada = self.afpn.computarTodosLosProcesamientos(args, 'AFNprocesamientos')
        elif metodo == 'Procesar lista de cadenas':
            lista = args[0]
            archivo = args[1]
            self.afpn.procesarListaCadenas(lista, archivo, True)
        elif metodo == 'Exportar':
            archivo = args
            self.afpn.exportar(archivo)
        elif metodo == 'Imprimir':
            print(self.afpn.toString())
        elif metodo == 'Graficar':
            print(self.afpn.toString(True))

    def probarAF2P(self,metodo = None,  args = None):
        if metodo == None:
            if len(args) == 1:
                self.af2p = AF2P(args[0])
            else:
                self.af2p = AF2P(args[0], args[1], args[2], args[3], args[4]) 
        if metodo == 'Procesar cadena':
            cadena = args
            aceptada = self.af2p.procesarCadena(cadena)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            cadena = args
            aceptada = self.af2p.procesarCadenaConDetalles(cadena)
            return print(aceptada)
        elif metodo == 'Procesar lista de cadenas':
            lista = args[0]
            archivo = args[1]
            self.af2p.procesarListaCadenas(lista, archivo, True)
        elif metodo == 'Exportar':
            archivo = args
            self.af2p.exportar(archivo)
        elif metodo == 'Imprimir':
            print(self.af2p.toString())
        elif metodo == 'Graficar':
            print(self.af2p.toString(True))
    
    def probarMT(self,metodo = None,  args = None):
        if metodo == None:
            if len(args) == 1:
                self.mt = MT(args[0])
            else:
                self.mt = MT(args[0], args[1], args[2], args[3], args[4]) 
        if metodo == 'Procesar cadena':
            cadena = args
            aceptada = self.mt.procesarCadena(cadena)
            return print(aceptada)
        elif metodo == 'Procesar cadena con detalles':
            cadena = args
            aceptada = self.mt.procesarCadenaConDetalles(cadena)
            return print(aceptada)
        elif metodo == 'Procesar lista de cadenas':
            lista = args[0]
            archivo = args[1]
            self.mt.procesarListaCadenas(lista, archivo, True)
        elif metodo == 'Exportar':
            archivo = args
            self.mt.exportar(archivo)
        elif metodo == 'Imprimir':
            print(self.mt.toString())
        elif metodo == 'Graficar':
            print(self.mt.toString(True))

    def probarAFNtoAFD(self, args = None):
        self.afn_conversion = self.afn.AFNtoAFD(self.afn)
        graph = graficarAutomata()
        graph.exportarGrafo(self.afn_conversion)
        cadena = args[0]
        lista = args[1]
        archivo = args[2]
        if len(lista[0]) == 0:
            print('AFN \n', self.afn.toString(), '\n')
            print('procesamiento AFN \n',self.afn_conversion.procesarCadenaConDetalles(cadena), '\n')
            print('AFN convertido \n', self.afn_conversion.toString(), '\n')
            print('procesamiento AFN convertido a AFD \n',self.afn.procesarCadena(cadena))
        else:
            print('AFN \n', self.afn.toString(), '\n')
            'procesamiento AFN \n',self.afn_conversion.procesarListaCadenas(lista, archivo, True), '\n'
            print('AFN convertido \n', self.afn_conversion.toString(), '\n')
            'procesamiento AFN convertido a AFD \n',self.afn.procesarListaCadenas(lista, archivo, True)
        pass

    def probarAFNLambdaToAFD(self, args = None):
        cadena = args
        graph = graficarAutomata()
        
        self.afn_lambda_conversion_AFN = self.afn_lambda.AFN_LambdaToAFN(self.afn_lambda)
        print('Convertido a AFN \n',self.afn_lambda_conversion_AFN.toString(), '\n')
        
        self.afn_lambda_conversion_AFD = self.afn_lambda.AFN_LambdaToAFD(self.afn_lambda)
        print('Convertido a AFD \n',self.afn_lambda_conversion_AFD.toString(), '\n')

        print('Procesamiento AFN_ lambda \n', self.afn_lambda.procesarCadenaConDetalles(cadena), '\n')
        print('procesamiento AFN \n',self.afn_lambda_conversion_AFN.procesarCadenaConDetalles(cadena), '\n')
        print('procesamiento AFD \n',self.afn_lambda_conversion_AFD.procesarCadenaConDetalles(cadena))
        graph.exportarGrafos([self.afn_lambda_conversion_AFN, self.afn_lambda_conversion_AFD], 'lambdaConversion')

    def probarComplemento(self):
        print(self.afd.toString(False))
        comp = self.afd.AFD_hallarComplemento(self.afd)
        print(comp.toString())

    def probarProductoCartesiano(self):
        graph = graficarAutomata()
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
        graph.exportarGrafos([y, o, dif, sim], 'productoCartesianoAFD')

    def probarSimplificacion(self):
        self.afd = self.afd.imprimirAFDSimplificado(True)
    
    def probarAFPNcartesiano(self, afd):
        self.afpn_cartesiano = self.afpn.hallarProductoCartesianoConAFD(afd)
        print(self.afpn_cartesiano.toString(True))
