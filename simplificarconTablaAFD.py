from AFD import AFD


def simplificar(afd: AFD):
    delta = afd.delta
    F= afd.F
    estados= sorted(list(afd.Q))
    n = len(estados)  # Tamaño de la matriz
    matriz = [['E'] * n for _ in range(n)]  # Inicializar matriz con 'E'

    # Paso 1: Crear los pares de estados involucrados en el DFA dado
    

    # Paso 2: Marcar los pares (Qa, Qb) donde Qa está en F y Qb no está en F
    for i in range(n):
        for j in range(n):
            if (estados[i] in F) != (estados[j] in F):
                matriz[i][j] = '1'
                matriz[j][i] = '1'
    # print(estados, type(estados))
    # for i in matriz:
    #     print(f'[ {"  ,  ".join(i)} ]')

    # Paso 3: Marcar los pares (Qa, Qb) que cumplen la condición de transición marcada
    marcados = set()
    ciclo = 2

    while True:
        nuevos_marcados = set()

        for i in range(n):
            for j in range(n):
                if matriz[i][j] == 'E':
                    qa = estados[i]
                    qb = estados[j]
                    marcado = None
                    for simb in afd.Sigma.simbolos:
                        transQa= delta.get(qa, None)
                        transQb = delta.get(qb, None)
                        if(not transQa) or (not transQb): # Cualquier estado o cualquier simbolo que...
                            marcado = False
                            break
                        transQa = transQa.get(simb, None)
                        transQb = transQb.get(simb, None)
                        if(not transQa) or (not transQb): # ...no exista, significa que esto conduce a un estado de no aceptación,
                            # por lo que el caso (qa, qb) de ese instante se descarta inmediatamente
                            marcado=False
                            break
                        if(transQa== transQb): # Se descarta tambien si el par es igual, ej: (q3,q3), esto no se usa en la matriz
                            marcado=False
                            break
                        indexQa= estados.index(transQa.pop())
                        indexQb= estados.index(transQb.pop())
                        if (matriz[indexQa][indexQb] !='E'): # Con comparar uno de los dos sectores de un q1,q2 de la matriz basta
                            cycle= str(ciclo)
                            matriz[i][j] = cycle
                            matriz[j][i] = cycle
                            marcado=True
                            break

                    if marcado and (qa, qb) not in nuevos_marcados and (qb,qa) not in nuevos_marcados:
                        nuevos_marcados.add((qa, qb)) # se agrega a los nuevos (i,j) no se agrega (j,i) por redundancia

        if len(nuevos_marcados) == 0:
            break

        marcados.update(nuevos_marcados)
        ciclo += 1

    return matriz, marcados

def imprimir_matriz_adyacencia_triangular(matriz):
    n = len(matriz)  # Tamaño de la matriz
    #print('q0')
    #estados= ['q0','q1', 'q2', 'q3']
    #print(estados[0], end='')
    for i in range(n):
        
        for j in range(n):  # Solo imprime elementos hasta la diagonal principal
            #print('indexs: ', i,j)
            print(matriz[i][j], end=" ")
        #print(estados[i], end='')
        print()  # Salto de línea después de cada fila



afd1 = AFD('ej4_simplificar_.dfa')
matriz, marcados = simplificar(afd=afd1)
imprimir_matriz_adyacencia_triangular(matriz=matriz)
# Imprimir la matriz
# for i in matriz:
    # print(i)
#imprimir_matriz_adyacencia_triangular(matriz=matriz)
