from AFD import AFD
from Alfabeto import Alfabeto
import re
#from visual_automata.fa.nfa import VisualNFA

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
    nombreArchivo=''
    extension = "nfa"
    aceptacion = []
    rechazadas = []
    abortadas = []
    deltaParaGraficar={}
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
            self.Sigma, self.Q, self.q0, self.F, self.delta = args
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
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]+'\n'+'\n'.join(sorted((list(self.hallarEstadosInaccesibles()))))+'\n'+self.etiquetas[6]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= sorted(list(self.delta[q][simb]))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        return print(out)

    def imprimirAFNSimplificado(self): #Similar al anterior sin estados inaccesibles
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+'\n'+self.etiquetas[6]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= sorted(list(self.delta[q][simb]))
                deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
        return print(out)

    def exportar(self, archivo):
        with open(archivo, "w") as f:
                f.write(self.toString())

    def AFNtoAFD(self, afn, imprimir = True):
        states = list(afn.Q)
        delta = afn.delta
        accepting= afn.F

        for state, transition in delta.items():
            for symbol, destiny in transition.items():
                if len(destiny)>1:           #Comprobar si un simbolo lleva a mas de un estado
                    states.append(tuple(destiny))    #Agregar tupla de todos los estados a los que lleva

        #Recorrer lista de estados una vez realizadas las modificaciones anteriores
        for actual in states:
            transitions = dict()    #diccionario con transiciones para los nuevos estados
            if type(actual) is tuple:       #Verificar que el estado actual sea una tupla
                for state in actual:
                    if len(state) > 1 and afn.delta.get(state) is not None:      #Verificar que la tupla contenga mas de un elemento    
                        for symbol in afn.delta.get(state):                      #Verificar transiciones de cada simbolo con cada estado de la tupla             
                            if transitions.get(symbol) is not None:              #Si ya se agregaron las transiciones de uno de los estados, actualizar con las de los demas
                                transitions.update({str(symbol):set(sorted(set(transitions[symbol]).union(delta[state][symbol])))})
                            else:                                                #Aun no se han agregado las transiciones de ningun estado
                                transitions.update({str(symbol):set(sorted(delta[state][symbol]))})

                delta.update({actual:transitions})

                #Agregar los estados que vayan surgiendo durante el proceso
                for symbol in afn.delta.get(actual):            
                    newState = tuple(afn.delta[actual][symbol])
                    if newState not in states and len(newState)>1:
                        states.append(newState)

        #Imprimir tabla de trancisiones
        if imprimir:
            out = ''
            for q in self.delta:
                for simb in self.delta[q]:
                    deltaSet= sorted(list(self.delta[q][simb]))
                    deltaSet= deltaSet[0] if len(deltaSet)==1 else ';'.join(deltaSet)
                    deltaLinea=f'{q}:{simb}>{deltaSet}'
                    out+='\n'+deltaLinea
            print(out)
            print('\n')
            
        strStates = set()
        for state in states:        #Agregar todos los estados que contengan alguno de aceptacion
            if type(state) is tuple:
                x = ','.join(state)     
                strStates.add(f'({x})')     #Convertir tupla a string
                for i in state:
                    if i in afn.F:
                        accepting.add(f'({x})')
            else:
                strStates.add(f'{state})')

        strDelta = dict()
        for actual, transition in delta.items():    #Cambiar keys del diccionario por strings
            x = '('+','.join(actual)+')' if type(actual) is tuple else actual
            strDelta[f'{x}'] = delta[actual]

        return AFD(afn.Sigma, strStates, afn.q0, set(accepting), delta) #Retornar AFD equivalente

    def procesamiento(self,cadena, actual, detalles, proc,  out=''):
        final = False
        breaked = False

        for index, char in enumerate(cadena):
            if char not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                out+= f'[{actual},{cadena[index:]}]-> Procesamiento abortado'
                if out not in self.abortadas:
                    self.abortadas.append(out)
                break
            if(actual in self.Q):
                if self.delta.get(actual) is not None and self.delta.get(actual).get(char) is not None: 
                    if len(list(self.delta[actual][char])) > 1:
                        out+= f'[{actual},{cadena[index:]}]-> '
                        for i in sorted(self.delta[actual][char]):
                            #print(sorted(self.delta[actual][char]))
                            actual = i
                            procesamiento = self.procesamiento(cadena[index+1:],i,detalles, proc,  out)
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
    def procesarCadena(self, cadena):
        return self.procesamiento(cadena, self.q0, False, True)

    def procesarCadenaConDetalles(self, cadena):
        return self.procesamiento(cadena, self.q0, True, True)

    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        self.aceptacion = []
        self.rechazadas = []
        self.abortadas = []
        self.procesamiento(cadena,  self.q0, False, '')

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

        return len(self.aceptacion+self.rechazadas+self.abortadas)

    def procesarListaCadenas(self, listaCadenas: list, nombreArchivo: str, imprimirPantalla:bool):

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

    def procesarCadenaConversion(self, cadena):
        afd = self.AFNtoAFD(self, False)
        return afd.procesarCadena(cadena) 
    
    def  procesarCadenaConDetallesConversion(self, cadena):
        afd = self.AFNtoAFD(self, False)
        return afd.procesarCadenaConDetalles(cadena) 

    
    def procesarListaCadenasConversion(self, listaCadenas,nombreArchivo, imprimirPantalla):
        afd = self.AFNtoAFD(self, False)
        return afd.procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla)
    
    
    # def graficarAFN(self):
    #     print('GRAFICAR\n\n\n')
    #     #print(self.deltaParaGraficar.items())
    #     gEstados=dict()
    #     for q in self.deltaParaGraficar:
    #         est=q
    #         if(est=='L'):
    #             est='q30'
    #         gEstados.update({est:dict()})

    #         for simb in self.deltaParaGraficar[q]:
                
    #             deltaSet= list(self.deltaParaGraficar[est][simb])
    #             print(f'{q}:{simb}>{deltaSet}')
    #             if simb=='$':
    #                 gEstados[est].update({"":deltaSet})    
                
    #             gEstados[est].update({simb:deltaSet})
                
    #             #print ('deltaLinea: ',deltaLinea)
    #     # nfa = VisualNFA(
    #     #     states=self.Q,
    #     #     input_symbols=set(self.Sigma.simbolos),
    #     #     transitions=gEstados,
    #     #     initial_state=self.q0,
    #     #     final_states=self.F,
    #     # )
    #     nfaprueba = VisualNFA(
    #     states={"q0", "q1", "q2"},
    #     input_symbols={"0", "1"},
    #     transitions={
    #     "q0": {"": {"q2"}, "1": {"q1"}},
    #     "q1": {"1": {"q2"}, "0": {"q0", "q2"}},
    #     "q2": {},
    #     },
    #     initial_state="q0",
    #     final_states={"q0"},
    #     )
    #     nfaprueba.show_diagram(view=True)#.render('afnGraficar', format='png', cleanup=True, view=True)

#================================================

# print('Ejecutando:...\n')
# nfa1= AFN("ej1.nfa")
# nfa1.graficarAFN()
# nda = nfa1.AFNtoAFD(nfa1)
# print(nda.toString())
# print('\n')

#print(nfa1.toString())
#print('\n')
#nfa1.exportar('ej2.nfa')
