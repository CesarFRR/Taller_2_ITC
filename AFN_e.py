from Alfabeto import Alfabeto
import re
class AFN_Lambda:
    Sigma=None
    Q=None
    q0=None
    F=None
    delta = {}
    estadosLimbo = None
    estadosInaccesibles = None
    automata_tipo = "nfe"
    etiquetas=['#!nfe', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
    def __init__(self, *args):
        if (len(args) == 1):  # Inicializar por archivo txt
            if (not args[0].endswith("." + self.automata_tipo)):
                raise ValueError(
                    "El archivo proporcioando no es de formato ", self.automata_tipo)
            try:
                afc = {}
                key = ''
                with open(args[0], 'r', newline='', encoding='utf-8') as file:
                    file = file.read().replace('\r\n', '\n').replace('\r', '\n')  # problema de saltos de linea solucionados
                    string= f'''{file}'''
                    dictReader={}
                    afc={}
                    for i in string.split('\n'):
                        if i in self.etiquetas[1:]:
                            key = i
                        elif i != '':
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions':  # transiciones, si pueden contener $ (lambda), esto es AFN-lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3): raise ValueError("transición inválida: ", i)
                                estado, simbolo, deltaResultado = trans
                                valor=dictReader.get(estado)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={simbolo: set(deltaResultado.split(';')) }
                                else:  #AFN-lambda: Pueden haber varias transiciones de q para un simbolo
                                    dictReader[estado].update({simbolo:set(deltaResultado.split(';'))})
                    self.Sigma = Alfabeto(afc['#alphabet'])
                    self.Q = set(afc['#states'])
                    self.q0 = afc['#initial'][0]
                    self.F = set(afc['#accepting'])
                    self.delta = dictReader       
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma, self.Q, self.qo, self.F, self.delta = args
            self.Q=set(self.Q)
            self.F=set(self.F)
            
    def hallarEstadosInaccesibles(self):
        pass
    def toString(self):
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for Q in self.delta:
            for simb in self.delta[Q]:
                deltaSet= sorted((list(self.delta[Q][simb])))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{Q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        return out
    def imprimirAFNLSimplificado(self):
        pass

    def exportar(self, archivo):
        with open(archivo, "w") as f:
                f.write(self.toString())

    def AFN_LambdaToAFN(self, afnl):
        pass
    def AFN_LambdaToAFD(self, afnl):
        pass
    def procesarCadena(self, cadena):
        return True
    def procesarCadenaConDetalles(self, cadena):
        pass
    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        pass
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla):
        pass
    def procesarCadenaConversion(self, cadena):
        pass
    def procesarCadenaConDetallesConversion(self, cadena):
        pass
    def procesarListaCadenasConversion(self, listaCadenas,nombreArchivo, imprimirPantalla): 
        pass

    def pruebas(self, cadena):
        out=''
        print("usando delta: \n")
        limbo = { 'L':{  s: set('L') for s in self.Sigma.simbolos} }
        print('limbo: ', limbo)
        for estado in self.delta:
            for simb in self.Sigma.simbolos:
                if(self.delta[estado].get(simb)==None):
                    self.delta[estado][simb]=limbo
        
        out = self.toString() #.get() retorna el conjunto del simbolo dado, si no existe retorna un conjunto vacío (esto es para evitar errores de KeyError: clave no encontrada)
        return out

    #================================================

print('Ejecutando:...\n')
nfe1= AFN_Lambda("ej1.nfe")

print('Ejecutando:...\n')
print(nfe1.delta)
# print(nfe1.toString())
# print('\n')
# nfe1.exportar('ej2.nfe')
print(nfe1.pruebas(' '))