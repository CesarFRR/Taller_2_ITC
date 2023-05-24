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

    def validar_conexion(self, nodo_inicial, nodo_final):
        visitados = set()  # Conjunto para almacenar los nodos visitados
        pila = [nodo_inicial]  # Pila para almacenar los nodos a explorar

        while pila:
            nodo_actual = pila.pop()

            if nodo_actual == nodo_final:
                return True  # Se encontró una conexión entre los nodos

            visitados.add(nodo_actual)

            if nodo_actual in self.delta:
                conexiones = self.delta[nodo_actual]  # Obtener las conexiones del nodo actual en el grafo
                for simbolo, destinos in conexiones.items():
                    for siguiente_nodo in destinos:
                        if siguiente_nodo not in visitados:
                            pila.append(siguiente_nodo)

        return False  # No se encontró una conexión entre los nodos

    def hallarEstadosInaccesibles(self):
        estadosInaccesibles = []
        for state in self.Q:
            if not self.validar_conexion(self.q0, state):
                estadosInaccesibles.append(state)
        self.estadosInaccesibles = estadosInaccesibles
        return estadosInaccesibles

    def toString(self):
        resultado = ""

        resultado += "#!nfa\n"

        # Agregar #alphabet
        resultado += "#alphabet\n"
        resultado += "-".join(self.Sigma) + "\n"

        # Agregar #states
        resultado += "#states\n"
        for state in self.Q:
            resultado += state + "\n"

        # Agregar #initial
        resultado += "#initial\n"
        resultado += self.q0 + "\n"

        # Agregar #accepting
        resultado += "#accepting\n"
        for state in self.F:
            resultado += state + "\n"
        resultado += "#transitions\n"
        transitions = self.delta
        for state in transitions:
            for symbol in transitions[state]:
                targets = transitions[state][symbol]
                targets_str = ";".join(targets)
                resultado += f"{state}:{symbol}>{targets_str}\n"

        return resultado

    def imprimirAFNSimplificado():
        pass
    
    def exportar(archivo):
        pass

    def AFD_AFNtoAFD(afn):
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




M = AFN(
        ['a','b'],      #Alfabeto de la Cinta
        ['q0','q1'],    #Estados Internos   
        'q0',           #Estado Inicial
        ['q1'],         #Estados finales o de aceptacion
        {'q0': {'a': ['q1'], 'b': ['q0', 'q1']}} # Funcion de Trancision
    )

print (f"Automata M:\n{str(M.toString())}")
print (f"Estados Innacesibles: {str(M.hallarEstadosInaccesibles())}")