class MT:
    Q = None
    q0 =None
    F =None
    Sigma =None
    CSigma = None
    delta = None
    Cinta =None
    def __init__(self, estados, estadoInicial, estadosAceptacion, alfabetoEntrada, alfabetoCinta, delta, cinta):
        self.Q = estados
        self.q0 = estadoInicial
        self.F = estadosAceptacion
        self.Sigma = alfabetoEntrada
        self.CSigma = alfabetoCinta
        self.delta = delta
        self.Cinta = cinta
    
        
    def procesarCadena(self, cadena):
        """procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por la MT."""
                    
        return True
    def procesarCadenaConDetalles(self, cadena):
        """  realiza  lo  mismo  que  el  método  anterior aparte  imprime  los detalles  del  procesamiento  con  el  formato  que se  indica  en  el  archivo MT.pdf. """
        return True
    def procesarFunción(cadena):
        """procesa  la  cadena  y  retorna la  cadena  que  queda  escrita sobre la cinta al final(última configuración instantánea). """
        pass
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla): 
        """procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo;  si  este  es  inválido  se  asigna  un  nombre  por  defecto.  Además,todo  esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla.Los campos deben estar separados por tabulación y son: 
        1. cadena 
        2. Última configuración instantánea
        3. “yes”o “no”dependiendo de si la cadena es aceptada o no."""
        pass
    def toString(self):
        """Representar la MT con el formato de los archivos de entrada de MT (MT.pdf) de manera que se pueda imprimir fácilmente"""
        pass
    