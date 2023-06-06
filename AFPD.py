from AFD import AFD
import copy
import re
from Alfabeto import Alfabeto
class AFPD:
    Q = None
    q0 =None
    F =None
    Sigma =None
    PSigma = None
    delta = None
    
    nombreArchivo='archivodpda'
    extension = "dpda"
    etiquetas=['#!dpda', '#states', '#initial', '#accepting','#tapeAlphabet', '#stackAlphabet',  '#transitions']
    instanciaVacia=False
    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], str)):  # Inicializar por archivo txt
            if (not args[0].endswith("." + self.extension)):raise ValueError("El archivo proporcioando no es de formato ", self.extension)
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
                        elif i != '' or not i.isspace():
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions': # AFD: no contiene transiciones lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3 or ';' in trans[2]): raise ValueError("transicion invalida: ", i) # "; " q no puede tener varias salidas con un simbolo
                                estado, simbolo, deltaResultado = trans
                                #print('trans: ', trans)
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={simbolo: set({deltaResultado}) }
                                else:
                                    dictReader[estado].update({simbolo:set({deltaResultado})})
                    self.Sigma = Alfabeto(afc['#alphabet'])
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
        elif(len(args) == 1 and isinstance(args[0], AFPD)):
            self.Q=copy.deepcopy(args[0].Q)
            self.qo=args[0].q0
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
        
        self.estadosLimbo = set()
        self.estadosInaccesibles=set()
        self.verificarCorregirCompletitudAFD()
        self.hallarEstadosLimbo()

    def __init__(self, estados, estadoInicial, estadosAceptacion, alfabetoCinta, alfabetoPila, delta):
        self.Q = estados
        self.q0 = estadoInicial
        self.F = estadosAceptacion
        self.Sigma = alfabetoCinta
        self.PSigma = alfabetoPila
        self.delta = delta

    def modificarPila(self, pila, operacion, parametro):
        """Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase."""
        pass
        
    def procesarCadena(self, cadena):
        """ procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata. """
                    
        return True
    def procesarCadenaConDetalles(self, cadena):
        """realiza  lo  mismo  que  el  método  anterior aparte  imprime  losdetalles  del  procesamiento  con  el  formato  que se  indica  en  el  archivo AFPD.pdf."""
        return True
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.
        Los campos deben estar separados por tabulación y son:
        1. cadena.
        2. procesamiento (con el formato del archivo AFPD.pdf).
        3. ‘yes’ o ‘no’dependiendo de si la cadena es aceptada o no.
        """
        pass
    def hallarProductoCartesianoConAFD(afd):
        """: debe calcular y retornar el producto cartesiano con un AFD dado como parámetro."""
        pass
    def toString(self):
        """Representar  el  AFPD  con  el  formato  de  los  archivos  de  entrada  de  AFPD (AFPD.pdf)de manera que se pueda imprimir fácilmente"""
        pass
    