class AFPD:
    def __init__(self, estados, estadoInicial, estadosAceptacion, alfabetoCinta, alfabetoPila, delta):
        self.estados = estados
        self.estadoInicial = estadoInicial
        self.estadosAceptacion = estadosAceptacion
        self.alfabetoCinta = alfabetoCinta
        self.alfabetoPila = alfabetoPila
        self.delta = delta

    def verificarDeterminismo(self):
        # Método para verificar que las transiciones dadas garanticen el determinismo del autómata.
        # Implementación pendiente.
        pass
        
    def procesarCadena(self, cadena):
        # Método para procesar una cadena de entrada en el autómata.
        estadoActual = self.estadoInicial
        pila = []
        
        for simbolo in cadena:
            if simbolo not in self.alfabetoCinta:
                return False
            
            transicionesPosibles = [transicion for transicion in self.delta if transicion[0] == estadoActual and 
                                    transicion[1] == simbolo and transicion[2] == pila[-1]]
            
            if len(transicionesPosibles) == 0:
                return False
            
            estadoActual, _, nuevoContenidoPila = transicionesPosibles[0]
            pila.pop()
            
            if nuevoContenidoPila != '':
                for simbolo in nuevoContenidoPila[::-1]:
                    pila.append(simbolo)
                    
        return estadoActual in self.estadosAceptacion and len(pila) == 0