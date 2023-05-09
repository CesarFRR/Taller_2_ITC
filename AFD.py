class AFD:
    Sigma=None
    Q=None
    q0=None
    F=None
    delta =[]
    estadosLimbo=None
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
    def hallarEstadosLimbo():
        pass
    def hallarEstadosInaccesibles():
        pass
    def toString():
        pass
    def imprimirAFDSimplificado():
        pass
    def exportar(archivo):
        pass
    def procesarCadena(cadena):
        return True
    def procesarCadenaConDetalles(cadena):
        return True
    def procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla):
        pass
    def AFD_hallarComplemento(afdInput):
        pass
    def AFD_hallarProductoCartesianoY(afd1: AFD,afd2: AFD):
        pass
    def AFD_hallarProductoCartesianoO(afd1: AFD, afd2: AFD):
        pass
    def AFD_hallarProductoCartesianoDiferencia(afd1: AFD, afd2: AFD):
        pass
    def AFD_hallarProductoCartesianoDiferenciaSimétrica(afd1: AFD, afd2: AFD):
        pass
    def AFD_hallarProductoCartesiano(afd1: AFD,afd2: AFD, StringOperacion):
        pass
    def AFD_simplificarAFD(afdinput: AFD):
        pass

print('a')

    #se pudo?
    #sirve? haga algo y dele ctr s, se guardo en mi pc, el punto blanco se fue, sirve , por cierto, instalese el tabNine, es una IA que le ayuda a codear mas rapido
    #listo, aunque ya lo tenia pero se borro xd
    # Tabnine AI, aaah ya, cierto, lo otro e que se puede hablar por meet, mmm, si eso seria todo, aaah, reunirnos a tal hora para abrir el live share y sale
    #pero ya sabemos que funciona