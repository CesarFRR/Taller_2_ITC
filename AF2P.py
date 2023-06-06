class AF2P:
    def __init__(self, estados, estado_inicial, estados_aceptacion, alfabeto_cinta, alfabeto_pila, delta):
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.alfabeto_cinta = alfabeto_cinta
        self.alfabeto_pila = alfabeto_pila
        self.delta = delta

    def es_aceptada(self, cadena):
        pila1 = []
        pila2 = []
        estado_actual = self.estado_inicial

        for simbolo in cadena:
            if simbolo not in self.alfabeto_cinta:
                return False

            if (estado_actual, simbolo,
                    pila1[-1] if len(pila1) > 0 else None,
                    pila2[-1] if len(pila2) > 0 else None) not in self.delta:
                return False

            siguiente_estado, push1, push2 = self.delta[(estado_actual, simbolo,
                                                          pila1[-1] if len(pila1) > 0 else None,
                                                          pila2[-1] if len(pila2) > 0 else None)]

            estado_actual = siguiente_estado

            if push1 is not None:
                pila1.append(push1)

            if push2 is not None:
                pila2.append(push2)

        return estado_actual in self.estados_aceptacion and len(pila1) == 0 and len(pila2) == 0