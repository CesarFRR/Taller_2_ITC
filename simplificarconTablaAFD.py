from AFD import AFD
from prettytable import PrettyTable

def simplificar(afd: AFD):
    delta = afd.delta
    F= afd.F
    estados= sorted(list(afd.Q))
    n = len(estados)  # Tamaño de la matriz
    matriz = [['E'] * n for _ in range(n)]  # Inicializar matriz con 'E'

    # Paso 1: Crear los pares de estados involucrados en el DFA dado
    totalParejas=set()
    marcados0= set()
    # Paso 2: Marcar los pares (Qa, Qb) donde Qa está en F y Qb no está en F
    for i in range(n):
        totalParejas.update([  (estados[i],estados[x]) for x in range(n) if estados[i]!= estados[x] and i<x]  )
        for j in range(n):
            if (estados[i] in F) != (estados[j] in F):
                matriz[i][j] = '1'
                matriz[j][i] = '1'
                if (estados[i], estados[j]) not in marcados0 and (estados[j], estados[i]) not in marcados0 and estados[i]!=estados[j]:
                    marcados0.add( (estados[i], estados[j]))
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
                            print('ERROR, ESTADO NO ENCONTRADO: ', transQa, transQb)
                            marcado = False
                            break
                        transQa = transQa.get(simb, None)
                        transQb = transQb.get(simb, None)
                        if(not transQa) or (not transQb): # ...no exista, significa que esto conduce a un estado de no aceptación,
                            # por lo que el caso (qa, qb) de ese instante se descarta inmediatamente
                            # print('ERROR, SIMBOLO NO ENCONTRADO: ', transQa, transQb, 'simb: ', simb, 'originales qa y qb: ', qa, qb)
                            # print('delta de qa:', delta.get(qa, None), '\ndelta de qb: ', delta.get(qb, None))
                            marcado=False
                            break
                        if(transQa== transQb): # Se descarta tambien si el par es igual, ej: (q3,q3), esto no se usa en la matriz
                            marcado=False
                            break
                        indexQa= estados.index(list(transQa)[0])
                        indexQb= estados.index(list(transQb)[0])
                        if(indexQa>indexQb):
                            indexQa, indexQb = indexQb, indexQa
                        # Con comparar uno de los dos sectores de un q1,q2 de la matriz basta:
                        if (matriz[indexQa][indexQb] !='E' and int(matriz[indexQa][indexQb])<ciclo ): # no tengo ni idea de porque puse int(matriz[indexQa][indexQb])<ciclo, solo sé que si lo quito sale mal la tabla, que dios nos bendiga hablo enserio xd
                            cycle= str(ciclo)
                            matriz[i][j] = cycle
                            matriz[j][i] = cycle
                            marcado=True
                            break
                    if marcado and (qa, qb) not in nuevos_marcados and (qb,qa) not in nuevos_marcados:
                        if(qa=='q0' or qb=='q4'):
                            print('encontrados! B: ', qa, qb)
                        nuevos_marcados.add((qa, qb)) # se agrega a los nuevos (i,j) no se agrega (j,i) por redundancia

        if len(nuevos_marcados) == 0:
            break

        marcados.update(nuevos_marcados)
        ciclo += 1
 
    print('total n° de parejas: ', len(totalParejas)/2)
    marcados.update(marcados0)
    noMarcados =  totalParejas.difference(marcados)

    for qa, qb in sorted(list(noMarcados)): # AQUI SE DEBE HACER LA FUSION DE ESTAODS
        new_key= '{'+f'{qa},{qb}'+'}'
        #afd.delta[new_key]=

    return matriz, marcados, noMarcados# return: matriz, marcados, no marcados

def imprimir_matriz_adyacencia_triangular(matriz, simbolos):
    n = len(matriz)  # Tamaño de la matriz
    for i in range(n):
        for j in range(i+1):  # Solo imprime elementos hasta la diagonal principal
            if(i==j):
                print(simbolos[i])
            else:
                print(matriz[j][i], end=" ")
        print()  # Salto de línea después de cada fila



def imprimir_tabla_delta_simplificar(matriz, marcados, noMarcados, afd1):
    tabla = PrettyTable()
    # Agregar encabezados
    estados=sorted(list(afd1.Q))
    simbolos=sorted(afd1.Sigma.simbolos)
    encabezado=['{p,q}']
    for simb in simbolos:
        encabezado.append('{' + f'δ(p,{simb}),δ(q,{simb})' + '}')
    tabla.field_names = encabezado
    # for q in estados:
    #     if(afd1.delta.get(q)==None):
    #         continue
    #     fila=[q]
    #     for simb in simbolos:
    #         trans=list(afd1.delta[q].get(simb, ['∅']))
    #         fila.append(trans[0])
    #     tabla.add_row(fila)
    tabla.add_row(['pareja(p,q)', 'parejaEvaluadacon simb 0', 'parejaEvaluadacon simb 1'])
    print(tabla)

    pass



afd1 = AFD('ej4_simplificar_.dfa')

matriz, marcados, noMarcados = simplificar(afd=afd1)


#DE AQUI PARA ABAJO ES LO QUE PIDE EL PROFESOR EN CUANTO A LA IMAGEN Simplificación.png

# TODO: 
# cosas por hacer: falta fusionar los estados teniendo en cuenta los estados que no fueron marcados --> noMarcados
# Falta la tabla que piden en Simplificación.png
# Eso sería todo
print('\n')
imprimir_matriz_adyacencia_triangular(matriz=matriz, simbolos=sorted(list(afd1.Q)))
print('\n')


imprimir_tabla_delta_simplificar(matriz, marcados, noMarcados, afd1)