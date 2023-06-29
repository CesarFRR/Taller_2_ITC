from Alfabeto import Alfabeto
import re
from Tree import nonBinaryTree, nonBinaryTreePila
from itertools import product as productoCartesiano
from AFD import AFD
from Graph import graficarAutomata

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
    nombreArchivo = ''
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


    def modificarPila(self, pila: str, operacion: str, parametro: str):
        """Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase."""
        if operacion == 'pop':
            pila = pila[:-1]
        if operacion == 'push':
            pila += parametro
        elif operacion == 'swap':
            pila[-1] == parametro

        return pila
    
    def recorrerCadena(self,tree):
        cadena = tree.val[1]
        for index, simbolo in enumerate(cadena):
            if self.delta.get(tree.val[0]) is not None:
                for char, parametro1 in sorted(self.delta[tree.val[0]]):
                    if char == simbolo:
                        for result, parametro2 in sorted(self.delta[tree.val[0]][(char, parametro1)]):
                            pila = tree.val[2]
                            if len(pila) > 0:
                                if parametro1 != '$' and parametro2 != '$':
                                    if parametro1 == pila[-1]:
                                        pila = self.modificarPila(pila, 'swap', parametro2)
                                        tree.insert(result, cadena[index+1:], pila)
                                        
                                elif parametro1 != '$' and parametro2 =='$':
                                    if parametro1 == pila[-1]:
                                        pila = self.modificarPila(pila, 'pop', parametro2)
                                        tree.insert(result, cadena[index+1:], pila)
                                        
                                    else:break
                                elif parametro1 == '$' and parametro2 != '$':
                                    pila = self.modificarPila(pila, 'push', parametro2)
                                    tree.insert(result, cadena[index+1:], pila)
                                    
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, cadena[index+1:], pila)
                                    
                            else:
                                if parametro1 == '$' and parametro2 != '$':
                                    pila = self.modificarPila(pila, 'push', parametro2)
                                    tree.insert(result, cadena[index+1:], pila)
                                    
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, cadena[index+1:], pila)   
                        for child in tree.children:
                            self.recorrerCadena(child)
                    elif char == '$':
                        for result, parametro2 in sorted(self.delta[tree.val[0]][(char, parametro1)]):
                            pila = tree.val[2]
                            if len(pila) > 0:
                                if parametro1 != '$' and parametro2 != '$':
                                    if parametro1 == pila[-1]:
                                        pila = self.modificarPila(pila, 'swap', parametro2)
                                        tree.insert(result, cadena[index:], pila)
                                        
                                elif parametro1 != '$' and parametro2 =='$':
                                    if parametro1 == pila[-1]:
                                        pila = self.modificarPila(pila, 'pop', parametro2)
                                        tree.insert(result, cadena[index:], pila)
                                        
                                    else:break
                                elif parametro1 == '$' and parametro2 != '$':
                                    pila = self.modificarPila(pila, 'push', parametro2)
                                    tree.insert(result, cadena[index:], pila)
                                    
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, cadena[index:], pila)
                                    
                            else:
                                if parametro1 == '$' and parametro2 != '$':
                                    pila = self.modificarPila(pila, 'push', parametro2)
                                    tree.insert(result, cadena[index:], pila)
                                    
                                elif parametro1 == '$' and parametro2 == '$':
                                    tree.insert(result, cadena[index:], pila)   
                        for child in tree.children:
                            self.recorrerCadena(child)
                    
                else:
                    break
            else:
                break
            

    def procesamiento(self,cadena):
        try:
            self.aceptacion = []
            self.rechazadas = []
            self.abortadas = []
            pila = ''
            tree = nonBinaryTreePila(self.q0, cadena, pila)
            self.rutas = []
            
            pila = self.recorrerCadena(tree)
            

            self.rutas = tree.recorrer(tree)

            for ruta in range(len(self.rutas)):
                self.rutas[ruta] = list(self.rutas[ruta])
                for i in range(len(self.rutas[ruta])):
                    self.rutas[ruta][i] = list(self.rutas[ruta][i])
                    for j in range(len(self.rutas[ruta][i])):
                        if self.rutas[ruta][i][j] == '':
                            self.rutas[ruta][i][j] = '$'

            for ruta in self.rutas:
                out=''
                if ruta[len(ruta)-1][1] == '$':
                    if ruta[len(ruta)-1][2] == '$':
                        if ruta[len(ruta)-1][0] in self.F:
                            for procesamiento in ruta:
                                out += f'{procesamiento}-> '
                            out+='Aceptacion'
                            if out not in self.aceptacion:
                                self.aceptacion.append(out)
                        else:
                            for procesamiento in ruta:
                                out += f'{procesamiento}->'
                            out+='No aceptacion'
                            if out not in self.aceptacion:
                                self.rechazadas.append(out)
                    else:
                        for procesamiento in ruta:
                            out += f'{procesamiento}->'
                        out+='No aceptacion'
                        if out not in self.rechazadas:
                            self.rechazadas.append(out)
                else:
                    for procesamiento in ruta:
                        out += f'{procesamiento}->'
                    out+='Procesamiento abortado'
                    if out not in self.abortadas:
                        self.abortadas.append(out)
            # print('aceptacion \n',self.aceptacion)
            # print('rechazadas \n',self.rechazadas)           
            # print('abortadas \n',self.abortadas)
            if len(self.aceptacion) > 0:
                return self.aceptacion[0]
        except:
            pass
        return None

        #print(tree)

    def procesarCadena(self, cadena):
        """ procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata. """
        aceptada = None
        
        try:
            aceptada=self.procesamiento(cadena)
        except:
            aceptada=False
        return aceptada
    
    def procesarCadenaConDetalles(self, cadena):
        """realiza  lo  mismo  que  el  método  anterior aparte  imprime  losdetalles  del  procesamiento  con  el  formato  que se  indica  en  el  archivo AFPD.pdf."""
        aceptada = self.procesamiento(cadena)
        if aceptada is not None:
            print(aceptada)
            return True
        return False
    
    def  computarTodosLosProcesamientos(self, cadena,  nombreArchivo):  
        """Debe  imprimir  cada  uno de los posibles procesamientos de acuerdo al formato establecido en el archivo AFPN.pdfe indicando si al final de cada procesamiento se llega a aceptación o rechazo. Debe llenar una lista  de  todos  procesamientos  de  aceptación,  una  lista  de  todos  los  procesamientos rechazados.  Debe  guardar  los  contenidos  de  estas  listas  cada  una  en  un  archivo(cuyos nombres  son  nombreArchivoAceptadasAFPN.txtynombreArchivoRechazadasAFPN.txt)  y además imprimirlas en pantalla. Se debe retornar el número de procesamientos realizados."""
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
    
    def procesarListaCadenas(self, listaCadenas, nombreArchivo = None, imprimirPantalla:bool = False): 

        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.  Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son: 
        1. cadena, 
        2. un procesamientode aceptación (si lo hay, si no unode rechazo), 
        3. número de posibles procesamientos 
        4. número de procesamientos de aceptación 
        5. número de procesamientos de rechazo 
        6. “yes”o “no”dependiendo de si la cadena es aceptada o no."""
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
                    if(self.aceptacion):
                        archivo.write(f'{self.aceptacion[0]}\n')
                except:
                    try:
                        if(self.rechazadas):
                            archivo.write(f'{self.rechazadas[0]}\n')
                    except:
                        if(self.abortadas):
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
            with open(f'./archivosSalida/{nombreArchivo}.txt', 'r') as archivo:
                for line in archivo:
                    print(line)

    def hallarProductoCartesianoConAFD(self, afd):
        """: debe calcular y retornar el producto cartesiano con un AFD dado como parámetro."""
        afpnEstados = sorted(self.Q)
        afdEstados = sorted(afd.Q)
        q0 = ''
        aceptacion = set()
        estados = [(i,j)for i in afpnEstados for j in afdEstados]
        q = set()
        transiciones = dict()
        for q1, q2 in estados:
            estadoCreado = f'({q1},{q2})'
            estadoLista = [q1, q2]
            q.add(estadoCreado)
            transiciones.update({estadoCreado:{}})
            if q1 in self.F and q2 in afd.F:
                aceptacion.add(estadoCreado)
            if({q1,q2}=={self.q0, afd.q0}):
                q0 = estadoCreado
            for simbolo in self.Sigma.simbolos:
                #print('a')
                trAFD = list(afd.delta[q2][simbolo])[0]
                if self.delta.get(q1) is not None:
                    for char, parametro1 in self.delta[q1]:
                        if char == simbolo:
                            for result, parametro2 in sorted(self.delta[q1][(char, parametro1)]):
                                
                                if transiciones[estadoCreado].get((char, parametro1)) is None:
                                    transiciones[estadoCreado][(char, parametro1)] = {(f'({result},{trAFD})', parametro2)}
                                else:
                                    transiciones[estadoCreado][(char, parametro1)].add((f'({result},{trAFD})', parametro2))
                        elif char == '$':
                            for result, parametro2 in sorted(self.delta[q1][(char, parametro1)]):
                                
                                if transiciones[estadoCreado].get((char, parametro1)) is None:
                                    transiciones[estadoCreado][(char, parametro1)] = {(f'({result},{estadoLista[1]})', parametro2)}
                    
                                else:
                                    transiciones[estadoCreado][(char, parametro1)].add((f'({result},{estadoLista[1]})', parametro2))
                        #     break
        return AFPN(q, q0, aceptacion, self.Sigma, self.PSigma, transiciones)
    

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
            self.graficarAutomata()
        return out
    
    def exportar(self, archivo):
        with open(f'./archivosSalida/{archivo}.{self.extension}', 'w') as archivo:
            archivo.write(self.toString())

    def graficarAutomata(self):
        """Grafica el automata usando librerias de matplotlib y NetworkX"""
        graficar = graficarAutomata()
        graficar.mostrarGrafo(self)

#----------------------------------------------------------------

#pda1 = AFPN('ej1.pda')
# print(pda1.delta)
# dfa = AFD('ej4.dfa')
# cartesiano = pda1.hallarProductoCartesianoConAFD(dfa)
# print(cartesiano.toString())
#print(pda1.procesarCadenaConDetalles('0110'))
# cartesiano.computarTodosLosProcesamientos('0110', 'cartesianoPrueba')
#print(pda1.computarTodosLosProcesamientos('0110', 'AFPN_rechazadas'))
# pda1.procesarListaCadenas(['aaab','aabbbbcc','aabbc','abc','abbbbbcccc'], 'ListaDeCadenasPila')
