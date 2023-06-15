from AFD import AFD

def minimizar_dfa(delta, estados_finales):
    """
    Minimiza un DFA dado utilizando el algoritmo de minimización de estados.

    Args:
        delta (dict): Delta del DFA representado como un diccionario.
        estados_finales (set): Conjunto de estados finales del DFA.

    Returns:
        dict: DFA minimizado representado como un diccionario.

    """
    # Manipulacion de entrada, convertir conjuntos a strings
    new_delta ={}
    for estado in delta:
        new_delta[estado] = {}
    for simbolo in delta[estado]:
        new_delta[estado][simbolo] = delta[estado][simbolo].pop()
    # Paso 1: Crear pares de todos los estados involucrados
    delta = new_delta
    pares = []
    for estado1 in delta:
        for estado2 in delta:
            if estado1 != estado2:
                pares.append((estado1, estado2))

    marcados = set()  # Conjunto de pares marcados

    # Paso 2: Marcar pares donde uno es final y el otro no es final
    for par in pares:
        estado1, estado2 = par
        if (estado1 in estados_finales and estado2 not in estados_finales) or (estado2 in estados_finales and estado1 not in estados_finales):
            marcados.add(par)

    cambios = True

    # Paso 3: Marcar pares transitivamente
    while cambios:
        cambios = False
        for par in pares:
            estado1, estado2 = par

            for simbolo in delta[estado1]:
                if simbolo in delta[estado2]:
                    transicion1 = delta[estado1][simbolo]
                    transicion2 = delta[estado2][simbolo]
                    nuevo_par = (transicion1, transicion2)

                    if nuevo_par in marcados:
                        if par not in marcados:
                            marcados.add(par)
                            cambios = True

    # Paso 4: Construir el DFA minimizado
    dfa_minimizado = {}

    for par in pares:
        if par not in marcados:
            estado1, estado2 = par
            nuevo_estado = f'{estado1},{estado2}'
            dfa_minimizado[nuevo_estado] = {}
            for simbolo in delta[estado1]:
                if simbolo in delta[estado2]:
                    dfa_minimizado[nuevo_estado][simbolo] = f'{delta[estado1].get(simbolo, "")},{delta[estado2].get(simbolo, "")}'
                else:
                    dfa_minimizado[nuevo_estado][simbolo] = ""
    for x in dfa_minimizado:
        print(x)
    return dfa_minimizado
def imprimir_tabla(tabla):
    estados = sorted(list(set([estado for estado_pair in tabla for estado in estado_pair])))
    print('estados: \n', estados)
    # Imprimir encabezado de la tabla
    header = ' | '.join(estados)
    print(f'  | {header} ')

    # Imprimir separador de encabezado y contenido
    separator = '-' * (len(header) + 4)
    print(f'--|{separator}')

    # Imprimir contenido de la tabla
    for estado1 in estados:
        row = [estado1]
        for estado2 in estados:
            pair = (estado1, estado2)
            marcado = tabla.get(pair, 'nada')
            row.append(marcado)
        row_str = ' | '.join(row)
        print(row_str)


def imprimir_tabla2(tabla, afd):
    if tabla is None:
        print("La tabla es nula.")
        return
    print('keys de tabla: \n', tabla.keys())
    print('key/value de la tabla:\n')
    for clave, valor in tabla.items():
        print(clave,valor)
    estados = sorted(list(set([estado for estado_pair in tabla.keys() for estado in estado_pair.split(",")])))
    print('estados de imprimir2: \n', estados)
    # Imprimir encabezados de columnas
    print("| Estado  |  ", end="")
    simbolos = sorted(list(afdSimp.delta[estados[0]].keys()))
    for simbolo in simbolos:
        print(f"  {simbolo}  |", end="")
    print()

    # Imprimir separador de encabezados
    print("+---------", end="")
    for _ in simbolos:
        print("+-------", end="")
    print("+")

    # Imprimir filas de la tabla
    for estado in estados:
        print(f"|  {estado}   |", end="")
        for simbolo in simbolos:
            transicion = tabla[estado].get(simbolo, "")
            print(f"  {transicion}   |", end="")
        print()

    # Imprimir separador de filas
    print("+---------", end="")
    for _ in simbolos:
        print("+-------", end="")
    print("+")

afdSimp = AFD('ej4_simplificar_.dfa')
afdSimp.toString(graficar=True)

tabla = minimizar_dfa(afdSimp.delta, afdSimp.F)

imprimir_tabla2(tabla=tabla, afd=afdSimp)