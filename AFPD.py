from AFD import AFD
import copy
import re
from Alfabeto import Alfabeto
class AFPD:
    """
    # Clase AFPD

    Ésta clase modela y simula el Autómata Finito con Pila determinista AFPD el cual puede poseer cero o una transición para un símbolo perteneciente al Alfabeto, además de que la Pila posee su propio alfabeto

    """
    Q = None
    q0 =None
    F =None
    Sigma =None
    PSigma = None
    delta = None
    
    nombreArchivo='archivodpda'
    extension = "dpda"
    etiquetas=['#!dpda', '#states', '#initial', '#accepting','#tapeAlphabet', '#stackAlphabet',  '#transitions']
    instanciaVacia=False
    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], str)):  # Inicializar por archivo txt
            if (not args[0].endswith("." + self.extension)):raise ValueError("El archivo proporcioando no es de formato ", self.extension)
            try:
                afc = {}
                key = ''
                with open(f'./archivosEntrada/{args[0]}', 'r', newline='', encoding='utf-8') as file:
                    file = file.read().replace('\r\n', '\n').replace('\r', '\n')  # problema de saltos de linea solucionados
                    string= f'''{file}'''
                    dictReader={}
                    afc={}
                    for i in string.strip().split('\n'):
                        if i in self.etiquetas[1:]:
                            key = i
                        elif i != '' or not i.isspace():
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions': # AFPD: no contiene transiciones lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=5 or ';' in trans): raise ValueError("transicion invalida: ", i) # "; " q no puede tener varias salidas con un simbolo
                                estado, simbolo, pop, estadoDestino, push = trans
                                #print('trans: ', trans)
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={ simbolo:[[pop, push, estadoDestino]] }
                                else:
                                    if(dictReader[estado].get(simbolo)==None):
                                        dictReader[estado][simbolo]=[[pop, push, estadoDestino]]
                                    else:
                                        dictReader[estado][simbolo].append([pop, push, estadoDestino])
                            
                    self.Sigma = Alfabeto(afc['#tapeAlphabet'])
                    self.PSigma= Alfabeto(afc['#stackAlphabet'])
                    self.Q = set(afc['#states'])
                    self.q0 = afc['#initial'][0]
                    self.F = set(afc['#accepting'])
                    self.delta = dictReader
                    #print('delta: ', self.delta)
                    self.nombreArchivo=((args[0]).split('.'+self.extension))[0]
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 6):  # Inicializar por los 6 parametros: alfabeto,alfabetoPila estados, estadoInicial, estadosAceptacion, delta
            self.Q, self.q0, self.F,self.Sigma, self.PSigma, self.delta = args
            self.Q=set(self.Q)
        elif(len(args) == 1 and isinstance(args[0], AFPD)):
            self.Q=copy.deepcopy(args[0].Q)
            self.q0=args[0].q0
            self.F=copy.deepcopy(args[0].F)
            self.Sigma=copy.deepcopy(args[0].Sigma)
            self.PSigma=copy.deepcopy(args[0].PSigma)
            self.delta=copy.deepcopy(args[0].delta)
        elif(len(args) == 0):
            self.Q = set()
            self.q0 =''
            self.F =set()
            self.Sigma =Alfabeto('')
            self.PSigma = Alfabeto('')
            self.delta = {}

        #self.PSigma.simbolos.append('$')



    def modificarPila(self, pila: list, operacion: str, parametro: str):
        """Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase."""
        parametro=list(parametro)
        if operacion == 'push':
            for simb in parametro:
                if(simb!= '$'):
                    pila.append(simb)
        elif operacion == 'pop':
            for simb in parametro:
                if(simb!= '$'):
                    if(len(pila)==0):
                        return False
                    pila.pop()
        elif operacion == 'swap':
            for simb in parametro:
                pila.pop()
                pila.append(simb)
                    
        return True
    def procesarCadena(self, cadena: str)->bool:   #Procesar cadena con delta como un diccionario
        """ procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata. 
        
            Nota: esta función está diseñada para soportar errores de entrada o lógica, tambien soporta pop y push de varios simbolos en una operación
            Ej: a, AA | BB---> b, BA | AA
        """
        pila =list()
        actual = self.q0
        estados=self.delta.keys()
        aceptada=None
        for simbolo in cadena:
            if simbolo not in self.Sigma.simbolos:  
                aceptada= False # El simbolo no se encuentre en el alfabeto entrada {Sigma}, procesamiento abortado
                break
            if(actual in estados):  # procesar la cadena
                if(self.delta.get(actual)==None):
                    break # estado {actual} sin transiciones, posible estado limbo o estado final
                elif(self.delta[actual].get(simbolo)==None):
                    aceptada = False # transicion con simbolo actual no disponible, por lo tanto se aborta el procesamiento
                    break
                if len(self.delta[actual][simbolo])>1: raise ValueError('No puede haber mas de una transición para un simbolo, no corresponde al comportamiento de un AFPD')
                transicion= self.delta[actual][simbolo][0]
                pop, push, actual = transicion
                if not all(simb in self.PSigma.simbolos for simb in pop) or not all(simb in self.PSigma.simbolos for simb in push):
                    aceptada = False # simbolo no se encuentre en el alfabeto de la pila {PSigma}
                if('$' != pop and '$' !=push):
                    self.modificarPila(pila, 'swap',push)
                else:
                    if(self.modificarPila(pila, 'pop', pop)==False):
                        aceptada = False #Pila vacía al momento de hacer pop(), procesamiento abortado
                    self.modificarPila(pila, 'push', push)

        if('$' in self.delta[actual].keys()): # Si existe una transición cuando la cadena ya se ha consumido toda, ej $,$|$
            pop, push, actual = self.delta[actual]['$'][0]
            if not all(simb in self.PSigma.simbolos for simb in pop) or not all(simb in self.PSigma.simbolos for simb in push):
                aceptada = False # simbolo no se encuentre en el alfabeto de la pila {PSigma}
            if('$' != pop and '$' !=push):
                self.modificarPila(pila, 'swap',push)
            else:
                if(self.modificarPila(pila, 'pop', pop)==False):
                    aceptada = False #Pila vacía al momento de hacer pop(), procesamiento abortado
                self.modificarPila(pila, 'push', push)
        
        if actual in self.F and len(pila)==0: #verificar si el estado actual es de aceptacion
            if(aceptada==None):
                aceptada=True
        else:
            aceptada= False
        return aceptada
        
    def procesarCadenaConDetalles(self, cadena):
        """realiza  lo  mismo  que  el  método  anterior aparte  imprime  losdetalles  del  procesamiento  con  el  formato  que se  indica  en  el  archivo AFPD.pdf."""
        #(q0,aabb,$)->(q0,abb,A)->(q0,bb,AA)->(q1,b,A)->(q1,$,$)>>accepted
        #(q0,aabbb,$)->(q0,abbb,A)->(q0,bbb,AA)->(q1,bb,A)->(q1,b,$)>>rejected
        pila =list()
        actual = self.q0
        estados=self.delta.keys()
        aceptada=None
        out=''
        for index, simbolo in enumerate(cadena):
            if  simbolo not in self.Sigma.simbolos:  
                out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted'
                print(out)
                return False # El simbolo no se encuentre en el alfabeto entrada {Sigma}, procesamiento abortado
            if(actual in estados):  # procesar la cadena
                if(self.delta.get(actual)==None):
                    out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })->'
                    break # estado {actual} sin transiciones, posible estado limbo o estado final
                elif(self.delta[actual].get(simbolo)==None):
                    aceptada = False # transicion con simbolo actual no disponible, por lo tanto se aborta el procesamiento
                    out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted'
                    print(out)
                    return False
                if len(self.delta[actual][simbolo])>1:
                    raise ValueError('No puede haber mas de una transición para un simbolo, no corresponde al comportamiento de un AFPD')
                transicion= self.delta[actual][simbolo][0]
                pop, push, actual = transicion
                if not all(simb in self.PSigma.simbolos for simb in pop) or not all(simb in self.PSigma.simbolos for simb in push):
                    out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted, ({pop} ∉ #stackAlphabet) V ({push} ∉ #stackAlphabet)'
                    print(out)
                    return False # simbolo no se encuentre en el alfabeto de la pila {PSigma}, abortar
                out+=  f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })->'
                if('$' != pop and '$' !=push):
                    self.modificarPila(pila, 'swap',push)
                else:
                    if(self.modificarPila(pila, 'pop', pop)==False):
                        out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted'
                        print(out)
                        return False#Pila vacía al momento de hacer pop(), procesamiento abortado
                        #aceptada = False 
                    self.modificarPila(pila, 'push', push)

        out+=  f'({actual},$,{"$" if len(pila)==0 else "".join(pila) })>>'
        if actual in self.F and len(pila)==0: #verificar si el estado actual es de aceptacion
            if(aceptada==None):
                out+='accepted'
                aceptada=True
        else:
            if(aceptada==None):
                out+='rejected'
            aceptada= False
        print(out)
        return aceptada
       
        
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto. Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.
        Los campos deben estar separados por tabulación y son:
        1. cadena.
        2. procesamiento (con el formato del archivo AFPD.pdf).
        3. ‘yes’ o ‘no’ dependiendo de si la cadena es aceptada o no.
        """
        out=''
        estados=self.delta.keys()
        for cadena in listaCadenas:
            out+=f'{cadena}\t'
            pila =list()
            actual = self.q0
            estados=self.delta.keys()
            aceptada=None

            for index, simbolo in enumerate(cadena):
                if  simbolo not in self.Sigma.simbolos:  
                    out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted'
                    break # El simbolo no se encuentre en el alfabeto entrada {Sigma}, procesamiento abortado
                if(actual in estados):  # procesar la cadena
                    if(self.delta.get(actual)==None):
                        out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })->'
                        break # estado {actual} sin transiciones, posible estado limbo o estado final
                    elif(self.delta[actual].get(simbolo)==None):
                        aceptada = False # transicion con simbolo actual no disponible, por lo tanto se aborta el procesamiento
                        out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted'
                    if len(self.delta[actual][simbolo])>1:
                        raise ValueError('No puede haber mas de una transición para un simbolo, no corresponde al comportamiento de un AFPD')
                    transicion= self.delta[actual][simbolo][0]
                    pop, push, actual = transicion
                    if not all(simb in self.PSigma.simbolos for simb in pop) or not all(simb in self.PSigma.simbolos for simb in push):
                        out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted, ({pop} ∉ #stackAlphabet) V ({push} ∉ #stackAlphabet)'
                        break# simbolo no se encuentre en el alfabeto de la pila {PSigma}, abortar
                    out+=  f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })->'
                    if('$' != pop and '$' !=push):
                        self.modificarPila(pila, 'swap',push)
                    else:
                        if(self.modificarPila(pila, 'pop', pop)==False):
                            out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })>>aborted'
                            aceptada = False #Pila vacía al momento de hacer pop(), procesamiento abortado
                            break
                        self.modificarPila(pila, 'push', push)

            out+=  f'({actual},$,{"$" if len(pila)==0 else "".join(pila) })>>'
            if actual in self.F and len(pila)==0: #verificar si el estado actual es de aceptacion
            #if(aceptada==None):
                out+='accepted'
                aceptada=True
            else:
                if(aceptada==None):
                    out+='rejected'
                aceptada= False
            out+=f'\t{"yes" if aceptada else "no"}\n'

        try:
            with open(f'./archivosSalida/{nombreArchivo}.txt', "w") as f:
                f.write(out)
        except:
            with open(f'./archivosSalida/procesarListaCadenas_AFPD.txt', "w") as f:
                f.write(out)
        if(imprimirPantalla):
            print(out)

            
    def hallarProductoCartesianoConAFD(afd):
        """: debe calcular y retornar el producto cartesiano con un AFD dado como parámetro."""
        pass
    def toString(self):
        """Representar  el  AFPD  con  el  formato  de  los  archivos  de  entrada  de  AFPD (AFPD.pdf)de manera que se pueda imprimir fácilmente"""
        if self.instanciaVacia: return 'Instancia AFD vacía, no se le asigno un archivo o argumentos'
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] + '\n'+ '\n'.join(sorted(list(self.Q)))+ '\n'+self.etiquetas[2]+'\n'+self.q0+'\n'+self.etiquetas[3] + '\n'.join(sorted(list(self.F)))+  '\n'+self.etiquetas[4]+'\n'+self.Sigma.toStringEntrada()+ '\n'+ self.etiquetas[5]+ '\n'+ self.PSigma.toStringEntrada()+'\n'+self.etiquetas[6]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= self.delta[q][simb][0]
                deltaLinea=f'{q}:{simb}:{deltaSet[0]}>{deltaSet[2]}:{deltaSet[1]}'
                out+='\n'+deltaLinea
                #print ('deltaLinea: ',deltaLinea)
        return out
    

pila1= AFPD('ej1.dpda')
#print(pila1.toString())
cadena1= 'aa'
# print('procesando ', cadena1, '--> ',pila1.procesarCadena(cadena1))
# print('procesando ', 'aaabbbb', '--> ',pila1.procesarCadenaConDetalles('aaabbbb'))
pila1.procesarListaCadenas(['aabb', 'aab', 'aaabcbb', 'bb', 'aaaa'], 'intento1', True)
