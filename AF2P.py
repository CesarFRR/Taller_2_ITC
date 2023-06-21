import copy
import re
from Alfabeto import Alfabeto
from Graph import graficarAutomata

class AF2P:
    """ 
    # Clase AF2P
    Ésta clase modela y simula el Autómata Finito con dos Pilas  AF2P el cual  posee 2 pilas como principal característica
    """
    Q = None
    q0 =None
    F =None
    Sigma =None
    PSigma = None
    delta = None
    nombreArchivo='archivo2pda'
    extension = "msm"
    etiquetas=['#!msm', '#states', '#initial', '#accepting','#tapeAlphabet', '#stackAlphabet',  '#transitions']
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
                                transLine=re.split(r"[>]", i)
                               
                                transA, transB = transLine
                                #print(transLine, transA.split(':'))
                                if(len(transA.split(':'))!=4): raise ValueError("transicion invalida: ", i) # "; " q no puede tener varias salidas con un simbolo
                                estado, simbolo, pop1, pop2 = transA.split(':') #estadoDestino, push = trans
                                #print('trans: ', trans)
                                listaTransiciones=[]
                                for transiciones in transB.split(';'):
                                    estadoDestino, push1, push2 = transiciones.split(':')
                                    listaTransiciones.append([pop1, push1, pop2, push2, estadoDestino])
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={ simbolo:listaTransiciones} #q0:a:A:B>q1:$:C;q2:D:B;q3:$:$
                                else:
                                    if(dictReader[estado].get(simbolo)==None):
                                        dictReader[estado][simbolo]=listaTransiciones
                                    else:
                                        dictReader[estado][simbolo].extend(listaTransiciones)
                            
                    self.Sigma = Alfabeto(afc['#tapeAlphabet'])
                    self.PSigma= Alfabeto(afc['#stackAlphabet'])
                    self.Q = set(afc['#states'])
                    self.q0 = afc['#initial'][0]
                    self.F = set(afc['#accepting'])
                    self.delta = dictReader
                    #print('delta: ', self.delta)
                    self.nombreArchivo=((args[0]).split('.'+self.extension))[0]
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 6):  # Inicializar por los 6 parametros: alfabeto,alfabetoPila estados, estadoInicial, estadosAceptacion, delta
            self.Q, self.q0, self.F,self.Sigma, self.PSigma, self.delta = args
            self.Q=set(self.Q)
        elif(len(args) == 1 and isinstance(args[0], AF2P)):
            self.Q=copy.deepcopy(args[0].Q)
            self.q0=args[0].q0
            self.F=copy.deepcopy(args[0].F)
            self.Sigma=copy.deepcopy(args[0].Sigma)
            self.PSigma=copy.deepcopy(args[0].PSigma)
            self.delta=copy.deepcopy(args[0].delta)
        elif(len(args) == 0):
            self.Q = set()
            self.q0 =''
            self.F =set()
            self.Sigma =Alfabeto('')
            self.PSigma = Alfabeto('')
            self.delta = {}

        #self.PSigma.simbolos.append('$')




    def modificarPila(self, pila: list, operacion: str, parametro: str):
        """Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase."""
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
                    pila.pop()
        elif operacion == 'swap':
            for simb in parametro:
                pila.pop()
                pila.append(simb)

    def procesarCadena(self, cadena: str)-> bool:
        """ procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata. """
                    
        return True
    def procesarCadenaConDetalles(self, cadena: str)-> bool:
        """ realiza  lo  mismo  que  el  método  anterior aparte imprime más detalles. En específico, si la cadena es aceptada debe imprimir uno de los procesamientos de aceptación y si es rechazada debe imprimir todos los procesamientos posibles  de  la  cadena.  En  particular,  cada  procesamiento  debe  ser  impreso de  acuerdo  al formato indicado en el archivo AF2P.pdf"""
        return True
    def  computarTodosLosProcesamientos(cadena,  nombreArchivo: str)-> int:  
        """Debe  imprimir  cada  uno de los posibles procesamientos de acuerdo al formato establecido en el archivo AF2P.pdfe indicando si al final de cada procesamiento se llega a aceptación o rechazo. Debe llenar una lista  de  todos  procesamientos  de  aceptación,  una  lista  de  todos  los  procesamientos rechazados.  Debe  guardar  los  contenidos  de  estas  listas  cada  una  en  un  archivo(cuyos nombres  son  nombreArchivoAceptadasAF2P.txtynombreArchivoRechazadasAF2P.txt)  y además imprimirlas en pantalla. Se debe retornar el número de procesamientos realizados."""
        return 0
    def procesarListaCadenas(self, listaCadenas,nombreArchivo:str='', imprimirPantalla:bool=False): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.  Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son: 
        1. cadena, 
        2. un procesamientode aceptación (si lo hay, si no unode rechazo), 
        3. número de posibles procesamientos 
        4. número de procesamientos de aceptación 
        5. número de procesamientos de rechazo 
        6. “yes”o “no”dependiendo de si la cadena es aceptada o no."""
        pass

    def toString(self, graficar:bool=False):
        """Representar el AF2P con el formato de los archivos de entrada de AF2P (AF2P.pdf) de manera que se pueda imprimir fácilmente."""
        if self.instanciaVacia: return 'Instancia AFD vacía, no se le asigno un archivo o argumentos'
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] + '\n'+ '\n'.join(sorted(list(self.Q)))+ '\n'+self.etiquetas[2]+'\n'+self.q0+'\n'+self.etiquetas[3] + '\n'.join(sorted(list(self.F)))+  '\n'+self.etiquetas[4]+'\n'+self.Sigma.toStringEntrada()+ '\n'+ self.etiquetas[5]+ '\n'+ self.PSigma.toStringEntrada()+'\n'+self.etiquetas[6]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= self.delta[q][simb]
                trans=''
                p1=''
                p2=''
                for d in deltaSet:
                    pop1, push1, pop2, push2, estadoDestino = d
                    p1, p2, = pop1, pop2
                    trans+=f'{estadoDestino}:{push1}:{push2};' #q0:a:A:B>q1:$:C;q2:D:B;q3:$:$
                trans = trans.rstrip(';')
                deltaLinea=f'{q}:{simb}:{p1}:{p2}>{trans}'
                out+='\n'+deltaLinea
                #print ('deltaLinea: ',deltaLinea)
        if graficar:
            self.graficarAutomata()
        return out
    def exportar(self, nombreArchivo):
        with open(f'./archivosSalida/{nombreArchivo}.{self.extension}', "w") as f:
            f.write(self.toString())
    def graficarAutomata(self):
        """Grafica el automata usando librerias de matplotlib y NetworkX"""
        graficar = graficarAutomata()
        graficar.mostrarGrafo(self)
    