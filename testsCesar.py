from MT import MT
from AF2P import AF2P
mt1=None
af2p1=None
#===================================================================#
def AF2P_construirDeArchivo(nombreArchivo):
    print('Factor 16 - Construir de archivo:')
    af2p1 = AF2P(nombreArchivo)
    #af2p1.graficarAutomata()
    print('\n',af2p1.delta)
    return af2p1

def AF2P_imprimirAutomata(af2p1:AF2P):
    print('Factor 17 - Imprimir autómata:')
    print(af2p1.toString())

def AF2P_exportar_a_archivo(af2p1:AF2P, nombreArchivo):
    print('Factor 18 - Exportar autómata a archivo:')
    af2p1.exportar(nombreArchivo)


#af2p1= AF2P_construirDeArchivo('ej1.msm')
af2p1= AF2P('ej1.msm')
#AF2P_imprimirAutomata(af2p1)
#AF2P_exportar_a_archivo(af2p1, 'ej1EXPORTADO')

#===================================================================#

def MT_construirDeArchivo(nombreArchivo):
    print('Factor 28 - Construir de archivo:')
    mt1 = MT(nombreArchivo)
    mt1.graficarAutomata()
    return mt1

def MT_imprimirAutomata(mt1:MT):
    print('Factor 29 - Imprimir autómata:')
    print(mt1.toString())

def MT_exportar_a_archivo(mt1:MT, nombreArchivo):
    print('Factor 30 - Exportar autómata a archivo:')
    mt1.exportar(nombreArchivo)

def MT_procesarEnDetalle(mt1:MT):
    print('Factor 31 - Procesar en detalle:')
    cadenas = [mt1.Sigma.generarCadenaAleatoria(i) for i in range(0,11)]
    for c in cadenas:
        print(mt1.procesarCadenaConDetalles(c))
    
def MT_procesar_lista_cadenas(mt1:MT, nombreArchivo):
    print('Factor 32 - Procesar lista de cadenas:')
    cadenas = [mt1.Sigma.generarCadenaAleatoria(i) for i in range(0,11)]
    print(mt1.procesarCadenaConDetalles(cadenas))

def MT_procesar_funcion(mt1:MT, nombreArchivo):
    print('Factor 33 - Procesar función:')
    cadenas = [mt1.Sigma.generarCadenaAleatoria(i) for i in range(0,11)]
    for c in cadenas:
        print('cadena: ',c,'Procesar función: ', mt1.procesarFunción(c))

MT_construirDeArchivo('ej1.tm')

#===================================================================#