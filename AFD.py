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
    def procesarCadena(cadena):   #Procesar cadena con delta como un diccionario
        actual = self.q0
        for i in cadena:
            if i not in self.Sigma:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                return False
            if self.delta.get(actual) is not None:  #Verificar que el estado actual exista
                transicion = self.delta[actual]    #Lista de transiciones del estado actual
                for j in transicion:    
                    if i in j: #Recorrer las transiciones verificando el simbolo actual y el estado resultado
                        actual = j[1] #Realizar transicion                    
                        break
                        
        if actual in self.F: #verificar si el estado actual es de aceptacion
            return True
        else:
            return False   
    
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

#Prueba
x = AFD(['a','b'], ['q0','q1'],'q0',['q0'],{'q0':[['a','q1'],['b','q1']],'q1':[['a','q0'],['b','q0']]})#Automata que recibe cadenas con numero par de simbolos
#Formato de delta: diccionario donde las keys son cada uno de los estados y los valores una matriz de los simbolos y la transicion de cada uno
#Por ej: 'q0':[['a','q1'],['b','q1']] --> q0 es el estado, con a lleva a q1 y b a q2
cadena = input('ingrese una cadena: ')
print(x.procesarCadena(cadena))
