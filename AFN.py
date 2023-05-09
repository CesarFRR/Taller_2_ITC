class AFN:
    Sigma = None
    Q = None
    q0 = None
    F = None
    delta = []
    estadosInaccesibles = None

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

    def hallarEstadosInaccesibles():
        pass

    def toString():
        pass

    def imprimirAFNSimplificado():
        pass
    
    def exportar(archivo):
        pass

    def AFD_AFNtoAFD(afn: AFN):
        pass

    def procesarCadena(cadena):
        return True

    def procesarCadenaConDetalles(cadena):
        return True

    def computarTodosLosProcesamientos(cadena, nombreArchivo):
        return 0
    def procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla):
        pass

    def procesarCadenaConversion(cadena):
        return True
    
    def  procesarCadenaConDetallesConversion(cadena):
        return True
    
    def procesarListaCadenasConversion(listaCadenas,nombreArchivo, imprimirPantalla):
        pass

    # =============================



print('a')

# se pudo?
# sirve? haga algo y dele ctr s, se guardo en mi pc, el punto blanco se fue, sirve , por cierto, instalese el tabNine, es una IA que le ayuda a codear mas rapido
# listo, aunque ya lo tenia pero se borro xd
# Tabnine AI, aaah ya, cierto, lo otro e que se puede hablar por meet, mmm, si eso seria todo, aaah, reunirnos a tal hora para abrir el live share y sale
# pero ya sabemos que funciona
