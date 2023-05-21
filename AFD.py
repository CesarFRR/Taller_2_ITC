import copy
import re
from Alfabeto import Alfabeto
from itertools import product as productoCartesiano


class AFD:
    Sigma = None
    Q = None
    q0 = None
    F = None
    delta = None # se intentará hacer el delta como  un diccionario, cada estado q contiene otro diccionario --> clave:simbolo, valor: conjunto de estados resultantes tras evaluar con la funcion delta
    estadosLimbo = None
    estadosInaccesibles = None
    extension = "dfa"
    etiquetas=['#!dfa', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
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
                    for i in string.split('\n'):
                        if i in self.etiquetas[1:]:
                            key = i
                        elif i != '' or not i.isspace():
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions' and i.split(":")[1].split(">")[0]!= "$": # AFD: no contiene transiciones lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3 or ';' in trans[2]): raise ValueError("transición inválida: ", i) # "; " q no puede tener varias salidas con un simbolo
                                estado, simbolo, deltaResultado = trans
                                #print('trans: ', trans)
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={simbolo: set({deltaResultado}) }
                                else:
                                    dictReader[estado].update({simbolo:set({deltaResultado})})
                    self.Sigma = Alfabeto(afc['#alphabet'])
                    self.Q = set(afc['#states'])
                    self.q0 = afc['#initial'][0]
                    self.F = set(afc['#accepting'])
                    self.delta = dictReader
                    #print('delta: ', self.delta)
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma, self.Q, self.qo, self.F, self.delta = args
            self.Q=set(self.Q)
        elif(len(args) == 1 and isinstance(args[0], AFD)):
            self.Sigma=copy.deepcopy(args[0].Sigma)
            self.Q=copy.deepcopy(args[0].Q)
            self.qo=args[0].q0
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

        
        self.estadosLimbo = set()
        self.estadosInaccesibles=set()
        self.verificarCorregirCompletitudAFD()
        self.hallarEstadosLimbo()

    def verificarCorregirCompletitudAFD(self):
        char =self.q0
        nombreLimbo='L'
        # if(len(char)>1 and isinstance(char[1], int)):  # Formas de nombrar al nuevo estado Limbo evitando repetidos
        #     nombreLimbo = f'{char[0]}{len(self.Q)+1}'
        #     if(nombreLimbo in self.Q):
        #         nombreLimbo = f'LimboDel{self.extension}_{len(self.Q)+1}'

        limbo = { 'L':{  s: {'L'} for s in self.Sigma.simbolos} }
        faltalimbo=False
        for estado in self.delta:
            for simb in self.Sigma.simbolos:
                if(self.delta[estado].get(simb)==None):
                    if(not 'L' in self.delta.keys()):
                        faltalimbo = True
                    self.delta[estado][simb]=limbo
                    self.estadosLimbo.add('L')

        if faltalimbo: self.delta.update(limbo)
        #print('verificarCorregirCompletitudAFD(): \n', self.toString())
        #out = self.toString() 

    def hallarEstadosLimbo(self):
        if (self.estadosLimbo==None):
            #print('estadosLimbo= None!!!!')
            self.estadoslimbo =set()
        for estado in self.delta:
            if all( self.delta[estado][simb]=={estado} for simb in self.Sigma.simbolos):
                #estado limbo encontrado!
                if(estado==self.q0): raise ValueError('El estado inicial no puede ser un estado limbo')
                self.estadosLimbo.add(estado)
                self.Q.add(estado)

    def hallarEstadosInaccesibles(self):
        accesibles ={self.q0} #Conjunto accesibles empieza con el inicial
        if (list(accesibles)[0]==None or list(accesibles)[0]==''): raise Exception("El estado inicial debe existir para hallar los inaccesibles")
        while True:
            alteraciones = False
            for estado in list(accesibles): #recorrer estados accesibles
                transiciones = self.delta[estado] # obtener los {'simbolo': delta} de un estado
                for estados_destino in transiciones.values(): #Recorrer los deltas de ese estado, cada estados_destino es un set(  ) de estados
                    for d in estados_destino: # Recorrer los elementos (estados) de ese set()
                        if d not in accesibles: # si (d) estado destino no está en los accesibles se agrega
                            accesibles.add(d)
                            alteraciones = True # Se vuelve a iterar el while, pero con conjunto de accesibles alterado (más grande)
            if not alteraciones: 
                break #En este punto ya se recorrió todos los estados accesibles por el estado inicial,
                        #por lo que no hay alteraciones, y para no entrar en bucles infinitos se hace break
        estados_totales = set(self.Q)
        inaccesibles = estados_totales - accesibles #Inaccesibles = Q - Accesibles
        return inaccesibles

    def toString(self):
        #print('instancia vacia?: ', self.instanciaVacia)
        if self.instanciaVacia: return 'Instancia AFD vacía, no se le asignó un archivo o argumentos'
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= list(self.delta[q][simb])[0]
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
                #print ('deltaLinea: ',deltaLinea)
        return out

    def imprimirAFDSimplificado(self):
        pass

    def exportar(self, archivo):
        with open(archivo, "w") as f:
            f.write(self.toString())

    def procesarCadena(self, cadena):   #Procesar cadena con delta como un diccionario
        actual = self.q0
        estados=self.delta.keys()
        for i in cadena:
            if i not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                return False
            if(actual in estados):
                actual = list(self.delta[actual][i])[0] #Realizar transicion 
                pass
            #Nota: no es necesario verificar si la transicion existe en el estado actual, 
            # en el constructor se rellenó con Limbos las transiciones que faltaban en la lectura de las transiciones del archivo,
            # por lo que la clase AFD siempre trabaja con tablas de transiciones completas
        if actual in self.F: #verificar si el estado actual es de aceptacion
            return True
        else:
            return False   
            

    def procesarCadenaConDetalles(self, cadena):
        return True

    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        pass

    def AFD_hallarComplemento(self, afdInput ):
        print("hallando complemento: \n")
        complemento= AFD(afdInput)
        nuevosEstadosF= self.Q.difference(self.F)
        complemento.F=nuevosEstadosF
        return complemento
    @staticmethod
    def AFD_hallarProductoCartesianoY(afd1 , afd2 ):
        pass
    @staticmethod
    def AFD_hallarProductoCartesianoO(afd1 , afd2 ):
        #1. hacer los pares del producto cartesiano usando la libreria itertools
        print('producto cartesiano:\n')
        afd1Q=sorted(list(afd1.Q))
        afd2Q=sorted(list(afd2.Q))
        print('afd1Q: ', afd1Q, '\nafd2Q: ', afd2Q)
        print('afd1 q0: ', afd1.q0, '\nafd2 q0: ', afd2.q0)
        pares =productoCartesiano(afd1Q, afd2Q)
        paresOrdenados=list([(list(p)) for p in pares]) #Lista de listas, los sets() no dejan ordenar, importante ordenar
        print('producto cartesiano Ordenado:\n')
        print(paresOrdenados)
        #2. Hallar los pares que son el resultado de evaluar los ParesOrdenados con delta1 y delta2
        # Al mismo tiempo que se desarrollan los nuevos atributos del nuevo AFD
        # Nota: para cada par (a, b) de paresOrdenados, (a) pertenece afd1, (b) a afd2

        print('\nNuevo AFD:\n')
        nuevoSigma=afd1.Sigma # Ley: ambos deben tener el mismo alfabeto A, por eso basta con que este sigma tambien sea A
        nuevoQ=set()
        nuevoq0=''
        nuevoF=set()
        nuevoDelta={}

        for q1, q2 in paresOrdenados:
            nuevoEstado=f'{q1},{q2}'
            nuevoQ.add(nuevoEstado)
            nuevoDelta.update({nuevoEstado:{}})
            if(q1 in afd1.F or q2 in afd2.F): # UNION: Aqui se usa el OR, en intersección se usaria el AND y en las demás, opreaciones entre conjuntos
                nuevoF.add(nuevoEstado)
            if(q1 == afd1.q0 and q2 == afd2.q0): # Definimos el nuevo estado inicial (q0)
                nuevoq0 =nuevoEstado
                print('estado q0 elegido, es:', nuevoEstado)

            for simbolo in afd1.Sigma.simbolos: 
                qAFD1= list(afd1.delta[q1][simbolo])[0] # qAFD1 = δ(qn, simbolo)
                qAFD2= list(afd2.delta[q2][simbolo])[0]
                print(f'δ(({q1},{q2}),{simbolo}) = (δ1({q1},{simbolo}),δ2({q2},{simbolo})) = ({qAFD1},{qAFD2})')
                nuevoDelta[nuevoEstado][simbolo]={f'{qAFD1},{qAFD2}'}
        print('\nAlfabeto (Sigma) del nuevoAFD: ', nuevoSigma.simbolos)
        print('\nself.Q del nuevo AFD: ', nuevoQ, 'tamaño: ', len(nuevoQ))
        print('\nq0 del nuevoAFD: ', nuevoq0)
        print('\nestados de aceptacion del nuevoAFD: ', nuevoF, 'tamaño: ', len(nuevoF))
        print('\ndelta del nuevoAFD: ', nuevoDelta, '\nTamaño del delta: ', len(nuevoDelta))
        return AFD(nuevoSigma, nuevoQ, nuevoq0, nuevoF, nuevoDelta)

        
    def AFD_hallarProductoCartesianoDiferencia(self, afd1 , afd2 ):
        pass

    def AFD_hallarProductoCartesianoDiferenciaSimétrica(self, afd1 , afd2 ):
        pass

    def AFD_hallarProductoCartesiano(self, afd1 , afd2 , StringOperacion):
        pass

    def AFD_simplificarAFD(self, afdinput ):
        pass

    def pruebas(self, cadena):
        out=''
        #print("usando delta: \n")
        limbo = { 'L':{  s: {'L'} for s in self.Sigma.simbolos} }
        #print('limbo: ', limbo)
        for estado in self.delta:
            for simb in self.Sigma.simbolos:
                if(self.delta[estado].get(simb)==None):
                    self.delta[estado][simb]=limbo
        out = self.toString() #.get() retorna el conjunto del simbolo dado, si no existe retorna un conjunto vacío (esto es para evitar errores de KeyError: clave no encontrada)
        return out

#================================================

#print('real Ejecutando:...\n')

archivo1='impares' # AFD--> L: |w| impar
afd1= AFD(archivo1+'.dfa') 
cadena='aaaba'
print('AFD: ',archivo1, ' Procesar la cadena: ',cadena,'resultado: ',  afd1.procesarCadena(cadena))
afd1.exportar(archivo1+'Exportado.'+afd1.extension)

archivo2='nocontieneBB' #AFD--> L: No contiene bb, que pendejada tan redundante :v
afd2= AFD(archivo2+'.dfa')
cadena='abaaabab'
print('AFD: ',archivo2, ' Procesar la cadena: ',cadena,'resultado: ',  afd2.procesarCadena(cadena))
afd2.exportar(archivo2+'Exportado.'+afd2.extension)

#Producto cartesiano tipo Union
archivo3=f'{archivo1}X{archivo2}' # L: impares Ó que no contengan bb
afd3 = AFD.AFD_hallarProductoCartesianoO(afd1, afd2)
cadena= 'bab'
print('AFD: ',archivo3, ' Procesar la cadena: ',cadena,'resultado: ',  afd3.procesarCadena(cadena))
#afd3.exportar(archivo3+'Exportado.'+afd3.extension)
print('\n#############################################################################')




