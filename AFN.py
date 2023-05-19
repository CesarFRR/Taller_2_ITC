from Alfabeto import Alfabeto
import re
import AFD, AFN_Lambda
class AFN:
    Sigma = None
    Q = None
    q0 = None
    F = None
    delta = {}
    estadosLimbo = None
    estadosInaccesibles = None
    automata_tipo = "nfa"
    etiquetas=['#!nfa', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
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
                            elif key== '#transitions' and i.split(":")[1].split(">")[0]!= "$": # AFN: no contiene transiciones lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3): raise ValueError("transición inválida: ", i)
                                estado, simbolo, deltaResultado = trans
                                valor=dictReader.get(estado)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={simbolo: set(deltaResultado.split(';')) }
                                else: #AFN: Pueden haber varias transiciones de q para un simbolo
                                    dictReader[estado].update({simbolo:set(deltaResultado.split(';'))})
                    self.Sigma = Alfabeto([afc['#alphabet'][0]])
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
        accesibles=set()
        for q in self.delta:
            for simb in self.delta[q]:
                accesibles.add(self.delta[q][simb])
        inaccesibles=self.Q.difference(accesibles)  #inaccesibles = Q - accesibles


    pass

    def toString(self):
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= sorted(list(self.delta[q][simb]))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        return out
    def imprimirAFNSimplificado(self):
        pass

    def exportar(self, archivo):
        with open(archivo, "w") as f:
                f.write(self.toString())

    def AFNtoAFD(self, afn: "AFN"):
        afd = AFD('')
        pass

    def procesarCadena(self, cadena):
        return True

    def procesarCadenaConDetalles(self, cadena):
        return True

    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        return 0
    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        pass

    def procesarCadenaConversion(self, cadena):
        return True
    
    def  procesarCadenaConDetallesConversion(self, cadena):
        return True
    
    def procesarListaCadenasConversion(self, listaCadenas,nombreArchivo, imprimirPantalla):
        pass

#================================================

print('Ejecutando:...\n')
nfa1= AFN("ej1.nfa")
print(nfa1.toString())
print('\n')
nfa1.exportar('ej2.nfa')