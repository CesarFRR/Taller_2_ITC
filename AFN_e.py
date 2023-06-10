from AFN import AFN
from Alfabeto import Alfabeto
from Graph import graficarAutomata
import re
class AFN_Lambda:
    """
    # Clase AFN_Lambda

    Ésta clase modela y simula el Autómata Finito No determinista con transiciones lambda AFNe también conocido como AFN epsilon o lambda el cual puede poseer cero, uno o más transiciónes para un símbolo perteneciente al Alfabeto además de las transiciones lambda

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
            simbolos, self.Q, self.qo, self.F, self.delta = args
            if(isinstance(simbolos, Alfabeto)):
                self.Sigma=simbolos
            else:
                self.Sigma=Alfabeto(simbolos)
            self.Q=set(self.Q)
            self.F=set(self.F)
        self.Sigma.simbolos.append('$')
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
    def toString(self):
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for Q in self.delta:
            for simb in self.delta[Q]:
                deltaSet= sorted((list(self.delta[Q][simb])))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{Q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        return out
    def imprimirAFNLSimplificado(self):
        pass

    def exportar(self, archivo: str):
        with open(archivo, "w") as f:
            f.write(self.toString())

    def lambda_clausura(afnl, states):
        clausura = set(states)
        while True:
            # Para cada estado en clausura, añade todos los estados que se pueden alcanzar mediante transiciones lambda.
            new_states = set(state for s in clausura for state in afnl.delta[s].get('$', set()))
            # Si no se añadieron nuevos estados, detiene el bucle.
            if new_states.issubset(clausura):
                break
            # Añade los nuevos estados a clausura.
            clausura = clausura.union(new_states)
        return clausura

    def AFN_LambdaToAFN(self, nfe1=None):
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
                    next_states = next_states.union(AFN_Lambda.lambda_clausura(nfe1, {target}))
                if(len(next_states)==0):
                    continue
                delta[state][symbol] = next_states
        # Actualiza los estados de aceptación para el AFN.
        for state in Q:
            # Si un estado puede llegar a un estado de aceptación a través de transiciones lambda, se convierte en un estado de aceptación.
            if not nfe1.F.isdisjoint(AFN_Lambda.lambda_clausura(nfe1, {state})):
                F.add(state)

        return AFN(Sigma, Q, q0, F, delta)

    def AFN_LambdaToAFD(self, nfe1=None):
        if nfe1==None:
            nfe1=self
        afn = AFN_Lambda.AFN_LambdaToAFN(nfe1)
        afd = AFN.AFNtoAFD(afn, False)
        return afd


    def procesamiento(self,cadena: str, actual, detalles, proc,  out='')-> bool:
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
                                procesamiento = self.procesamiento(cadena[index:], i, detalles, proc, out)
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

    def procesarCadena(self, cadena: str)-> bool:
        return self.procesamiento(cadena, self.q0, False, True)

    def procesarCadenaConDetalles(self, cadena: str)-> bool:
        return self.procesamiento(cadena, self.q0, True, True)

    def computarTodosLosProcesamientos(self, cadena: str, nombreArchivo: str)-> int:
        self.aceptacion = []
        self.rechazadas = []
        self.abortadas = []
        self.procesamiento(cadena, self.q0, False, '')

        with open(f'{nombreArchivo}Abortadas.txt', 'a') as abortadas:
            abortadas.truncate(0)
            for i in self.abortadas:
                abortadas.write(f'{i}\n')
                print(f'{i}')
        with open(f'{nombreArchivo}Rechazadas.txt', 'a') as rechazadas:
            rechazadas.truncate(0)
            for i in self.rechazadas:
                rechazadas.write(f'{i}\n')
                print(f'{i}')
        with open(f'{nombreArchivo}Aceptadas.txt', 'a') as aceptadas:
            aceptadas.truncate(0)
            for i in self.aceptacion:
                aceptadas.write(f'{i}\n')
                print(f'{i}')

        return len(self.aceptacion + self.rechazadas + self.abortadas)

    def procesarListaCadenas(self, listaCadenas: list,nombreArchivo: str, imprimirPantalla: bool):
        with open(nombreArchivo, 'r+') as archivo:
            archivo.truncate(0)

        with open(nombreArchivo, 'a') as archivo:
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

        if imprimirPantalla:
            with open(nombreArchivo, 'r') as archivo:
                for line in archivo:
                    print(line)

    def procesarCadenaConversion(self, cadena: str)-> bool:
        afd1= self.AFN_LambdaToAFD(self)
        return afd1.procesarCadena(cadena)

    def procesarCadenaConDetallesConversion(self, cadena: str)-> bool:
        afd1 = self.AFN_LambdaToAFD(self)
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
        graficarAutomata.mostrarGrafo(self)
  

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