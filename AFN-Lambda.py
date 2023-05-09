class AFN:
    Sigma=None
    Q=None
    q0=None
    F=None
    delta =[]
    estadosInaccesibles=None

    # def __init__(self, alfabeto, estados, estadoInicial, estadosAceptacion, delta):
    #     self.Sigma = alfabeto
    #     self.Q = estados
    #     self.q0 = estadoInicial
    #     self.F = estadosAceptacion
    #     self.delta = delta
    
    def __init__(self, *args):
        if (len(args) == 1):  # Inicializar por archivo txt
            pass
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma = args[0]
            self.Q = args[1]
            self.q0 = args[2]
            self.F = args[3]
            self.delta = args[4]
        else:  # otras posibles sobrecargas de constructores (opcional)
            pass

    def verificarCorregirCompletitudAFD():
        pass
    def hallarEstadosInaccesibles():
        pass
    def toString():
        pass
    def imprimirAFNLSimplificado():
        pass
    def exportar(archivo):
        pass
    def AFN_LambdaToAFN(afnl):
        pass
    def AFN_LambdaToAFD(afnl):
        pass
    def procesarCadena(cadena):
        return True
    def procesarCadenaConDetalles(cadena):
        pass
    def computarTodosLosProcesamientos(cadena, nombreArchivo):
        pass
    def procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla):
        pass
    def procesarCadenaConversion(cadena):
        pass
    def procesarCadenaConDetallesConversion(cadena):
        pass
    def procesarListaCadenasConversion(listaCadenas,nombreArchivo, imprimirPantalla): 
        pass