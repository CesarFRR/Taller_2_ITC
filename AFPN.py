from Alfabeto import Alfabeto
import re
from Tree import nonBinaryTree, nonBinaryTreePila

class AFPN:
    """
    # Clase AFPN

    Ésta clase modela y simula el Autómata Finito de Pila No determinista AFN el cual puede poseer cero, uno o más transiciónes para un símbolo perteneciente al Alfabeto

    """
    Q = None
    q0 =None
    F =None
    Sigma =None
    PSigma = None
    delta = None
    extension = 'pda'
    etiquetas=['#!pda', '#states', '#initial', '#accepting','#tapeAlphabet', '#stackAlphabet',  '#transitions']
    instanciaVacia=False
    nonPila = {}
    modPila = {}
    pilas = []
    aceptacion = []
    rechazadas = []
    abortadas = []

    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], str)):  # Inicializar por archivo txt
            if (not args[0].endswith("." + self.extension)):raise ValueError("El archivo proporcioando no es de formato ", self.extension)
            #try:
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
                            trans=re.split(r"[:>;]", i)
                            if(len(trans)<5): raise ValueError("transicion invalida: ", i) # "; " q no puede tener varias salidas con un simbolo
                            estado, simbolo, pop = trans[0], trans[1], trans[2]
                            estadoDestino = []
                            push = []
                            for j in range(len(trans[3:])):
                                if j%2 == 0:
                                    estadoDestino.append(trans[j+3]) 
                                else:
                                    push.append(trans[j+3])
                            
                            #print('trans: ', trans)
                            #===================================================================#
                            valor=dictReader.get(estado)
                            #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                            if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                dictReader[estado]={(simbolo, pop):{(i,j) for i,j in zip(estadoDestino, push)}}
                                self.nonPila[estado]= {simbolo: {i for i in estadoDestino}}
                            else:
                                if(dictReader[estado].get(simbolo)==None):
                                    dictReader[estado][(simbolo, pop)]={(i,j) for i,j in zip(estadoDestino, push)}
                                    self.nonPila[estado][simbolo] = {i for i in estadoDestino}
                                else:
                                    dictReader[estado][(simbolo, pop)].add((i,j) for i,j in zip(estadoDestino, push))
                                    self.nonPila[estado][simbolo].add(i for i in estadoDestino)
                
                
                self.Sigma = Alfabeto(afc['#tapeAlphabet'])
                self.PSigma= Alfabeto(afc['#stackAlphabet'])
                self.Q = set(afc['#states'])
                self.q0 = afc['#initial'][0]
                self.F = set(afc['#accepting'])
                self.delta = dictReader
                #print('delta: ', self.delta)
                self.nombreArchivo=((args[0]).split('.'+self.extension))[0]
                
            # except Exception as e:
            #     print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 6):  # Inicializar por los 6 parametros: alfabeto,alfabetoPila estados, estadoInicial, estadosAceptacion, delta
            self.Q, self.q0, self.F,self.Sigma, self.PSigma, self.delta = args
            self.Q=set(self.Q)


    def modificarPila(self, pila: list, operacion: str, parametro: str):
        """Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase."""
        """Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase."""
        simplePar=parametro
        simplePila= ''.join(pila)
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
                    elif(simplePila.count(simplePar)==1 and simplePila.endswith(simplePar)):
                        # Este caso es muy extraño que suceda pero puede suceder:
                        # Si la A (Él parametro) está inicialmente colocada en el fondo de la pila,
                        # entonces la pila se vacía y la unidad de control queda 
                        # escaneando el fondo vacío.
                        pila=[]
                    else:
                        pila.pop()
        elif operacion == 'swap':
            for simb in parametro:
                pila.pop()
                pila.append(simb)
                    
        return True
    
    def recorrerCadena(self,tree):
        cadena = tree.val[2]
        for index, simbolo in enumerate(cadena):
            inserted = False
            if self.delta.get(tree.val[0]) is not None:
                for char, parametro1 in sorted(self.delta[tree.val[0]]):
                    if char == simbolo:
                        for result, parametro2 in sorted(self.delta[tree.val[0]][(char, parametro1)]):
                            pila = tree.val[1]
                            if len(pila) > 0:
                                if parametro1 != '$' and parametro2 != '$':
                                    if parametro1 == pila[-1]:
                                        pila[-1] = parametro2
                                        tree.insert(result, pila, cadena[index+1:])
                                        inserted = True
                                elif parametro1 != '$' and parametro2 =='$':
                                    if parametro1 == pila[-1]:
                                        pila = pila[:-1]
                                        tree.insert(result, pila, cadena[index+1:])
                                        inserted = True
                                    else:break
                                elif parametro1 == '$' and parametro2 != '$':
                                    
                                    pila+=parametro2
                                    tree.insert(result, pila, cadena[index+1:])
                                    inserted = True
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, pila, cadena[index+1:])
                                    inserted = True
                            else:
                                if parametro1 == '$' and parametro2 != '$':
                                    pila+=parametro2
                                    tree.insert(result, pila, cadena[index+1:])
                                    inserted = True
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, pila, cadena[index+1:])
                                    inserted = True
                        if inserted == True:    
                            for child in tree.children:
                                self.recorrerCadena(child)
                    elif char == '$':
                        for result, parametro2 in sorted(self.delta[tree.val[0]][(char, parametro1)]):
                            pila = tree.val[1]
                            if len(pila) > 0:
                                if parametro1 != '$' and parametro2 != '$':
                                    if parametro1 == pila[-1]:
                                        pila[-1] = parametro2
                                        tree.insert(result, pila, cadena[index:])
                                        inserted = True
                                elif parametro1 != '$' and parametro2 =='$':
                                    if parametro1 == pila[-1]:
                                        
                                        pila = pila[:-1]
                                        tree.insert(result, pila, cadena[index:])
                                        inserted = True
                                    
                                elif parametro1 == '$' and parametro2 != '$':
                                    pila+=parametro2
                                    tree.insert(result, pila, cadena[index:])
                                    inserted = True
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, pila, cadena[index:])
                                    inserted = True
                            else:
                                if parametro1 == '$' and parametro2 != '$':
                                    pila+=parametro2
                                    tree.insert(result, pila, cadena[index:])
                                    inserted = True
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, pila, cadena[index:])
                                    inserted = True

                        if inserted == True:    
                            for child in tree.children:
                                self.recorrerCadena(child)
                    
                else:
                    break
            else:
                break
            

    def procesamiento(self,cadena):
        pila = ''
        tree = nonBinaryTreePila(self.q0, pila, cadena)
        self.rutas = []
        
        pila = self.recorrerCadena(tree)
        

        self.rutas = tree.recorrer(tree)
        for ruta in self.rutas:
            if ruta[-1][2] == '':
                if ruta[-1][1] == '':
                    if ruta[-1][0] in self.F:
                        if ruta not in self.aceptacion:
                            self.aceptacion.append(ruta)
                    else:
                        if ruta not in self.rechazadas:
                            self.rechazadas.append(ruta)
                else:
                    if ruta not in self.rechazadas:
                        self.rechazadas.append(ruta)
            else:
                if ruta not in self.abortadas:
                    self.abortadas.append(ruta)

        if len(self.aceptacion) > 0:
            return self.aceptacion[0]
        return None
        # print('aceptacion \n',self.aceptacion) 
        # print('rechazadas \n',self.rechazadas)           
        # print('abortadas \n',self.abortadas)           

        #print(tree)

    def procesarCadena(self, cadena):
        """ procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata. """
        aceptada = self.procesamiento(cadena)
        if aceptada is not None:
            return True
        return False
    def procesarCadenaConDetalles(self, cadena):
        """realiza  lo  mismo  que  el  método  anterior aparte  imprime  losdetalles  del  procesamiento  con  el  formato  que se  indica  en  el  archivo AFPD.pdf."""
        return True
    def  computarTodosLosProcesamientos(cadena,  nombreArchivo):  
        """Debe  imprimir  cada  uno de los posibles procesamientos de acuerdo al formato establecido en el archivo AFPN.pdfe indicando si al final de cada procesamiento se llega a aceptación o rechazo. Debe llenar una lista  de  todos  procesamientos  de  aceptación,  una  lista  de  todos  los  procesamientos rechazados.  Debe  guardar  los  contenidos  de  estas  listas  cada  una  en  un  archivo(cuyos nombres  son  nombreArchivoAceptadasAFPN.txtynombreArchivoRechazadasAFPN.txt)  y además imprimirlas en pantalla. Se debe retornar el número de procesamientos realizados."""
        return 0
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.  Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son: 
        1. cadena, 
        2. un procesamientode aceptación (si lo hay, si no unode rechazo), 
        3. número de posibles procesamientos 
        4. número de procesamientos de aceptación 
        5. número de procesamientos de rechazo 
        6. “yes”o “no”dependiendo de si la cadena es aceptada o no."""
        pass

    def hallarProductoCartesianoConAFD(afd):
        """: debe calcular y retornar el producto cartesiano con un AFD dado como parámetro."""
        pass

    def toString(self, graficar:bool = False):
        """Representar  el  AFPNcon  el  formato  de  los  archivos  de  entrada  de  AFPN (AFPN.pdf) de manera que se pueda imprimir fácilmente."""
        if self.instanciaVacia: return 'Instancia AFD vacía, no se le asigno un archivo o argumentos'
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] + '\n'+ '\n'.join(sorted(list(self.Q)))+ '\n'+self.etiquetas[2]+'\n'+self.q0+'\n'+self.etiquetas[3] + '\n'.join(sorted(list(self.F)))+  '\n'+self.etiquetas[4]+'\n'+self.Sigma.toStringEntrada()+ '\n'+ self.etiquetas[5]+ '\n'+ self.PSigma.toStringEntrada()+'\n'+self.etiquetas[6]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= list(self.delta[q][simb])
                deltaLinea = f'{q}:{simb[0]}:{simb[1]}>'
                for i in deltaSet:
                    deltaLinea+= f'{i[0]}:{i[1]};'
                deltaLinea = deltaLinea.rstrip(deltaLinea[-1])
                out+='\n'+deltaLinea
                #print ('deltaLinea: ',deltaLinea)
        if graficar:
            self.gra
        return out
    
        pass

#----------------------------------------------------------------

pda1 = AFPN('ej2.pda')
print(pda1.procesarCadena('aaabbbbbbbbbcccccc'))