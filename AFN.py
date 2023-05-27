from Alfabeto import Alfabeto
import re

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
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma, self.Q, self.qo, self.F, self.delta = args
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
    
    def AFNtoAFD(self, afn):
        states = list(afn.Q)
        delta = afn.delta
        accepting= afn.F

        for state,transition in delta.items():  
            for symbol in transition:
                if len(transition[symbol])>1:           #Comprobar si un simbolo lleva a mas de un estado
                    states.append(tuple(transition[symbol]))    #Agregar tupla de todos los estados a los que lleva
        
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
        headers = ['Estado']+(list(afn.Sigma.simbolos))
        for i in headers:
            print(f'{i:<20}',end="")
        for key, value in delta.items():
            print('\n',f'{str(key):<20}', end="")
            for state,transition in value.items():
                print(f'{str(value[state]):<20}', end="")
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

    def procesarCadena(self, cadena):
        actual = [self.q0]
        for simbolo in cadena:
            prox = []
            if simbolo not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                return False
            for state in actual:
                if self.delta.get(actual[actual.index(state)]) is not None:   #Verificar que el estado actual exista
                    transiciones = self.delta[actual[actual.index(state)]]    #Lista de transiciones del estado actual    
                    if simbolo in transiciones:                               #Recorrer las transiciones verificando el simbolo actual y el estado resultado
                        for i in transiciones[simbolo]:
                            prox.append(i)                                    
            actual = prox
            if actual == []:
                break
            #print(f'{simbolo:3}:{actual}')
            
        for state in actual:              
            if state in self.F and actual!=[]:  #verificar si el estado actual es de aceptacion en cualquier procesamiento
                return True
        return False
    
    #Trabajando en esto
    def procesarCadenaConDetalles(self, cadena):
        return self.procesamiento(cadena,self.q0,'')
        
    
    def procesamiento(self,cadena, actual, out):
        final = False
        for index, char in enumerate(cadena):
            if char not in self.Sigma.simbolos:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                out+= f'[{actual},{cadena[index:]}]-> No Aceptación'
                print(out)
                return False
            if(actual in self.Q):
                if self.delta.get(actual) is not None: 
                    if len(list(self.delta[actual][char])) > 1:
                        out+= f'[{actual},{cadena[index:]}]-> '
                        for i in list(self.delta[actual][char]):
                            procesamiento = self.procesamiento(cadena[index+1:],i,out)
                            if procesamiento ==True:
                                return True
                    elif len(list(self.delta[actual][char])) == 1:
                        out+= f'[{actual},{cadena[index:]}]-> '
                        actual = list(self.delta[actual][char])[0]
            else:
                break
            if len(cadena[index:]) == 1:
                final = True

        if actual in self.F and final == True: #verificar si el estado actual es de aceptacion
            out+= 'Aceptación'
            print(out)
            return True
        else:
            out+= 'No Aceptación'
        
        return False
    
    #Trabajando en esto
    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        return 0
    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        pass 

    def procesarCadenaConversion(self, cadena):
        afd = self.AFNtoAFD(self)
        return afd.procesarCadena(cadena)
    
    def  procesarCadenaConDetallesConversion(self, cadena):
        afd = self.AFNtoAFD(self)
        return afd.procesarCadenaConDetalles(cadena)
    
    def procesarListaCadenasConversion(self, listaCadenas,nombreArchivo, imprimirPantalla):
        pass

#================================================

print('Ejecutando:...\n')
nfa1= AFN("ej1.nfa")
nda = nfa1.AFNtoAFD(nfa1)
print(nda.toString())
print('\n')
#print(nfa1.toString())
#print('\n')
#nfa1.exportar('ej2.nfa')
