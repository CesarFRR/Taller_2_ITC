import copy
import re
from Alfabeto import Alfabeto
from itertools import product as productoCartesiano
from prettytable import PrettyTable
from Graph import graficarAutomata

class AFD:
    """
    # Clase AFD

    Ésta clase modela y simula el Autómata Finito determinista AFD el cual puede poseer cero o una transición para un símbolo perteneciente al Alfabeto

        >>> AFD('nombreDeArchivo.nfa')
        # Lee un archivo de entrada afd.
        
        >>> AFD(alfabeto: Alfabeto, estados: set, estadoInicial: str, estadosAceptacion: set, Delta: dict)
        # Recibe los 5 atributos del autómata
        
        >>> AFD(instanciaAfd: AFD)
        # Recibe como parámetro una instancia de la misma clase creando una copia exacta de ésta gracias a la librería copy
        
    """
    Sigma = None
    Q = None
    q0 = None
    F = None
    delta = None # se intentara hacer el delta como  un diccionario, cada estado q contiene otro diccionario --> clave:simbolo, valor: conjunto de estados resultantes tras evaluar con la funcion delta
    estadosLimbo = None
    estadosInaccesibles = None
    nombreArchivo='archivo'
    extension = "dfa"
    etiquetas=['#!dfa', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
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
                    for i in string.split('\n'):
                        if i in self.etiquetas[1:]:
                            key = i
                        elif i != '' or not i.isspace():
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions' and i.split(":")[1].split(">")[0]!= "$": # AFD: no contiene transiciones lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3 or ';' in trans[2]): raise ValueError("transicion invalida: ", i) # "; " q no puede tener varias salidas con un simbolo
                                estado, simbolo, deltaResultado = trans
                                #print('trans: ', trans)
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={simbolo: set({deltaResultado}) }
                                else:
                                    dictReader[estado].update({simbolo:set({deltaResultado})})
                    #print('en constructor, mostrar alphabet:---> ', afc['#alphabet'])
                    self.Sigma = Alfabeto(afc['#alphabet'])
                    self.Q = set(afc['#states'])
                    self.q0 = afc['#initial'][0]
                    self.F = set(afc['#accepting'])
                    self.delta = dictReader
                    self.nombreArchivo=((args[0]).split('.'+self.extension))[0]
                    self.verificarCorregirCompletitudAFD()
                    self.hallarEstadosLimbo()
                    self.estadosInaccesibles= self.hallarEstadosInaccesibles()
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            simbolos, self.Q, self.q0, self.F, self.delta = args
            if(isinstance(simbolos, Alfabeto)):
                self.Sigma=simbolos
            else:
                self.Sigma=Alfabeto(simbolos)
            self.Q=set(self.Q)
            
            self.estadosLimbo = set()
            self.estadosInaccesibles=set()
            self.verificarCorregirCompletitudAFD()
            self.hallarEstadosLimbo()
            self.estadosInaccesibles= self.hallarEstadosInaccesibles()
        elif(len(args) == 1 and isinstance(args[0], AFD)):
            self.Sigma=copy.deepcopy(args[0].Sigma)
            self.Q=copy.deepcopy(args[0].Q)
            self.q0=args[0].q0
            self.F=copy.deepcopy(args[0].F)
            self.delta=copy.deepcopy(args[0].delta)
            self.estadosInaccesibles=copy.deepcopy(args[0].estadosInaccesibles)
            self.estadosLimbo=copy.deepcopy(args[0].estadosLimbo)
        elif(len(args) == 0):
            self.Sigma = Alfabeto('')
            self.Q = set()
            self.q0 = ''
            self.F = set()
            self.delta = {}
            self.estadosLimbo = set()
            self.estadosInaccesibles = set()
            self.instanciaVacia=True

        


    def verificarCorregirCompletitudAFD(self):
        """Revisa si el AFD leído está completo y sino agrega un estado limbo y ajusta las transiciones para que quede completo."""
        if self.estadosLimbo==None:
            self.estadosLimbo=set()
        limbo = { 'L':{  s:'L' for s in self.Sigma.simbolos} }
        faltalimbo=False
        for estado in self.delta:
            for simb in self.Sigma.simbolos:
                if(self.delta[estado].get(simb)==None):
                    if(not 'L' in self.delta.keys()):
                        faltalimbo = True
                    self.delta[estado][simb]='L'
                    self.estadosLimbo.add('L')
        if faltalimbo: self.delta.update(limbo)
        
    def hallarEstadosLimbo(self):
        """ para determinar los estados limbo del autómata y guardarlos en el atributocorrespondiente. """
        if (self.estadosLimbo==None):
            self.estadosLimbo =set()
        for estado in self.delta:
            if all( self.delta[estado].get(simb, set())=={estado} for simb in self.Sigma.simbolos):
                #estado limbo encontrado!
                if(estado==self.q0): raise ValueError('El estado inicial no puede ser un estado limbo')
                elif(estado in self.F):
                    continue
                self.estadosLimbo.add(estado)
                self.Q.add(estado)

    def hallarEstadosInaccesibles(self):
        """ para determinar los estados inacessibles del autómata y guardarlos en el atributo correspondiente."""
        visitados = set()  # Conjunto para almacenar los nodos visitados
        cola = [self.q0]  # Cola para realizar el recorrido en anchura
            
        while cola:
            nodo_actual = cola.pop(0)  # Tomar el primer nodo de la cola
            
            if nodo_actual not in visitados:
                # Procesar el nodo actual
                
                visitados.add(nodo_actual)  # Marcar el nodo como visitado
                
                # Agregar los vecinos no visitados a la cola
                for _, trans in self.delta[nodo_actual].items():
                    for q in trans:
                        if q not in visitados:
                            cola.append(q)

                    
        return self.Q.difference(visitados)

    def toString(self, graficar: bool=False)-> str:
        """método para imprimir donde se vean los estados, estado inicial, estados de aceptación, estados inaccesibles, estados limbo y tabla de transiciones. """
        if self.instanciaVacia: return 'Instancia AFD vacía, no se le asigno un archivo o argumentos'
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= list(self.delta[q][simb])[0]
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        if(graficar):
            self.graficarAutomata()
        return out

    def exportar(self, archivo):
        """ Guardar el autómata en un archivo con el formatoespecificado"""

        with open(f'./archivosSalida/{archivo}', "w") as f:
            f.write(self.toString())

    def procesarCadena(self, cadena: str)->bool:
        """procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata"""
        actual = self.q0
        estados=self.delta.keys()
        for i in cadena:
            if i not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                return False
            if(actual in estados):  #Realizar transicion 
                actual = list(self.delta[actual][i])[0] if len(self.delta[actual][i])==1 else '('+','.join(self.delta[actual][i])+')'#Realizar transicion 
                 #Nota2: Se modifico para porder recibir los estados resultantes de la conversion sin problemas
            #Nota: no es necesario verificar si la transicion existe en el estado actual, 
            # en el constructor se relleno con Limbos las transiciones que faltaban en la lectura de las transiciones del archivo,
            # por lo que la clase AFD siempre trabaja con tablas de transiciones completas
 
        if actual in self.F: #verificar si el estado actual es de aceptacion
            return True
        else:
            return False   
            

    def procesarCadenaConDetalles(self, cadena: str)-> bool:
        """ realiza lo mismo que el método `procesarCadena()` pero aparte imprime los estados que va tomando al procesar cada símbolo."""
        actual = self.q0
        estados=self.delta.keys()
        out=''
        aceptada=None
        for index, char in enumerate(cadena): #     [Q0,aabb]->[Q1,abb]->[Q2,bb] -> [Q1,b]-> Aceptacion | [Q0,aabb]->[Q1,abb]->[Q2,bb] -> [Q2,b]-> No Aceptacion
            if char not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                out+= f'[{actual},{cadena[index:]}]-> Procesamiento abortado'
                print(out)
                return False
            if(actual in estados):
                out+= f'[{actual},{cadena[index:]}]-> ' 
                actual = list(self.delta[actual][char])[0] if len(self.delta[actual][char])==1 else '('+','.join(self.delta[actual][char])+')'
                #Nota: Se modifico para porder recibir los estados resultantes de la conversion sin problemas

        if actual in self.F: #verificar si el estado actual es de aceptacion
            out+= 'Aceptacion'
            aceptada= True
        else:
            out+= 'No Aceptacion'
            aceptada= False
        print(out)
        return aceptada

    def procesarListaCadenas(self, listaCadenas: list, nombreArchivo: str='', imprimirPantalla: bool=False):
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por defecto.Además,todo esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla. Los campos deben estar separados por tabulación y son:
        1. cadena,
        2. sucesion de parejas (estado, símbolo) de cada paso del procesamiento .
        3. sí o no dependiendo de si la cadena es aceptada o no."""
        estados=self.delta.keys()
        out=''

        for cadena in listaCadenas:
            out+=cadena+'\t'
            actual = self.q0
            aceptada=None
            for index, char in enumerate(cadena): #     [Q0,aabb]->[Q1,abb]->[Q2,bb] -> [Q1,b]-> Aceptacion | [Q0,aabb]->[Q1,abb]->[Q2,bb] -> [Q2,b]-> No Aceptacion
                if char not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                    out+= f'[{actual},{cadena[index:]}]-> Procesamiento abortado'
                    aceptada= False
                    break
                if(actual in estados):
                    out+= f'[{actual},{cadena[index:]}]-> ' 
                    actual = list(self.delta[actual][char])[0] if len(self.delta[actual][char])==1 else '('+','.join(self.delta[actual][char])+')'
                    
            if actual in self.F : #verificar si el estado actual es de aceptacion
                if(aceptada==None):
                    out+= 'Aceptacion\tyes'
                aceptada= True
            else:
                if(aceptada==None):
                    out+= 'No Aceptacion\tno'
                aceptada= False
            out+='\n'
        try:
            with open(f'./archivosSalida/{nombreArchivo}.txt', "w") as f:
                f.write(out)
        except:
            with open(f'./archivosSalida/procesarListaCadenas_AFD.txt', "w") as f:
                f.write(out)
        if(imprimirPantalla):
            print(out)

    def AFD_hallarComplemento(self, afdInput ):
        """Debe calcular y retornar el complemento de afdInput."""
        print("hallando complemento: \n")
        complemento= AFD(afdInput)
        nuevosEstadosF= self.Q.difference(self.F)
        complemento.F=nuevosEstadosF
        return complemento
    @staticmethod
    def AFD_hallarProductoCartesianoY(afd1 , afd2 ):
        """ hallar el producto cartesiano de afd1 y afd2 de manera que se acepte el lenguajeL(afd1)∩L(afd2)."""
        afd1Q=sorted(list(afd1.Q))
        afd2Q=sorted(list(afd2.Q))
        pares =productoCartesiano(afd1Q, afd2Q)
        paresOrdenados=list([(list(p)) for p in pares]) 
        #print(paresOrdenados)
        nuevoSigma=afd1.Sigma 
        nuevoQ=set()
        nuevoq0=''
        nuevoF=set()
        nuevoDelta={}
        out=[] #Lo que el profe pide imprimir --> ProductoCartesiano.png
        for q1, q2 in paresOrdenados:
            nuevoEstado=f'{q1},{q2}'
            nuevoQ.add(nuevoEstado)
            nuevoDelta.update({nuevoEstado:{}})
            if(q1 in afd1.F and q2 in afd2.F): # INTERSECCION: Se usa el AND
                nuevoF.add(nuevoEstado)
            if({q1,q2}=={afd1.q0, afd2.q0}):
                nuevoq0 =nuevoEstado
            for simbolo in afd1.Sigma.simbolos: 
                qAFD1= list(afd1.delta[q1][simbolo])[0] # qAFD1 = d(qn, simbolo)
                qAFD2= list(afd2.delta[q2][simbolo])[0]
                out.append(f'd(({q1},{q2}),{simbolo}) = (d1({q1},{simbolo}),d2({q2},{simbolo})) = ({qAFD1},{qAFD2})')
                nuevoDelta[nuevoEstado][simbolo]={f'{qAFD1},{qAFD2}'}

        print('\n'.join(out))
        return AFD(nuevoSigma, nuevoQ, nuevoq0, nuevoF, nuevoDelta)
    
    @staticmethod
    def AFD_hallarProductoCartesianoO(afd1 , afd2 ):
        """ hallar el producto cartesiano de afd1 y afd2 de manera que se acepte el lenguajeL(afd1)∪L(afd2)."""
        #1. hacer los pares del producto cartesiano usando la libreria itertools
        #print('producto cartesiano:\n')
        afd1Q=sorted(list(afd1.Q))
        afd2Q=sorted(list(afd2.Q))
        #print('afd1Q: ', afd1Q, '\nafd2Q: ', afd2Q)
        #print('afd1 q0: ', afd1.q0, '\nafd2 q0: ', afd2.q0)
        pares =productoCartesiano(afd1Q, afd2Q)
        paresOrdenados=list([(list(p)) for p in pares]) #Lista de listas, los sets() no dejan ordenar, importante ordenar
        #print('producto cartesiano Ordenado:\n')
        #print(paresOrdenados)
        #2. Hallar los pares que son el resultado de evaluar los ParesOrdenados con delta1 y delta2,
        # al mismo tiempo que se desarrollan los nuevos atributos del nuevo AFD
        # Nota: para cada par (a, b) de paresOrdenados, (a) pertenece afd1, (b) a afd2, por eso el orden importa
        #print('\nNuevo AFD:\n')
        nuevoSigma=afd1.Sigma # Ley: ambos deben tener el mismo alfabeto A, por eso basta con que este sigma tambien sea A
        nuevoQ=set()
        nuevoq0=''
        nuevoF=set()
        nuevoDelta={}
        out=[] #Lo que el profe pide imprimir --> ProductoCartesiano.png
        for q1, q2 in paresOrdenados:
            nuevoEstado=f'{q1},{q2}'
            nuevoQ.add(nuevoEstado)
            nuevoDelta.update({nuevoEstado:{}})
            if(q1 in afd1.F or q2 in afd2.F): # UNION: Aqui se usa el OR, en interseccion se usaria el AND y en las demas, opreaciones entre conjuntos
                nuevoF.add(nuevoEstado)
            if({q1,q2}=={afd1.q0, afd2.q0}): # Definimos el nuevo estado inicial (q0), se comparan con conjuntos (a prueba de errores)
                nuevoq0 =nuevoEstado
                #print('estado q0 elegido, es:', nuevoEstado)

            for simbolo in afd1.Sigma.simbolos: 
                qAFD1= list(afd1.delta[q1][simbolo])[0] # qAFD1 = d(qn, simbolo)
                qAFD2= list(afd2.delta[q2][simbolo])[0]
                out.append(f'd(({q1},{q2}),{simbolo}) = (d1({q1},{simbolo}),d2({q2},{simbolo})) = ({qAFD1},{qAFD2})')
                #print(out[-1])
                nuevoDelta[nuevoEstado][simbolo]={f'{qAFD1},{qAFD2}'}
        # print('\nAlfabeto (Sigma) del nuevoAFD: ', nuevoSigma.simbolos)
        # print('\nself.Q del nuevo AFD: ', nuevoQ, 'tamaño: ', len(nuevoQ))
        # print('\nq0 del nuevoAFD: ', nuevoq0)
        # print('\nestados de aceptacion del nuevoAFD: ', nuevoF, 'tamaño: ', len(nuevoF))
        # print('\ndelta del nuevoAFD: ', nuevoDelta, '\nTamaño del delta: ', len(nuevoDelta))
        print('\n'.join(out))
        return AFD(nuevoSigma, nuevoQ, nuevoq0, nuevoF, nuevoDelta)

    @staticmethod    
    def AFD_hallarProductoCartesianoDiferencia(afd1 , afd2 ):
        """hallar el producto cartesiano de afd1 y afd2 de manera que se acepte el lenguajeL(afd1)−L(afd2)."""
        afd1Q=sorted(list(afd1.Q))
        afd2Q=sorted(list(afd2.Q))
        pares =productoCartesiano(afd1Q, afd2Q)
        paresOrdenados=list([(list(p)) for p in pares]) 
        print(paresOrdenados)
        nuevoSigma=afd1.Sigma 
        nuevoQ=set()
        nuevoq0=''
        nuevoF= set() 
        nuevoDelta={}
        out=[] #Lo que el profe pide imprimir --> ProductoCartesiano.png
        for q1, q2 in paresOrdenados:
            nuevoEstado=f'{q1},{q2}'
            nuevoQ.add(nuevoEstado)
            nuevoDelta.update({nuevoEstado:{}})
            if(q1 in afd1.F and q2 not in afd2.F): # DIFERENCIA: 
                nuevoF.add(nuevoEstado)
            if({q1,q2}=={afd1.q0, afd2.q0}):
                nuevoq0 =nuevoEstado

            for simbolo in afd1.Sigma.simbolos: 
                qAFD1= list(afd1.delta[q1][simbolo])[0] # qAFD1 = d(qn, simbolo)
                qAFD2= list(afd2.delta[q2][simbolo])[0]
                out.append(f'd(({q1},{q2}),{simbolo}) = (d1({q1},{simbolo}),d2({q2},{simbolo})) = ({qAFD1},{qAFD2})')
                #print(out[-1])
                nuevoDelta[nuevoEstado][simbolo]={f'{qAFD1},{qAFD2}'}
        print('\n'.join(out))
        return AFD(nuevoSigma, nuevoQ, nuevoq0, nuevoF, nuevoDelta)
    
    @staticmethod
    def AFD_hallarProductoCartesianoDiferenciaSimetrica( afd1 , afd2 ):
        """hallar el producto cartesiano de afd1 y afd2 de manera que se aceptela diferencia simétricaentreL(afd1)yL(afd2), i.e.el lenguajeL(afd1)△L(afd2)"""
        afd1Q=sorted(list(afd1.Q))
        afd2Q=sorted(list(afd2.Q))
        pares =productoCartesiano(afd1Q, afd2Q)
        paresOrdenados=list([(list(p)) for p in pares]) 
        print(paresOrdenados)
        nuevoSigma=afd1.Sigma 
        nuevoQ=set()
        nuevoq0=''
        nuevoF= set() 
        nuevoDelta={}
        out=[] #Lo que el profe pide imprimir --> ProductoCartesiano.png
        for q1, q2 in paresOrdenados:
            nuevoEstado=f'{q1},{q2}'
            nuevoQ.add(nuevoEstado)
            nuevoDelta.update({nuevoEstado:{}})
            if(q1 in afd1.F) != (q2 in afd2.F): # DIFERENCIA SIMETRICA 
                nuevoF.add(nuevoEstado)
            if({q1,q2}=={afd1.q0, afd2.q0}):
                nuevoq0 =nuevoEstado
            for simbolo in afd1.Sigma.simbolos: 
                qAFD1= list(afd1.delta[q1][simbolo])[0] # qAFD1 = d(qn, simbolo)
                qAFD2= list(afd2.delta[q2][simbolo])[0]
                out.append(f'd(({q1},{q2}),{simbolo}) = (d1({q1},{simbolo}),d2({q2},{simbolo})) = ({qAFD1},{qAFD2})')
                #print(out[-1])
                nuevoDelta[nuevoEstado][simbolo]={f'{qAFD1},{qAFD2}'}
        print('\n'.join(out))
        return AFD(nuevoSigma, nuevoQ, nuevoq0, nuevoF, nuevoDelta)
    @staticmethod
    def AFD_hallarProductoCartesiano(afd1 , afd2 , StringOperacion):
        """Dado dos AFD, calcular su producto cartesiano donde la variable operacion determina el tipo de aceptación que se debe manejar: "interseccion", "union", "diferencia" o "diferencia simétrica"."""
        # "interseccion", "union", "diferencia" o "diferencia simétrica"
        AFD=None
        union=['union', 'u', '+', '∪']
        inters=['intersección','interseccion', 'and', '^', '∩']
        dif=['diferencia', 'difference', 'diff', 'dif', '-']
        difSimetrica=['diferencia simétrica', 'diferencia simetrica', 'd']
        if(StringOperacion in union):
            AFD = AFD.AFD_hallarProductoCartesianoO(afd1,afd2)
        elif(StringOperacion in inters):
            AFD = AFD.AFD_hallarProductoCartesianoY(afd1,afd2)
        elif(StringOperacion in dif):
            AFD = AFD.AFD_hallarProductoCartesianoDiferencia(afd1,afd2)
        elif(StringOperacion in difSimetrica):
            AFD = AFD.AFD_hallarProductoCartesianoDiferenciaSimetrica(afd1,afd2)

        return AFD


    def AFD_simplificarAFD(self, afd1):
        afd = AFD(afd1)

        # SIMPLIFICAR USANDO UNA MATRIZ COMPLETA

        delta = afd.delta
        F= afd.F
        estados= sorted(list(afd.Q))
        n = len(estados)  # Tamaño de la matriz
        matriz = [['E'] * n for _ in range(n)]  # Inicializar matriz con 'E'
        # Paso 1: Crear los pares de estados involucrados en el DFA dado
        totalParejas=set()
        marcados0= set()
        # Paso 2: Marcar los pares (Qa, Qb) donde Qa está en F y Qb no está en F
        for i in range(n):
            totalParejas.update([  (estados[i],estados[x]) for x in range(n) if estados[i]!= estados[x] and i<x]  )
            for j in range(n):
                if (estados[i] in F) != (estados[j] in F):
                    matriz[i][j] = '1'
                    matriz[j][i] = '1'
                    if (estados[i], estados[j]) not in marcados0 and (estados[j], estados[i]) not in marcados0 and estados[i]!=estados[j]:
                        marcados0.add( (estados[i], estados[j]))
        # Paso 3: Marcar los pares (Qa, Qb) que cumplen la condición de transición marcada
        marcados = set()
        ciclo = 2
        while True:
            nuevos_marcados = set()
            for i in range(n):
                for j in range(n):
                    if matriz[i][j] == 'E':
                        qa = estados[i]
                        qb = estados[j]
                        marcado = None
                        for simb in afd.Sigma.simbolos:
                            transQa= delta.get(qa, None)
                            transQb = delta.get(qb, None)
                            if(not transQa) or (not transQb): # Cualquier estado o cualquier simbolo que...
                                marcado = False
                                break
                            transQa = transQa.get(simb, None)
                            transQb = transQb.get(simb, None)
                            if(not transQa) or (not transQb): # ...no exista, significa que esto conduce a un estado de no aceptación,
                                # por lo que el caso (qa, qb) de ese instante se descarta inmediatamente
                                # print('ERROR, SIMBOLO NO ENCONTRADO: ', transQa, transQb, 'simb: ', simb, 'originales qa y qb: ', qa, qb)
                                # print('delta de qa:', delta.get(qa, None), '\ndelta de qb: ', delta.get(qb, None))
                                marcado=False
                                break
                            if(transQa== transQb): # Se descarta tambien si el par es igual, ej: (q3,q3), esto no se usa en la matriz
                                marcado=False
                                break
                            indexQa= estados.index(list(transQa)[0])
                            indexQb= estados.index(list(transQb)[0])
                            if(indexQa>indexQb):
                                indexQa, indexQb = indexQb, indexQa
                            # Con comparar uno de los dos sectores de un q1,q2 de la matriz basta:
                            if (matriz[indexQa][indexQb] !='E' and int(matriz[indexQa][indexQb])<ciclo ): # int(matriz[indexQa][indexQb])<ciclo hace que se registre el ultimo ciclo
                                cycle= str(ciclo)
                                matriz[i][j] = cycle
                                matriz[j][i] = cycle
                                marcado=True
                                break
                        if marcado and (qa, qb) not in nuevos_marcados and (qb,qa) not in nuevos_marcados:
                            nuevos_marcados.add((qa, qb)) # se agrega a los nuevos (i,j) no se agrega (j,i) por redundancia
            if len(nuevos_marcados) == 0:
                break
            marcados.update(nuevos_marcados)
            ciclo += 1
        marcados.update(marcados0)

        # IMPRIMIR TABLA TRIANGULAR

        for i in range(n):
            for j in range(i+1):  # Solo imprime elementos hasta la diagonal principal
                if(i==j):
                    print(estados[i], end=' |\n')
                else:
                    print(matriz[j][i], end=" "*len(estados[i]) + "|" + " "*len(estados[i]) ) 
            print()  # Salto de línea después de cada fila

        # IMPRIMIR TABLA DEL DELTA

        noMarcados = totalParejas.difference(marcados)
        tabla = PrettyTable()
        simbolos=sorted(afd.Sigma.simbolos)
        encabezado=['{p,q}']
        for simb in simbolos:
            encabezado.append('{' + f'd(p,{simb}),d(q,{simb})' + '}')
        tabla.field_names = encabezado
        n= len(matriz)
        for i in range(n):
            for j in range(n):
                if (estados[i],estados[j]) in marcados:
                    qa, qb = estados[i], estados[j]
                    ciclo= int(matriz[i][j])
                    filaTabla1=['{' + f'{qa},{qb}' + '}']
                    if(ciclo >1 ):
                        filaTabla1[0] = filaTabla1[0]+ f' X {ciclo}'
                    for simb in afd.Sigma.simbolos:
                        qaEv = list(delta[qa][simb])[0]
                        qbEv = list(delta[qb][simb])[0]
                        filaTabla1.append('{' + f'{qaEv},{qbEv}' + '}')
                    tabla.add_row(filaTabla1)
                elif (estados[i],estados[j]) in noMarcados:
                    filaTabla2=['{' + f'{qa},{qb}' + '}']
                    for simb in afd.Sigma.simbolos:
                        qaEv = list(delta[qa][simb])[0]
                        qbEv = list(delta[qb][simb])[0]
                        filaTabla2.append('{' + f'{qaEv},{qbEv}' + '}')
                    tabla.add_row(filaTabla2)
        print(tabla)

        # FUSIONAR ESTADOS EN EL DELTA ORIGINAL
        sorted_noMarcados =sorted(list(noMarcados))
        for qa, qb in sorted_noMarcados:
            estadoNext=set()
            new_key= '{'+f'{qa},{qb}'+'}'
            afd.delta[new_key]=dict()
            for simb in afd.Sigma.simbolos:
                afd.delta[new_key].update({simb:set()})
                estadoNext |=(delta[qa][simb])
                estadoNext |= (delta[qb][simb])
                if(len(estadoNext)==1):
                    afd.delta[new_key][simb]={estadoNext.pop()}
                else:
                    strQnext= '{'+",".join(sorted(list(estadoNext)))+'}'
                    delta[new_key][simb].add(strQnext)

        for qa, qb in sorted_noMarcados:
            strQ= '{'+f'{qa},{qb}'+'}'
            if (qa in afd.F or qb in afd.F):
                afd.F.difference_update({qa,qb})
                afd.F.add(strQ)
            if (qa in afd.Q or qb in afd.Q):
                afd.Q.difference_update({qa,qb})
                afd.Q.add(strQ)
            for q in delta:
                for simb in delta[q]:
                    trans= delta[q][simb].pop()
                    if(trans!=None):
                        if(trans in {qa,qb}):
                            delta[q][simb]={strQ}
                        else:
                            delta[q][simb]={trans}
            del delta[qa]
            del delta[qb]
        afd.nombreArchivo=afd1.nombreArchivo + 'Simplificado'
        return afd

    def imprimirAFDSimplificado(self,graficar: bool=False)-> str:
        """método para imprimir donde se vean los estados, estado inicial, estados de aceptación, y tabla de transiciones. No se deben mostrar los estados inaccesibles, ni los estados limbo, ni las transiciones que vayan a los estados limbo."""

        if self.instanciaVacia: return 'Instancia AFD vacía, no se le asigno un archivo o argumentos'
        simb=''
        simpDelta=copy.deepcopy(self.delta)
        simpQ= self.Q.difference(self.estadosInaccesibles)
        simpF= self.F.difference(self.estadosInaccesibles)
        #Ando simp estos dias
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(simpQ)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(simpF)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for q in self.delta:
            if(q in self.estadosLimbo):
                simpDelta.pop(q)
                continue
            for simb in self.delta[q]:
                
                deltaSet= list(self.delta[q][simb])[0]
                if(deltaSet in self.estadosLimbo):
                    simpDelta[q].pop(simb)
                    continue
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        if(graficar):
            AFD(self.Sigma, simpQ, self.q0, simpF, simpDelta).graficarAutomata()
        return out
    

    def graficarAutomata(self):
        """Grafica el automata usando librerias de matplotlib y NetworkX"""
        graficar = graficarAutomata()
        graficar.mostrarGrafo(self)


#================================================

#print('real Ejecutando:...\n')

#archivo1='impares' # AFD--> L: |w| impar
#afd1= AFD(archivo1+'.dfa') 
# cadena=''
# print('AFD: ',archivo1, ' Procesar la cadena: ',cadena,'resultado: ',  afd1.procesarCadena(cadena))
# print('\n\nAFD: ',archivo1, ' Procesar la cadena con detalles: ',cadena,'Procedimiento: \n')
# result= afd1.procesarCadenaConDetalles(cadena)
# print('\nResultado: ', result)
# afd1.exportar(archivo1+'Exportado.'+afd1.extension)

#exportar lista cadenas:
#listaCadenas= ['abba', 'baabb', 'bbabaaab', 'a', 'bba', 'baabba', 'aaaaaba', 'bbbbab', 'ababababbaXa']
#afd1.procesarListaCadenas(listaCadenas, 'procesarListaCadenasResultado.txt',True)

#archivo2='nocontieneBB' #AFD--> L: No contiene bb, que pendejada tan redundante :v
#afd2= AFD(archivo2+'.dfa')
#cadena='abaaabab'
#print('AFD: ',archivo2, ' Procesar la cadena: ',cadena,'resultado: ',  afd2.procesarCadena(cadena))
# afd2.exportar(archivo2+'Exportado.'+afd2.extension)

#Producto cartesiano
#archivo3=f'{archivo1}X{archivo2}' # L: impares O que no contengan bb
#afd3 = AFD.AFD_hallarProductoCartesianoO(afd1, afd2) #union

#afd3.graficarAFD()
#afd3 = AFD.AFD_hallarProductoCartesianoY(afd1, afd2) #Interseccion
#print('\nAFD nuevo, Alfabeto: ', afd3.Sigma.simbolos, '\nEstados: ', afd3.Q, '\nEstado inicial: ',afd3.q0, '\nEstados Finales: ', afd3.F, '\ndelta: ',afd3.delta)
#cadena= 'babab' # Contiene bb Y es impar --> True
#print('AFD: ',archivo3, ' Procesar la cadena: ',cadena,'resultado: ',  afd3.procesarCadena(cadena))
#afd3.exportar(archivo3+'Exportado.'+afd3.extension)
#print('\n#############################################################################')
#Faltan desarrollar algunos métodos
# simplificar= 'simplificar'
# afdsimp = AFD(simplificar+'.dfa') 
# #afdsimp.graficarAFD()
# simplificado = AFD.AFD_simplificarAFD(afdsimp)

# print(sorted(list(simplificado)))

