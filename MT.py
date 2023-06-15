from Alfabeto import Alfabeto
from Graph import graficarAutomata
import re, copy
class MT:
    """ 
    # Clase MT 
    ## Máquina de Turing
    Ésta clase modela y simula la Máquina de Turing MT de una sola Cinta 

    """
    Q = None
    q0 =None
    F =None
    Sigma =None
    CSigma = None #Gamma
    delta = None
    Cinta =None
    nombreArchivo='archivoMT'
    extension = "tm"
    etiquetas=['#!tm', '#states', '#initial', '#accepting','#inputAlphabet', '#tapeAlphabet',  '#transitions']
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
                    for i in string.strip().split('\n'):
                        if i in self.etiquetas[1:]:
                            key = i
                        elif i != '' or not i.isspace():
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions': # AFPD: no contiene transiciones lambda
                                trans=re.split(r"[:?]", i)
                                if(len(trans)!=5 or ';' in trans): raise ValueError("transicion invalida: ", i) # "; " q no puede tener varias salidas con un simbolo
                                estado, simbolo, estadoDestino, escritura ,desplazamiento = trans
                                #print('trans: ', trans)
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={ simbolo:[[escritura, desplazamiento, estadoDestino]] }
                                else:
                                    if(dictReader[estado].get(simbolo)==None):
                                        dictReader[estado][simbolo]=[[escritura, desplazamiento, estadoDestino]]
                                    else:
                                        dictReader[estado][simbolo].append([escritura, desplazamiento, estadoDestino])
                    self.Q = set(afc['#states'])
                    self.q0 = afc['#initial'][0]
                    self.F = set(afc['#accepting'])
                    self.Sigma = Alfabeto(afc['#inputAlphabet'])
                    self.Sigma.simbolos= [simb for simb in self.Sigma.simbolos if simb not in {'#', '$'}]
                    self.CSigma= Alfabeto(afc['#tapeAlphabet'])
                    self.delta = dictReader
                    #print('delta: ', self.delta)
                    self.nombreArchivo=((args[0]).split('.'+self.extension))[0]
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 6):  # Inicializar por los 6 parametros: alfabeto,alfabetoPila estados, estadoInicial, estadosAceptacion, delta
            self.Q, self.q0, self.F, self.Sigma, self.CSigma, self.delta = args
            self.Q=set(self.Q)
        elif(len(args) == 1 and isinstance(args[0], MT)):
            self.Q=copy.deepcopy(args[0].Q)
            self.q0=args[0].q0
            self.F=copy.deepcopy(args[0].F)
            self.Sigma=copy.deepcopy(args[0].Sigma)
            self.CSigma=copy.deepcopy(args[0].CSigma)
            self.delta=copy.deepcopy(args[0].delta)
        elif(len(args) == 0):
            self.Q = set()
            self.q0 =''
            self.F =set()
            self.Sigma =Alfabeto('')
            self.CSigma = Alfabeto('')
            self.delta = {}

        self.CSigma.simbolos.append('!')
        
    def procesarCadena(self, cadena: str='', imprimir=False, procesarFuncion=False, modoProcesarListas=False):
        """procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por la MT."""
        cinta = ['!'] if len(cadena.strip())==0 else list(cadena)
        index=0
        q=self.q0
        alfabeto= self.Sigma.simbolos + self.CSigma.simbolos
        trans= self.delta
        aceptada = None
        out=f'{cadena}\t'
        try:
            while True:
                # Obtener el símbolo actual
                simb = cinta[index]
                cinta[index]=f'({q})' # Se hace esto con propósitos de la impresión. Costo: tiempo constante
                out+=''.join(cinta)+'->'
                cinta[index]=simb
                if(q in self.F):  # q es de aceptación ?
                    aceptada = True
                    break
                if(simb not in alfabeto): # El simbolo no existe en los dos alfabetos, se descarta de paso que halla transiciónes para este simbolo
                    aceptada = False
                    break
                if(not trans.get(q, set())): # El estado no existe o no tiene transiciones, teniendo en cuenta que se comprobó que no es de aceptación (en el principio del while) se rechaza la cadena
                    aceptada=False
                    break
                # Calcular la transición: Siguiente estado + instrucciones lectura/escritura
                escritura, desplazamiento, estadoDestino  = trans[q][simb][0]
                # Actualizar el símbolo en la posición actual de la cinta
                cinta[index] = escritura
                # Desplazamiento de la posición actual según el movimiento
                if desplazamiento == '>':  # Desplazamiento a la derecha
                    index += 1
                    if index == len(cinta):  # Verificar si es la última posición
                        cinta.append('!')  # Agregar espacio en blanco al final de la cinta
                elif desplazamiento == '<':  # Desplazamiento a la izquierda
                    if index == 0: # Verificar si es la primera posición
                        cinta.insert(0, '!') # Inserar espacio en blanco al inicio de la cinta
                    else:
                        index -= 1
                q = estadoDestino
        except:
            pass

        if(modoProcesarListas):
            out=f'{cadena}\t{"".join(cinta).replace("!", "")}\t{"yes" if aceptada else "no"}'
            return out
        if(aceptada==None):
            out+='aborted'
            aceptada=False
        elif(aceptada):
            out+='accepted'
        else:
            out+='rejected'
        if imprimir:
            print(f'{out}\t{"yes" if aceptada else "no"}')
        if procesarFuncion:
            return ''.join(cinta).replace('!', '')
        return aceptada

    def procesarCadenaConDetalles(self, cadena):
        """  realiza  lo  mismo  que  el  método  anterior aparte  imprime  los detalles  del  procesamiento  con  el  formato  que se  indica  en  el  archivo MT.pdf. """

        return self.procesarCadena(cadena=cadena, imprimir=True)
    
    def procesarFunción(self, cadena):
        """procesa  la  cadena  y  retorna la  cadena  que  queda  escrita sobre la cinta al final(última configuración instantánea). """
        return self.procesarCadena(cadena=cadena, procesarFuncion=True)

    def procesarListaCadenas(self, listaCadenas ,nombreArchivo: str, imprimirPantalla: bool): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.  Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son: 
        1. cadena 
        2. Última configuración instantánea
        3. “yes”o “no”dependiendo de si la cadena es aceptada o no."""
        out=''
        for cadena in listaCadenas:
            out += self.procesarCadena(cadena=cadena,modoProcesarListas=True) + '\n'

        try:
            with open(f'./archivosSalida/{nombreArchivo}.txt', "w") as f:
                f.write(out)
        except:
            nombreArchivo= 'procesarListaCadenas_MT'
            with open(f'./archivosSalida/{nombreArchivo}', "w") as f:
                f.write(out)

        if(imprimirPantalla):
            print(out)

    def toString(self, graficar:bool=False):
        """Representar la MT con el formato de los archivos de entrada de MT (MT.pdf) de manera que se pueda imprimir fácilmente"""
        if self.instanciaVacia: return 'Instancia AFD vacía, no se le asigno un archivo o argumentos'
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] + '\n'+ '\n'.join(sorted(list(self.Q)))+ '\n'+self.etiquetas[2]+'\n'+self.q0+'\n'+self.etiquetas[3] + '\n'.join(sorted(list(self.F)))+  '\n'+self.etiquetas[4]+'\n'+self.Sigma.toStringEntrada()+ '\n'+ self.etiquetas[5]+ '\n'+ self.CSigma.toStringEntrada()+'\n'+self.etiquetas[6]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= self.delta[q][simb][0]
                deltaLinea=f'{q}:{simb}:{deltaSet[1]}?{deltaSet[2]}:{deltaSet[0]}'
                out+='\n'+deltaLinea
                #print ('deltaLinea: ',deltaLinea)
        if graficar:
            self.graficarAutomata()
        return out
    def graficarAutomata(self):
        """Grafica el automata usando librerias de matplotlib y NetworkX"""
        graficar = graficarAutomata()
        graficar.mostrarGrafo(self)