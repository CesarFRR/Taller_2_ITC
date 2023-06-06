class AFPN:
    pila=None
    def __init__(self, estados, estadoInicial, estadosAceptacion, alfabetoCinta, alfabetoPila, delta):
        self.estados = estados
        self.estadoInicial = estadoInicial
        self.estadosAceptacion = estadosAceptacion
        self.alfabetoCinta = alfabetoCinta
        self.alfabetoPila = alfabetoPila
        self.delta = delta

    def procesarCadena(self, cadena):
        # Método para procesar una cadena de entrada en el autómata.
        estadosActuales = [self.estadoInicial]
        
        for simbolo in cadena:
            nuevosEstadosActuales = []
            
            for estadoActual in estadosActuales:
                transicionesPosibles = [transicion for transicion in self.delta if transicion[0] == estadoActual and 
                                        transicion[1] == simbolo and transicion[2] == self.pila[-1]]
                
                for transicion in transicionesPosibles:
                    nuevoEstadoActual, _, nuevoContenidoPila = transicion
                    
                    if nuevoEstadoActual not in nuevosEstadosActuales:
                        nuevosEstadosActuales.append(nuevoEstadoActual)
                        
                    if nuevoContenidoPila != '':
                        for simbolo in nuevoContenidoPila[::-1]:
                            self.pila.append(simbolo)
                            
            estadosActuales = nuevosEstadosActuales
            
        return any(estadoActual in self.estadosAceptacion for estadoActual in estadosActuales) and len(self.pila) == 0