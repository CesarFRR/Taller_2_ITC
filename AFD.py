from Alfabeto import Alfabeto
import re


class AFD:
    Sigma = None  
    Q = None
    q0 = None
    F = None
    delta = {} # se intentará hacer el delta como  un diccionario, cada estado q contiene otro diccionario --> clave:simbolo, valor: conjunto de estados resultantes tras evaluar con la funcion delta
    estadosLimbo = None
    estadosInaccesibles = None
    automata_tipo = "dfa"
    etiquetas=['#!dfa', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
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
                            elif key== '#transitions' and i.split(":")[1].split(">")[0]!= "$": # transiciones, verificar que cada una no contenga $ (lambda)
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
                                    raise ValueError("transición inválida --> AFD: no pueden haber dos transiciones de ", trans[0], " para la misma etiqueta ", trans[2], " --> ", i)
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
    def verificarCorregirCompletitudAFD(self):
        pass

    def hallarEstadosLimbo(self):
        pass

    def hallarEstadosInaccesibles(self):
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

    def imprimirAFDSimplificado(self):
        pass

    def exportar(self, archivo):
        pass

    def procesarCadena(self, cadena):   #Procesar cadena con delta como un diccionario
            actual = self.q0
            for i in cadena:
                if i not in self.Sigma:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                    return False
                if self.delta.get(actual) is not None:  #Verificar que el estado actual exista
                    transicion = self.delta[actual]    #Lista de transiciones del estado actual
                    for j in transicion:    
                        if i in j: #Recorrer las transiciones verificando el simbolo actual y el estado resultado
                            actual = j[1] #Realizar transicion                    
                            break
                            
            if actual in self.F: #verificar si el estado actual es de aceptacion
                return True
            else:
                return False   

    def procesarCadenaConDetalles(self, cadena):
        return True

    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        pass

    def AFD_hallarComplemento(self, afdInput: "AFD"):
        pass

    def AFD_hallarProductoCartesianoY(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesianoO(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesianoDiferencia(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesianoDiferenciaSimétrica(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesiano(self, afd1: "AFD", afd2: "AFD", StringOperacion):
        pass

    def AFD_simplificarAFD(self, afdinput: "AFD"):
        pass

#================================================

print('Ejecutando:...')
afd1= AFD("ej1.dfa")
print(afd1.toString())
