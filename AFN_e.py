from AFN import AFN
from Alfabeto import Alfabeto
from Graph import graficarAutomata
import re
class AFN_Lambda:
    """
    # Clase AFN_Lambda

    Ésta clase modela y simula el Autómata Finito No determinista con transiciones lambda AFNe también conocido como AFN epsilon o lambda el cual puede poseer cero, uno o más transiciónes para un símbolo perteneciente al Alfabeto además de las transiciones lambda

        >>> AFD('nombreDeArchivo.nfa')
        # Lee un archivo de entrada afn lambda.
        
        >>> AFD(alfabeto: Alfabeto, estados: set, estadoInicial: str, estadosAceptacion: set, Delta: dict)
        # Recibe los 5 atributos del autómata
    """
    Sigma=None
    Q=None
    q0=None
    F=None
    delta = {}
    estadosLimbo = None
    estadosInaccesibles = None
    automata_tipo = "nfe"
    etiquetas=['#!nfe', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
    nombreArchivo=''
    extension = "nfe"
    aceptacion = []
    rechazadas = []
    abortadas = []
    recount=None
    def __init__(self, *args):
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
                            elif key== '#transitions':  # transiciones, si pueden contener $ (lambda), esto es AFN-lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3): raise ValueError("transicion invalida: ", i)
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
                    self.nombreArchivo=((args[0]).split('.'+self.extension))[0]
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
            self.F=set(self.F)
        self.Sigma.simbolos.append('$')
        self.estadosInaccesibles= self.hallarEstadosInaccesibles()
        self.recount=0

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
        """método para imprimir donde se vean los estados, estado inicial, estados de aceptación, estados inaccesibles, y tabla de transiciones. El formato debe ser el adjunto acá (Formato de Entrada.pdf).Se darán puntos adicionales si se muestra el grafo, (Se puede gaficar con el bool graficar= True)."""
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for Q in self.delta:
            for simb in self.delta[Q]:
                deltaSet= sorted((list(self.delta[Q][simb])))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{Q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        
        if graficar:
            self.graficarAutomata()
        return out
    def imprimirAFNLSimplificado(self, graficar: bool=False)-> str:
        """método para imprimir donde se vean los estados, estado inicial, estados de aceptacióny tabla de transiciones. No se deben mostrar los estados inaccesibles.El formato debe ser el adjunto acá (Formato de Entrada.pdf).Se darán puntos adicionales si se muestra el grafo (Se puede con graficar = True)"""
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

    def exportar(self, archivo: str):
        """Guardar el autómata en un archivo con el formato especificado (Formato de Entrada.pdf)"""
        with open(f'./archivosSalida/{archivo}.{self.extension}', "w") as f:
            f.write(self.toString())

    def l_clausura(nfe1, states):
        """Versión simplificada de lambda_clausura() hecha específicamente para modular/reutilizar codigo y lograr realizar la función de imprimir las cadenas clausura"""
        clausura = set(states)
        while True:
            # Para cada estado en clausura, añade todos los estados que se pueden alcanzar mediante transiciones lambda.
            new_states = set()
            new_states = set(state for s in clausura for state in nfe1.delta[s].get('$', set()))
            # Si no se añadieron nuevos estados, detiene el bucle.
            if new_states.issubset(clausura):
                break
            # Añade los nuevos estados a clausura.
            clausura = clausura.union(new_states)
        return clausura
    
    def lambda_clausura(nfe1, states, imprimir=False):
        """recibe un AFN-λy retorna el AFN equivalente. Debe imprimir laλ-clausura de cada estado y la definición de cada transición incluyendo todos los pasos del procesamiento"""
        out=''
        states = sorted(states)
        clausura = set(states)
        strClausura=[[f'λ[{q}]', set()] for q in states]
        for index, s in enumerate(clausura):
            strClausura[index][1] |=AFN_Lambda.l_clausura(nfe1, {s})
        for cl in strClausura:
            out+=cl[0]+' = '+ '{'+','.join(sorted(list(cl[1])))+'}' +'\n'
        for index,q in enumerate(states):
            for simb in nfe1.Sigma.simbolos:
                if(simb=='$'): continue
                estadosDestino =[nfe1.delta[estado].get(simb, set()) for estado in states]
                estadosDestino= sorted(list(set().union(*estadosDestino)))
                clausuraEstadosDest = sorted(list(AFN_Lambda.l_clausura(nfe1, estadosDestino)))
                clausuraEstadosDest = '∅' if clausuraEstadosDest is None or not clausuraEstadosDest else '{'+','.join(clausuraEstadosDest)+'}'
                out+=f"d'({q},{simb}) = λ[d({strClausura[index][0]},{simb})] =λ[d({'{'+','.join(sorted(list(strClausura[index][1])))+'}' if strClausura[index][1] else '∅'},{simb})] = λ[{'{'+','.join(estadosDestino)+'}' if estadosDestino else '∅'}] = {clausuraEstadosDest}\n"
        if imprimir:
            print(out)
        return clausura if type(clausura) ==set else set(*clausura)

    def AFN_LambdaToAFN(self, nfe1=None, imprimir=True):
        """recibe un AFN-λy retorna el AFN equivalente. Debe imprimir laλ-clausura de cada estado y la definición de cada transición incluyendo todos los pasos del procesamiento"""
        if(nfe1==None):
            nfe1=self
        # Copia Sigma, Q, q0 y F desde afnl, pero elimina el símbolo '$' de Sigma.
        Sigma = [s for s in nfe1.Sigma.simbolos if s!='$']
        Q = nfe1.Q
        q0 = nfe1.q0
        F = set()
        delta = {}

        # Calcula la función de transición para el AFN.
        for state in Q:
            delta[state] = {}
            for symbol in Sigma:
                next_states = set()
                for target in nfe1.delta[state].get(symbol, set()):
                    next_states |= (AFN_Lambda.lambda_clausura(nfe1, {target}, imprimir))
                if(len(next_states)==0):
                    continue
                delta[state][symbol] = next_states

        # Actualiza los estados de aceptación para el AFN.
        for state in sorted(list(Q)):
            # Si un estado puede llegar a un estado de aceptación a través de transiciones lambda, se convierte en un estado de aceptación.
            if not nfe1.F.isdisjoint(AFN_Lambda.lambda_clausura(nfe1, {state}, imprimir=True)):
                F.add(state)

        return AFN(Sigma, Q, q0, F, delta)

    def AFN_LambdaToAFD(self, nfe1=None, imprimir=False):
        """recibe un AFN-λ y retorna el AFD equivalente. imprime las tablas y cálculos especificados para los dos procesos que se harán anf_lambda --> afn y luego afn --> afd,  separando claramente las dos fases de la conversión"""
        if nfe1==None:
            nfe1=self
        print('convirtiendo AFN_lambda --> AFN:\n')
        afn = self.AFN_LambdaToAFN(nfe1, imprimir)
        print('convirtiendo AFN --> AFD:\n')
        afd = afn.AFNtoAFD(afn, imprimir)
        return afd


    def procesamiento(self,cadena: str, actual, detalles, proc,  out='')-> bool:
        """Código 'núcleo' del procesamiento de cadenas para el AFN_lambda, modulado y reutilizado para cada tipo de procesamiento"""
        if(self.recount>300):
            return False
        else:
            self.recount+=1
        try:
            final = False
            breaked = False
            #print('Estado actual: ', actual)
            for index, char in enumerate(cadena):
                if char not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                    out += f'[{actual},{cadena[index:]}]-> Procesamiento abortado'
                    if out not in self.abortadas:
                        self.abortadas.append(out)
                    break
                if(actual in self.Q):
                    if self.delta.get(actual) is not None:
                        if '$' in self.delta[actual].keys():
                            if len(list(self.delta[actual]['$'])) > 1:
                                out += f'[{actual},{cadena[index:]}]-> '
                                transLambda= list(self.delta[actual]['$'])
                                for i in sorted(transLambda):
                                    #print(sorted(self.delta[actual][char]))
                                    #print('Estado actual: ', actual, 'i:  ', i)
                                    if(actual==i):
                                        continue
                                    
                                    actual = i
                                    try:
                                        procesamiento = self.procesamiento(cadena[index:], i, detalles, proc, out)
                                    except:
                                        return False
                                    if proc:
                                        if procesamiento:
                                            return True

                            elif len(list(self.delta[actual]['$'])) == 1:
                                out += f'[{actual},{cadena[index:]}]-> '
                                actual = list(self.delta[actual]['$'])[0]

                        if self.delta.get(actual).get(char) is not None:
                            if len(list(self.delta[actual][char])) > 1:
                                out += f'[{actual},{cadena[index:]}]-> '
                                for i in sorted(self.delta[actual][char]):
                                    # print(sorted(self.delta[actual][char]))
                                    actual = i
                                    procesamiento = self.procesamiento(cadena[index+1:], i, detalles, proc, out)
                                    if proc:
                                        if procesamiento:
                                            return True

                            elif len(list(self.delta[actual][char])) == 1:
                                out+= f'[{actual},{cadena[index:]}]-> '
                                actual = list(self.delta[actual][char])[0]
                        else:
                            out+= f'[{actual},{cadena[index:]}]-> '
                            breaked = True
                            break
                if index == len(cadena)-1:
                    final = True

            if actual in self.F and final: #verificar si el estado actual es de aceptacion
                out+= f'[{actual},]-> '
                out+= 'Aceptacion'
                if out not in self.aceptacion:
                    self.aceptacion.append(out)
                if proc:
                    if detalles:
                        print(out)
                    return True

            elif actual not in self.F:
                out+= f'[{actual},]-> '
                out+= 'No aceptacion'
                if out not in self.rechazadas:
                    self.rechazadas.append(out)
                if proc:
                    return False

            elif breaked is True:
                out+= 'Procesamiento abortado'
                if out not in self.abortadas:
                    self.abortadas.append(out)
                if proc:
                    return False
            if proc:
                return False
        except:
            return False
    def procesar_cadena_afn_lambda(self, cadena):
        delta= self.delta
        estado_inicial=self.q0
        estados_aceptacion=self.F
        estados_actuales = set(estado_inicial)  # Conjunto de estados actuales
        estados_visitados = set()  # Conjunto de estados visitados
        
        for simbolo in cadena:
            nuevos_estados = set()  # Conjunto de nuevos estados alcanzados
            
            # Consultar transiciones regulares
            for estado in estados_actuales:
                if simbolo in delta.get(estado, {}):
                    nuevos_estados |= delta[estado].get(simbolo, set())  # Unión de estados alcanzados
                    print(delta[estado].get(simbolo, set()))
            
            # Consultar transiciones lambda
            while True:
                nuevos_estados_lambda = set()  # Conjunto de nuevos estados alcanzados por transiciones lambda
                
                for estado in sorted(list(estados_actuales)):
                    if not delta.get(estado, {}): continue
                    if '$' in delta[estado].keys():
                        nuevos_estados_lambda |= delta[estado].get('$', set())  # Unión de estados alcanzados por transiciones lambda
                
                nuevos_estados_lambda -= estados_visitados  # Excluir estados visitados previamente
                
                if not nuevos_estados_lambda:
                    break  # No hay nuevos estados alcanzados por transiciones lambda
                
                estados_actuales |= nuevos_estados_lambda  # Agregar nuevos estados alcanzados por transiciones lambda
                estados_visitados |= nuevos_estados_lambda  # Marcar nuevos estados como visitados
            
            estados_actuales = nuevos_estados  # Actualizar estados actuales
        
        # Verificar si algún estado actual es un estado de aceptación
        if estados_actuales & estados_aceptacion:
            return True  # Cadena aceptada
        else:
            return False  # Cadena rechazada


    def procesarCadena(self, cadena: str)-> bool:
        """procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata. """
        aceptada=None
        try:
            aceptada= self.procesamiento(cadena, self.q0, False, True)
        except:
            aceptada=False
        return  aceptada

    def procesarCadenaConDetalles(self, cadena: str)-> bool:
        """realiza lo mismo que el método procesarCadena() pero aparte imprime los estados que va tomando al procesar cada símbolo de uno de los procesamientos que lleva a la cadena a ser aceptada."""
        return self.procesamiento(cadena, self.q0, True, True)

    def computarTodosLosProcesamientos(self, cadena: str, nombreArchivo: str)-> int:
        """Debe imprimir cada uno de los posibles procesamientos de la cadena indicando de qué estado a qué estado pasa al procesar cada símbolo e indicando si al final de cada procesamiento se llega a aceptación o rechazo. Debe llenar una lista de todos procesamientos de aceptación, una lista de todos los procesamientos abortados y una lista de todos los procesamientos de rechazo. Debe guardar los contenidos de estas listas cada una en un archivo(cuyos nombres son nombreArchivoAceptadas.txt, nombreArchivoRechazadas.txt y nombreArchivoAbortadas.txt) y además imprimirlas en pantalla. Se debe retornar el número de procesamientos realizados."""
        self.aceptacion = []
        self.rechazadas = []
        self.abortadas = []
        self.procesamiento(cadena, self.q0, False, '')

        with open(f'./archivosSalida/{nombreArchivo}Abortadas_AFNe.txt', 'a') as abortadas:
            abortadas.truncate(0)
            for i in self.abortadas:
                abortadas.write(f'{i}\n')
                print(f'{i}')
        with open(f'./archivosSalida/{nombreArchivo}Rechazadas_AFNe.txt', 'a') as rechazadas:
            rechazadas.truncate(0)
            for i in self.rechazadas:
                rechazadas.write(f'{i}\n')
                print(f'{i}')
        with open(f'./archivosSalida/{nombreArchivo}Aceptadas_AFNe.txt', 'a') as aceptadas:
            aceptadas.truncate(0)
            for i in self.aceptacion:
                aceptadas.write(f'{i}\n')
                print(f'{i}')

        return len(self.aceptacion + self.rechazadas + self.abortadas)

    def procesarListaCadenas(self, listaCadenas: list,nombreArchivo: str='', imprimirPantalla: bool=False):
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por defecto. Además,todo esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son:
       
        1. cadena
        2. sucesión de parejas (estado, símbolo) de cada paso del procesamientomás corto de aceptación (si lo hay, si no el más corto de rechazo)
        3. número de posibles procesamientos
        4. número de procesamientos de aceptación
        5. número de procesamientos abortados.
        6. número de procesamientos de rechazo
        7. sí o no dependiendo de si la cadena es aceptada o no."""
        try:
            with open(f'./archivosSalida/{nombreArchivo}.txt', 'a') as archivo:
                archivo.truncate(0)
        except:
            nombreArchivo= 'procesarListaCadenas_AFNe'
            with open(f'./archivosSalida/{nombreArchivo}.txt', 'a') as archivo:
                archivo.truncate(0)
        try:
            with open(f'./archivosSalida/{nombreArchivo}.txt', 'a') as archivo:
                for cadena in listaCadenas:
                    self.aceptacion = []
                    self.rechazadas = []
                    self.abortadas = []
                    actual = self.q0
                    self.procesamiento(cadena, actual, True, True)

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
        except:
            pass
        if imprimirPantalla:
            with open(f'./archivosSalida/{nombreArchivo}.txt', 'r') as archivo:
                for line in archivo:
                    print(line)

    def procesarCadenaConversion(self, cadena: str)-> bool:
        """procesa la cadena, haciendo una previa conversión a AFD, y retorna verdadero si es aceptada y falso si es rechazada por el autómata."""
        afd1= self.AFN_LambdaToAFD(self, imprimir=False)
        return afd1.procesarCadena(cadena)

    def procesarCadenaConDetallesConversion(self, cadena: str)-> bool:
        """realiza lo mismo que el método procesarCadenaConversion() pero aparte imprime los estados (del AFD) que va tomando al procesar cada símbolo"""
        afd1 = self.AFN_LambdaToAFD(self, imprimir=False)
        return afd1.procesarCadenaConDetalles(cadena)

    def procesarListaCadenasConversion(self, listaCadenas: list,nombreArchivo: str, imprimirPantalla: bool):
        """Convierte ésta instancia a un AFD y luego procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por defecto. Además todo esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla. Los campos deben estar separados por tabulación y son:           
            1. cadena, 
            2. sucesión de parejas (estado, símbolo) de cada paso del procesamiento . 
            3. sí o no dependiendo de si la cadena es aceptada o no"""
        afd1 = self.AFN_LambdaToAFD(self)
        afd1.procesarListaCadenas(listaCadenas,nombreArchivo,imprimirPantalla)
    def graficarAutomata(self):
        """Grafica el automata usando librerias de matplotlib y NetworkX"""
        graficar = graficarAutomata()
        graficar.mostrarGrafo(self)
  

    #================================================

#print('Ejecutando AFN_e.py:...\n')
# nfe1= AFN_Lambda("ej1.nfe")

# print('Ejecutando:...\n')

# listacadenas= ['aaaba', 'bba', 'ababaa', 'aaabbb', 'ab', 'bb', 'aa']
# print(nfe1.procesarCadena('aaa'))
# nfe1.procesarCadenaConDetalles('aaa')
# nfe1.procesarListaCadenas(listacadenas)


#print(nfe1.delta)
# print(nfe1.toString())
# print('\n')
# nfe1.exportar('ej2.nfe')
#print(nfe1.pruebas(' '))