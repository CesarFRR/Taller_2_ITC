from AFD import AFD
from Alfabeto import Alfabeto
from Graph import graficarAutomata
from prettytable import PrettyTable, ALL
import re
from Tree import nonBinaryTree
#from visual_automata.fa.nfa import VisualNFA

class AFN:
    """
    # Clase AFN

    Ésta clase modela y simula el Autómata Finito No determinista AFN el cual puede poseer cero, uno o más transiciónes para un símbolo perteneciente al Alfabeto

    """
    Sigma = None
    Q = None
    q0 = None
    F = None
    delta = {}
    estadosLimbo = None
    estadosInaccesibles = None
    automata_tipo = "nfa"
    etiquetas=['#!nfa', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
    nombreArchivo=''
    extension = "nfa"
    aceptacion = []
    rechazadas = []
    abortadas = []
    deltaParaGraficar={}
    rutas = []
    def __init__(self, *args):
        """Este único constructor utiliza artificios de python para simular sobrecarga de constructores ya que python no tiene esa característica, como resultado se puede instanciar una clase AFN de las siguientes maneras:

        >>> AFN('nombreDeArchivo.nfa')
        # Lee un archivo de entrada afn.
        
        >>> AFN(alfabeto, estados: set, estadoInicial, estadosAceptacion,Delta)
        # Recibe los 5 atributos del autómata
        
        

        
        """
        if (len(args) == 1):  # Inicializar por archivo txt
            if (not args[0].endswith("." + self.automata_tipo)):
                raise ValueError(
                    "El archivo proporcioando no es de formato ", self.automata_tipo)
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
                        elif i != '':
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions' and i.split(":")[1].split(">")[0]!= "$": # AFN: no contiene transiciones lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3): raise ValueError("transicion invalida: ", i)
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
                    self.deltaParaGraficar=dictReader.copy()
                    self.nombreArchivo=((args[0]).split('.'+self.extension))[0]
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            simbolos, self.Q, self.q0, self.F, self.delta = args
            if(isinstance(simbolos, Alfabeto)):
                self.Sigma=simbolos
            else:
                self.Sigma=Alfabeto(simbolos)
            self.Q=set(self.Q)
            self.F=set(self.F)
        
        self.estadosInaccesibles= self.hallarEstadosInaccesibles()
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

    def toString(self, graficar:bool=False):
        """método para imprimir donde se vean los estados, estado inicial, estados de aceptación, estados inaccesibles, y tabla de transiciones."""
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ '#inaccesible' + '\n' + '\n'.join(sorted((list(self.estadosInaccesibles)))) + '\n' +self.etiquetas[5]+'\n'
        deltaLinea=''
        for q in sorted(self.delta.keys()):
            for simb in self.delta[q]:
                deltaSet= sorted(list(self.delta[q][simb]))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        if(graficar):
            self.graficarAutomata()
        return out

    def imprimirAFNSimplificado(self): #Similar al anterior sin estados inaccesibles
        """método para imprimir donde se vean los estados, estado inicial, estados de aceptación,y tabla de transiciones. No se deben mostrar los estados inaccesibles."""
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q.difference(self.estadosInaccesibles))))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F.difference(self.estadosInaccesibles))))+'\n'+self.etiquetas[5]
        deltaLinea=''
        for q in self.delta:
            if(q in self.estadosInaccesibles):
                continue
            for simb in self.delta[q]:
                deltaSet= sorted(list(self.delta[q][simb]))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        return out

    def exportar(self, archivo):
        """Guardar el autómata en un archivo con el formatoespecificado """
        with open(f'./archivosSalida/{archivo}', "w") as f:
                f.write(self.toString())

    def AFNtoAFD(self, afn1, imprimir = True):
        """ recibe un AFN y retorna el AFD equivalente. Debe imprimir la tabla que muestra los estados (antiguos y nuevos) con las transiciones definidas para cada símbolo del alfabeto. Debe eliminar los estados inaccesibles (a través de un método de la clase AFD)"""
        states = list(afn1.Q).copy()
        delta = afn1.delta.copy()
        accepting= afn1.F.copy()

        for state, transitions in delta.items():
            for symbol, destiny in transitions.items():
                if len(destiny)>1:           #Comprobar si un simbolo lleva a mas de un estado
                    states.append(tuple(destiny))    #Agregar tupla de todos los estados a los que lleva

        #Recorrer lista de estados una vez realizadas las modificaciones anteriores
        for estado in states:
            transitions = dict()    #diccionario con transiciones para los nuevos estados
            if type(estado) is tuple:       #Verificar que el estado actual sea una tupla
                for state in estado:
                    if len(state) > 1 and afn1.delta.get(state) is not None:      #Verificar que la tupla contenga mas de un elemento    
                        for symbol in afn1.delta.get(state):                      #Verificar transiciones de cada simbolo con cada estado de la tupla             
                            if transitions.get(symbol) is not None:              #Si ya se agregaron las transiciones de uno de los estados, actualizar con las de los demas
                                transitions.update({str(symbol):set(sorted(set(transitions[symbol]).union(delta[state][symbol])))})
                            else:                                                #Aun no se han agregado las transiciones de ningun estado
                                transitions.update({str(symbol):set(sorted(delta[state][symbol]))})

                delta.update({estado:transitions})

                #Agregar los estados que vayan surgiendo durante el proceso
                for symbol in delta.get(estado):            
                    newState = tuple(delta[estado][symbol].copy())
                    if newState not in states and len(newState)>1:
                        states.append(newState)
        strStates = set()
        for state in states:        #Agregar todos los estados que contengan alguno de aceptacion
            if type(state) is tuple:
                x = '{'+','.join(sorted(list(state)))+'}'     
                strStates.add(f'{x}')     #Convertir tupla a string
                for i in state:
                    if i in afn1.F:
                        accepting.add(f'{x}')
            else:
                strStates.add(f'{state}')
        strDelta = dict()
        for estado, transitions in delta.items():
            
            #print('transiciones y tipo: ', transitions, type(transitions.get('a')))    #Cambiar keys del diccionario por strings
            x = '{'+','.join(sorted(list(estado)))+'}' if type(estado) is tuple else estado
            strDelta[f'{x}'] = { simb: dict() for simb in sorted(delta[estado].keys()) }
            for simb, trans in delta[estado].items():
                strTrans=None
                if(len(trans)>1):
                    strTrans = '{'+','.join( (sorted(list(trans))) )+'}'
                    strTrans= {strTrans}
                else: 
                    strTrans=trans
                strDelta[f'{x}'][simb]=strTrans

        afd1= AFD(afn1.Sigma, strStates, afn1.q0, set(accepting), strDelta)
        afd1.nombreArchivo=afn1.nombreArchivo+'ToAFD'
        #Imprimir tabla de trancisiones
        #print(afd1.toString())
        if imprimir:
            tabla = PrettyTable()
            # Agregar encabezados
            estados=sorted(list(afd1.Q))
            simbolos=sorted(afd1.Sigma.simbolos)
            #print('estados: ', estados, '\nsimbolos: ', simbolos)
            tabla.field_names = ["Δ"] + simbolos
            for q in estados:
                if(afd1.delta.get(q)==None):
                    continue
                fila=[q]
                for simb in simbolos:
                    trans=list(afd1.delta[q].get(simb, ['∅']))
                    fila.append(trans[0])
                tabla.add_row(fila)
            print(tabla)

        return  afd1 #Retornar AFD equivalente
    
    def recorrerCadena(self, cadena, tree):
        for index, simbolo in enumerate(cadena):
            if self.delta.get(tree.val) is not None:
                if self.delta[tree.val].get(simbolo) is not None:
                    for i in sorted(self.delta[tree.val][simbolo]):
                        tree.insert(i)
                    for child in tree.children:
                        self.recorrerCadena(cadena[index+1:], child)
                    return 0
                    
                else:
                    break
            else:
                break

    def procesamiento(self, cadena, rutas = None): #cadena: str, actual, detalles, proc,  out=''
        """Función encargada del procesamiento teniendo en cuenta todos los caminos posibles cuando se está en (  q  ) estado y se va a consumir 'a' simbolo, se tendrán en cuenta las {a + lambda} transiciones"""
        self.rutas = []
        self.aceptacion = []
        self.abortadas = []
        self.rechazadas = []
        
        if rutas is None:
            rutas = nonBinaryTree(self.q0)

        self.recorrerCadena(cadena, rutas)#crear todos los procesamientos
        self.rutas = rutas.recorrer(rutas) #recorrer los procesamientos y almacenarlos
        for procesamiento in self.rutas:    #Calsificar los procesamientos
            if type(procesamiento) == list:
                
                if len(procesamiento) == len(cadena)+1:
                    if procesamiento[-1] in self.F:
                        out = ''
                        for estado, (index, simbolo) in zip(procesamiento, enumerate(cadena)):
                            out += f'[{estado},{cadena[index:]}]->'
                        out+='Aceptacion'
                        if out not in self.aceptacion:
                            self.aceptacion.append(out)
                    else:
                        out = ''
                        for estado, (index, simbolo) in zip(procesamiento, enumerate(cadena)):
                            out += f'[{estado},{cadena[index:]}]->'
                        out+='No aceptacion'
                        if out not in self.rechazadas:
                            self.rechazadas.append(out)
                else:
                    out = ''
                    for estado, index in zip(procesamiento, range(len(procesamiento))):
                        out += f'[{estado},{cadena[index:]}]->'
                    out+='Procesamiento Abortado'
                    if out not in self.abortadas:
                        self.abortadas.append(out)
            elif type(procesamiento) == str:
                if len(procesamiento) == len(cadena)+1:
                    if procesamiento[-1] in self.F:
                        out = ''
                        out += f'[{procesamiento},{cadena}]->'
                        out+='Aceptacion'
                        if out not in self.aceptacion:
                            self.aceptacion.append(out)
                    else:
                        out = ''
                        out += f'[{procesamiento},{cadena}]->'
                        out+='No aceptacion'
                        if out not in self.rechazadas:
                            self.rechazadas.append(out)
                else:
                    out = ''
                    out += f'[{procesamiento},{cadena}]->'
                    out+='Procesamiento Abortado'
                    if out not in self.abortadas:
                        self.abortadas.append(out)

        rutas.children = []

        if len(self.aceptacion) > 0:
            return self.aceptacion[0]
        else:
            return None
        
    def procesarCadena(self, cadena):
        """procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata"""
        aceptada = self.procesamiento(cadena)
        if aceptada is not None:
            return True
        return False

    def procesarCadenaConDetalles(self, cadena):
        """realiza lo mismo que el método `procesarCadena()` pero aparte imprime los estados que va tomando al procesar cada símbolo de uno de los procesamientos que lleva a la cadena a ser aceptada. """
        aceptada = self.procesamiento(cadena)
        if aceptada is not None:
            print(aceptada)
            return True
        return False

    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        """Debe imprimir cada uno de los posibles procesamientos de la cadena indicando de qué estado a qué estado pasa al procesar cada símbolo e indicando si al final de cada procesamiento se llega a aceptación o rechazo. Debe llenar una lista de todos procesamientos de aceptación, una lista de todos los procesamientos abortados y una lista de todos los procesamientos de rechazo. Debe guardar los contenidos de estas listas cada una en un archivo(cuyos nombres son nombreArchivoAceptadas.txt, nombreArchivoRechazadas.txt y nombreArchivoAbortadas.txt) y además imprimirlas en pantalla. Se debe retornar el número de procesamientos realizados."""

        self.aceptacion = []
        self.rechazadas = []
        self.abortadas = []
        self.procesamiento(cadena)

        with open(f'./archivosSalida/{nombreArchivo}Abortadas.txt', 'a') as abortadas:
            abortadas.truncate(0)
            for procesamiento in self.abortadas:
                abortadas.write(f'{procesamiento}\n')
                print(f'{procesamiento}')
        with open(f'./archivosSalida/{nombreArchivo}Rechazadas.txt', 'a') as rechazadas:
            rechazadas.truncate(0)
            for procesamiento in self.rechazadas:
                rechazadas.write(f'{procesamiento}\n')
                print(f'{procesamiento}')
        with open(f'./archivosSalida/{nombreArchivo}Aceptadas.txt', 'a') as aceptadas:
            aceptadas.truncate(0)
            for procesamiento in self.aceptacion:
                aceptadas.write(f'{procesamiento}\n')
                print(f'{procesamiento}')

        return len(self.aceptacion+self.rechazadas+self.abortadas)

    def procesarListaCadenas(self, listaCadenas: list, nombreArchivo: str, imprimirPantalla:bool):
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por defecto. Además,todo esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son: ▪cadena, ▪sucesión de parejas (estado, símbolo) de cada paso del procesamientomás corto de aceptación (si lo hay, si no el más corto de rechazo)
        
        1. número de posibles procesamientos
        2. número de procesamientos de aceptación
        3. número de procesamientos abortados
        4. número de procesamientos de rechazo
        5. sí o no dependiendo de si la cadena es aceptada o no."""
        try:
            with open(f'./archivosSalida/{nombreArchivo}.txt', 'a') as archivo:
                archivo.truncate(0)
        except:
            nombreArchivo= 'procesarListaCadenas_AFN'
            with open(f'./archivosSalida/{nombreArchivo}.txt', 'a') as archivo:
                archivo.truncate(0)

        with open(f'./archivosSalida/{nombreArchivo}.txt', 'a') as archivo:
            for cadena in listaCadenas:
                self.procesamiento(cadena)
                archivo.write(f'{cadena}\n')
                try:
                    archivo.write(f'{self.aceptacion[0]}\n')
                except:
                    try:
                        archivo.write(f'{self.rechazadas[0]}\n')
                    except:
                        archivo.write(f'{self.abortadas[0]}\n')
                archivo.write(f'Numero de procesamientos\n{len(self.aceptacion+self.rechazadas+self.abortadas)}\n')
                archivo.write(f'Numero de procesamientos de aceptacion\n{len(self.aceptacion)}\n')
                archivo.write(f'Numero de procesamientos abortados\n{len(self.abortadas)}\n')
                archivo.write(f'Numero de procesamientos rechazados\n{len(self.rechazadas)}\n')
                if len(self.aceptacion)>=1:
                    archivo.write('Si\n\n')
                else:
                    archivo.write('No\n\n')

        if imprimirPantalla:
            with open(f'./archivosSalida/{nombreArchivo}', 'r') as archivo:
                for line in archivo:
                    print(line)

    def procesarCadenaConversion(self, cadena):
        """procesa la cadena, haciendo una previa conversión a AFD, y retorna verdadero si es aceptada y falso si es rechazada por el autómata."""
        afd = self.AFNtoAFD(self, False)
        return afd.procesarCadena(cadena)
    
    def  procesarCadenaConDetallesConversion(self, cadena):
        """realiza lo mismo que el método `procesarCadenaConversion()` pero aparte imprime los estados (del AFD) que va tomando al procesar cada símbolo"""
        afd = self.AFNtoAFD(self, False)
        return afd.procesarCadenaConDetalles(cadena) 

    
    def procesarListaCadenasConversion(self, listaCadenas,nombreArchivo, imprimirPantalla):
        """rocesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por defecto.Además todo esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla. Los campos deben estar separados por tabulación y son:
 1. cadena
 2. sucesión de parejas (estado, símbolo) de cada paso del procesamiento
 3. sí o no dependiendo de si la cadena es aceptada o no."""

        afd = self.AFNtoAFD(self, False)
        return afd.procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla)
    

    def graficarAutomata(self):
        """Grafica el automata usando librerias de matplotlib y NetworkX"""
        graficar = graficarAutomata()
        graficar.mostrarGrafo(self)

#================================================

#print('Ejecutando:...\n')
# nfa1= AFN("ej1.nfa")
# #print(nfa1.computarTodosLosProcesamientos('bbbabababac','AFNprocesamientos'))
# #print(nfa1.procesarListaCadenas(['aab','bbcba', 'babbbcbb', 'bbccbab'], 'ProcesarLista', False))
# # # nfa1.graficarAFN()
# # dfa1 = nfa1.AFNtoAFD(nfa1)
# # nfe1= AFN_Lambda('ej1.nfe').AFN_LambdaToAFD()
# dfa1 = nfa1.AFNtoAFD(nfa1)
# print(nfa1.toString())
# #print(nfa1.delta)
# print(dfa1.toString())
#print(nfa1.toString())
# print('\n')

#print(nfa1.toString())
#print('\n')
#nfa1.exportar('ej2.nfa')
