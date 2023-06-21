from AFD import AFD
from prettytable import PrettyTable



def simplificar(afd1: AFD):
    afd = AFD(afd1)

    # SIMPLIFICAR USANDO UNA MATRIZ COMPLETA

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
                        if (matriz[indexQa][indexQb] !='E' and int(matriz[indexQa][indexQb])<ciclo ): # int(matriz[indexQa][indexQb])<ciclo hace que se registre el ultimo ciclo
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
    marcados.update(marcados0)

    # IMPRIMIR TABLA TRIANGULAR

    for i in range(n):
        for j in range(i+1):  # Solo imprime elementos hasta la diagonal principal
            if(i==j):
                print(estados[i], end=' |\n')
            else:
                print(matriz[j][i], end=" "*len(estados[i]) + "|" + " "*len(estados[i]) ) 
        print()  # Salto de línea después de cada fila

    # IMPRIMIR TABLA DEL DELTA

    noMarcados = totalParejas.difference(marcados)
    tabla = PrettyTable()
    simbolos=sorted(afd.Sigma.simbolos)
    encabezado=['{p,q}']
    for simb in simbolos:
        encabezado.append('{' + f'δ(p,{simb}),δ(q,{simb})' + '}')
    tabla.field_names = encabezado
    n= len(matriz)
    for i in range(n):
        for j in range(n):
            if (estados[i],estados[j]) in marcados:
                qa, qb = estados[i], estados[j]
                ciclo= int(matriz[i][j])
                filaTabla1=['{' + f'{qa},{qb}' + '}']
                if(ciclo >1 ):
                    filaTabla1[0] = filaTabla1[0]+ f' X {ciclo}'
                for simb in afd.Sigma.simbolos:
                    qaEv = list(delta[qa][simb])[0]
                    qbEv = list(delta[qb][simb])[0]
                    filaTabla1.append('{' + f'{qaEv},{qbEv}' + '}')
                tabla.add_row(filaTabla1)
            elif (estados[i],estados[j]) in noMarcados:
                filaTabla2=['{' + f'{qa},{qb}' + '}']
                for simb in afd.Sigma.simbolos:
                    qaEv = list(delta[qa][simb])[0]
                    qbEv = list(delta[qb][simb])[0]
                    filaTabla2.append('{' + f'{qaEv},{qbEv}' + '}')
                tabla.add_row(filaTabla2)
    print(tabla)

    # FUSIONAR ESTADOS EN EL DELTA ORIGINAL
    sorted_noMarcados =sorted(list(noMarcados))
    for qa, qb in sorted_noMarcados:
        estadoNext=set()
        new_key= '{'+f'{qa},{qb}'+'}'
        afd.delta[new_key]=dict()
        for simb in afd.Sigma.simbolos:
            afd.delta[new_key].update({simb:set()})
            estadoNext |=(delta[qa][simb])
            estadoNext |= (delta[qb][simb])
            if(len(estadoNext)==1):
                afd.delta[new_key][simb]={estadoNext.pop()}
            else:
                strQnext= '{'+",".join(sorted(list(estadoNext)))+'}'
                delta[new_key][simb].add(strQnext)

    for qa, qb in sorted_noMarcados:
        strQ= '{'+f'{qa},{qb}'+'}'
        if (qa in afd.F or qb in afd.F):
            afd.F.difference_update({qa,qb})
            afd.F.add(strQ)
        if (qa in afd.Q or qb in afd.Q):
            afd.Q.difference_update({qa,qb})
            afd.Q.add(strQ)
        for q in delta:
            for simb in delta[q]:
                trans= delta[q][simb].pop()
                if(trans!=None):
                    if(trans in {qa,qb}):
                        delta[q][simb]={strQ}
                    else:
                        delta[q][simb]={trans}
        del delta[qa]
        del delta[qb]
    afd.nombreArchivo=afd1.nombreArchivo + 'Simplificado'
    return afd

afd1 = AFD('ej4_simplificar_.dfa')

afd2 =simplificar(afd1)


afd1.toString(graficar=True)

afd2.toString(graficar=True)
#imprimir_matriz_adyacencia_triangular(matriz, Q)

#imprimir_tabla_delta_simplificar(matriz, marcados, noMarcados, afd1)


#fusionar_estados(afd1, noMarcados)

