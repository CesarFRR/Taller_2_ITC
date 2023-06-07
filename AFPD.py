from AFD import AFD
import copy
import re
from Alfabeto import Alfabeto
class AFPD:
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
                with open(args[0], 'r', newline='', encoding='utf-8') as file:
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
                                estado, simbolo, push, estadoDestino, pop = trans
                                #print('trans: ', trans)
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={ simbolo:[[push, pop, estadoDestino]] }
                                else:
                                    if(dictReader[estado].get(simbolo)==None):
                                        dictReader[estado][simbolo]=[[pop, push, estadoDestino]]
                                    else:
                                        dictReader[estado][simbolo].append([push, pop, estadoDestino])
                            
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
            self.qo=args[0].q0
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



    def modificarPila(self, pila: list, operacion: str, parametro: str):
        """Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase."""
        parametro=list(parametro)
        if operacion == 'push':
            for simb in parametro:
                if(simb!= '$'):
                    pila.append(simb)
        elif operacion == 'pop':
            for _ in parametro:
                if(simb!= '$'):
                    pila.pop()
        elif operacion == 'swap':
            for simb in parametro:
                pila.pop()
                pila.append(simb)
                    
        return True
    def procesarCadena(self, cadena):   #Procesar cadena con delta como un diccionario
        """ procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata. """
        pila =list()
        actual = self.q0
        estados=self.delta.keys()
        for simbolo in cadena:
            if simbolo not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto entrada
                return False
            if(actual in estados):  #Realizar transicion 
                if(self.delta.get(actual)==None):
                    break
                elif(self.delta[actual].get(simbolo)==None):
                    return False
                if len(self.delta[actual][simbolo])>1: raise ValueError('No puede haber mas de una transición para un simbolo, no corresponde al comportamiento de un AFPD')
                transicion= self.delta[actual][simbolo][0]
                pop, push = transicion[0], transicion[1]
                if pop not in self.PSigma.simbolos or push not in self.PSigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto de la pila
                    return False
                if('$' != pop and '$' !=push):
                    self.modificarPila(pila, 'swap',push)
                else:
                    self.modificarPila(pila, 'pop', pop[0])
                    self.modificarPila(pila, 'push', pop[1])

        if actual in self.F and len(pila)==0: #verificar si el estado actual es de aceptacion
            return True
        else:
            return False
        
    def procesarCadenaConDetalles(self, cadena):
        """realiza  lo  mismo  que  el  método  anterior aparte  imprime  losdetalles  del  procesamiento  con  el  formato  que se  indica  en  el  archivo AFPD.pdf."""
        #(q0,aabb,$)->(q0,abb,A)->(q0,bb,AA)->(q1,b,A)->(q1,$,$)>>accepted
        #(q0,aabbb,$)->(q0,abbb,A)->(q0,bbb,AA)->(q1,bb,A)->(q1,b,$)>>rejected
        pila =list()
        out=''
        actual = self.q0
        estados=self.delta.keys()
        for index, simbolo in enumerate(cadena):
            if simbolo not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto entrada
                out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })-> Procesamiento abortado'
                print(out)
                return False
            if(actual in estados):  #Realizar transicion 
                out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })-> '
                if(self.delta.get(actual)==None):
                    break
                elif(self.delta[actual].get(simbolo)==None):
                    out+='Procesamiento abortado'
                    print(out)
                    return False
                if len(self.delta[actual][simbolo])>1: raise ValueError('No puede haber mas de una transición para un simbolo, no corresponde al comportamiento de un AFPD')
                transicion= self.delta[actual][simbolo][0]
                pop, push = transicion[0], transicion[1]
                if pop not in self.PSigma.simbolos or push not in self.PSigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto de la pila
                    return False
                if('$' != pop and '$' !=push):
                    self.modificarPila(pila, 'swap',push)
                else:
                    self.modificarPila(pila, 'pop', pop[0])
                    self.modificarPila(pila, 'push', pop[1])
        print(out)
        if actual in self.F and len(pila)==0: #verificar si el estado actual es de aceptacion
            return True
        else:
            return False
        
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.
        Los campos deben estar separados por tabulación y son:
        1. cadena.
        2. procesamiento (con el formato del archivo AFPD.pdf).
        3. ‘yes’ o ‘no’dependiendo de si la cadena es aceptada o no.
        """
        for cadena in listaCadenas:
            pila =list()
            out=''
            aceptada=None
            actual = self.q0
            estados=self.delta.keys()
            for index, simbolo in enumerate(cadena):
                if simbolo not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto entrada
                    out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })-> Procesamiento abortado'
                    aceptada=False
                    break
                if(actual in estados):  #Realizar transicion 
                    out+= f'({actual},{cadena[index:]},{"$" if len(pila)==0 else "".join(pila) })-> '
                    if(self.delta.get(actual)==None):
                        break
                    elif(self.delta[actual].get(simbolo)==None):
                        out+='Procesamiento abortado'
                        print(out)
                        return False
                    if len(self.delta[actual][simbolo])>1: raise ValueError('No puede haber mas de una transición para un simbolo, no corresponde al comportamiento de un AFPD')
                    transicion= self.delta[actual][simbolo][0]
                    pop, push = transicion[0], transicion[1]
                    if pop not in self.PSigma.simbolos or push not in self.PSigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto de la pila
                        return False
                    if('$' != pop and '$' !=push):
                        self.modificarPila(pila, 'swap',push)
                    else:
                        self.modificarPila(pila, 'pop', pop[0])
                        self.modificarPila(pila, 'push', pop[1])
            if actual in self.F : #verificar si el estado actual es de aceptacion
                if(aceptada==None):
                    out+= 'Aceptacion'
                aceptada= True
            print(out)
            if actual in self.F and len(pila)==0: #verificar si el estado actual es de aceptacion
                return True
            else:
                return False
            
        # estados=self.delta.keys()
        # out=''

        # for cadena in listaCadenas:
        #     actual = self.q0
        #     aceptada=None
        #     for index, char in enumerate(cadena): #     [Q0,aabb]->[Q1,abb]->[Q2,bb] -> [Q1,b]-> Aceptacion | [Q0,aabb]->[Q1,abb]->[Q2,bb] -> [Q2,b]-> No Aceptacion
        #         if char not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
        #             out+= f'[{actual},{cadena[index:]}]-> Procesamiento abortado'
        #             aceptada= False
        #             break
        #         if(actual in estados):
        #             out+= f'[{actual},{cadena[index:]}]-> ' 
        #             actual = list(self.delta[actual][char])[0] if len(self.delta[actual][char])==1 else '('+','.join(self.delta[actual][char])+')'
        #     if actual in self.F : #verificar si el estado actual es de aceptacion
        #         if(aceptada==None):
        #             out+= 'Aceptacion'
        #         aceptada= True
        #     else:
        #         if(aceptada==None):
        #             out+= 'No Aceptacion'
        #         aceptada= False
        #     out+='\n'
  
        # with open(f'{nombreArchivo}procesarListaCadenas.txt', "w") as f:
        #     f.write(out)
        # if(imprimirPantalla):
        #     print(out)
        # pass
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
print(pila1.toString())
