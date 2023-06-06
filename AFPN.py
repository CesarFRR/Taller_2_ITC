class AFPN:
    Q = None
    q0 =None
    F =None
    Sigma =None
    PSigma = None
    delta = None
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
    def  computarTodosLosProcesamientos(cadena,  nombreArchivo):  
        """Debe  imprimir  cada  uno de los posibles procesamientos de acuerdo al formato establecido en el archivo AFPN.pdfe indicando si al final de cada procesamiento se llega a aceptación o rechazo. Debe llenar una lista  de  todos  procesamientos  de  aceptación,  una  lista  de  todos  los  procesamientos rechazados.  Debe  guardar  los  contenidos  de  estas  listas  cada  una  en  un  archivo(cuyos nombres  son  nombreArchivoAceptadasAFPN.txtynombreArchivoRechazadasAFPN.txt)  y además imprimirlas en pantalla. Se debe retornar el número de procesamientos realizados."""
        return 0
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.  Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son: 
        1. cadena, 
        2. un procesamientode aceptación (si lo hay, si no unode rechazo), 
        3. número de posibles procesamientos 
        4. número de procesamientos de aceptación 
        5. número de procesamientos de rechazo 
        6. “yes”o “no”dependiendo de si la cadena es aceptada o no."""
        pass
    def hallarProductoCartesianoConAFD(afd):
        """: debe calcular y retornar el producto cartesiano con un AFD dado como parámetro."""
        pass
    def toString(self):
        """Representar  el  AFPNcon  el  formato  de  los  archivos  de  entrada  de  AFPN (AFPN.pdf) de manera que se pueda imprimir fácilmente."""
        pass
    