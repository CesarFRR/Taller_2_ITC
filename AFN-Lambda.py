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
                    if(not string.startswith(self.etiquetas[0])):
                        print("si empieza con: ", self.etiquetas[0])
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
                                estado=trans[0]
                                simbolo=trans[1]
                                deltaResultado=trans[2]
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={simbolo: set(deltaResultado.split(',')) }
                                elif(simbolo in valor):
                                    pass #Transición válida --> AFN: si pueden haber varias transiciones de q para un simbolo o etiqueta
                                else:
                                    dictReader[estado].update({simbolo:set(deltaResultado.split(','))})
                    self.Sigma = Alfabeto([afc['#alphabet'][0]])
                    self.Q = afc['#states']
                    self.q0 = afc['#initial'][0]
                    self.F = afc['#accepting']
                    self.delta = dictReader       
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma = args[0]
            self.Q = args[1]
            self.q0 = args[2]
            self.F = args[3]
            self.delta = args[4]
    def verificarCorregirCompletitudAFD():
        pass
    def hallarEstadosInaccesibles():
        pass
    def toString(self):
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(self.Q)+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(self.F)+ '\n'+ self.etiquetas[5]+'\n'
        for estado in self.delta:
            keys_simbolos=list(self.delta[estado].keys())
            simbolos=self.delta.get(estado)
            for k in keys_simbolos:
                set=simbolos[k]
                set = set.pop() if len(set)==1 else ','.join(set)
                #print(estado+':'+k+'>'+set)
                out=out+estado+':'+k+'>'+set+'\n'
        return out
    def imprimirAFNLSimplificado():
        pass
    def exportar(archivo):
        pass
    def AFN_LambdaToAFN(afnl):
        pass
    def AFN_LambdaToAFD(afnl):
        pass
    def procesarCadena(cadena):
        return True
    def procesarCadenaConDetalles(cadena):
        pass
    def computarTodosLosProcesamientos(cadena, nombreArchivo):
        pass
    def procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla):
        pass
    def procesarCadenaConversion(cadena):
        pass
    def procesarCadenaConDetallesConversion(cadena):
        pass
    def procesarListaCadenasConversion(listaCadenas,nombreArchivo, imprimirPantalla): 
        pass

    #================================================

print('Ejecutando:...\n')
nfe1= AFN_Lambda("ej1.nfe")
print(nfe1.toString())
