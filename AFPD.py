
class AFPD:
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
    