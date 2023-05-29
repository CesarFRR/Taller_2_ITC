from AFN import AFN
from Alfabeto import Alfabeto
import re
class AFN_Lambda:
    Sigma=None
    Q=None
    q0=None
    F=None
    delta = {}
    estadosLimbo = None
    estadosInaccesibles = None
    automata_tipo = "nfe"
    etiquetas=['#!nfe', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
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
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma, self.Q, self.qo, self.F, self.delta = args
            self.Q=set(self.Q)
            self.F=set(self.F)

        self.Sigma.add('$')

    def hallarEstadosInaccesibles(self):
        pass
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

    def exportar(self, archivo):
        with open(archivo, "w") as f:
            f.write(self.toString())

    def lambda_clausura(self, afnl, states):
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

    def AFN_LambdaToAFN(self, afnl):
        # Copia Sigma, Q, q0 y F desde afnl, pero elimina el símbolo '$' de Sigma.
        Sigma = afnl.Sigma - {'$'}
        Q = afnl.Q
        q0 = afnl.q0
        F = set()
        delta = {}

        # Calcula la función de transición para el AFN.
        for state in Q:
            delta[state] = {}
            for symbol in Sigma:
                next_states = set()
                for target in afnl.delta[state].get(symbol, set()):
                    next_states = next_states.union(self.lambda_clausura(afnl, {target}))
                delta[state][symbol] = next_states

        # Actualiza los estados de aceptación para el AFN.
        for state in Q:
            # Si un estado puede llegar a un estado de aceptación a través de transiciones lambda, se convierte en un estado de aceptación.
            if not afnl.F.isdisjoint(self.lambda_clausura(afnl, {state})):
                F.add(state)

        return AFN(Sigma, Q, q0, F, delta)

    def AFN_LambdaToAFD(self, afnl):
        afn = self.AFN_LambdaToAFN(afnl)
        afd = AFN.AFNtoAFD(afn, False)
        return afd


    def procesamiento(self,cadena, actual, detalles, proc,  out=''):
        final = False
        breaked = False

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
                            for i in sorted(self.delta[actual]['$']):
                                # print(sorted(self.delta[actual][char]))
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

    def procesarCadena(self, cadena):
        return self.procesamiento(cadena, self.q0, False, True)

    def procesarCadenaConDetalles(self, cadena):
        return self.procesamiento(cadena, self.q0, True, True)

    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
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

    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla):
        pass

    def procesarCadenaConversion(self, cadena):
        pass

    def procesarCadenaConDetallesConversion(self, cadena):
        pass

    def procesarListaCadenasConversion(self, listaCadenas,nombreArchivo, imprimirPantalla):
        pass

    def pruebas(self, cadena):
        out=''
        print("usando delta: \n")
        limbo = { 'L':{  s: set('L') for s in self.Sigma.simbolos} }
        print('limbo: ', limbo)
        for estado in self.delta:
            for simb in self.Sigma.simbolos:
                if(self.delta[estado].get(simb)==None):
                    self.delta[estado][simb] = limbo

        out = self.toString() #.get() retorna el conjunto del simbolo dado, si no existe retorna un conjunto vacío (esto es para evitar errores de KeyError: clave no encontrada)
        return out

    #================================================

print('Ejecutando:...\n')
nfe1= AFN_Lambda("ej1.nfe")

print('Ejecutando:...\n')
print(nfe1.delta)
# print(nfe1.toString())
# print('\n')
# nfe1.exportar('ej2.nfe')
print(nfe1.pruebas(' '))