from MT import MT
from AF2P import AF2P
from AFD import AFD
from AFN_e import AFN_Lambda
import os
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
#af2p1= AF2P('ej1.msm')
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
    print(mt1.procesarListaCadenas(cadenas, nombreArchivo=nombreArchivo, imprimirPantalla=True))

def MT_procesar_funcion(mt1:MT):
    print('Factor 33 - Procesar funcion:')
    cadenas = [mt1.Sigma.generarCadenaAleatoria(i) for i in range(0,11)]
    for c in cadenas:
        print('cadena: ',c,'Procesar funcion: ', mt1.procesarFunción(c))

#MT_construirDeArchivo('ej1.tm')
#mt1= MT('ej1.tm')
#MT_imprimirAutomata(mt1=mt1)
#MT_exportar_a_archivo(mt1=mt1, nombreArchivo='mt1EXPORTADO')
#MT_procesarEnDetalle(mt1=mt1)
#MT_procesar_lista_cadenas(mt1=mt1, nombreArchivo='listaCadenaMT1')
#MT_procesar_funcion(mt1=mt1)
#===================================================================#



# afd1= AFD('noContieneBB.dfa')
# afd2= AFD('impares.dfa')
#a que se refiere
# afdCartesianoY = afd1.AFD_hallarProductoCartesianoY(afd1,afd2)
# como es para afn lambda el codigo que usted usó para su parte, que con solo enter saltaba a la otra funcionalidad


input ()
 
print("Factor 25 construir desde archivo:")
nfe = AFN_Lambda('ej2.nfe')
nfe.graficarAutomata()

input ()
try:
    print("Factor 26 lambda clausura para un estado:")
    nfe.lambda_clausura(nfe.q0, imprimir=True)
except:
    pass


input ()
try:
    print("Factor 27 lambda clausura para varios estados:")
    nfe.lambda_clausura(nfe.Q, imprimir=True)
except:
    pass



input ()
try:
    print("Factor 28 inaccesibles:")
    print(nfe.hallarEstadosInaccesibles())
except:
    pass


try:
    print("Factor 29 imprimir automata:")
    print(nfe.imprimirAFNLSimplificado())
except:
    pass
input ()
 



input ()
try:
    print("Factor 30 export:")
    print(nfe.exportar('NFE_EXPORTADO'))
except:
    pass

try:
    print("Factor 31 procesar en detalle:")
    print(nfe.procesarCadenaConDetalles(cadena))
except:
    pass
cadena='aabbbca'
input ()
try:
    print("Factor 32 computar todos los proc:")
    print(nfe.computarTodosLosProcesamientos(cadena=cadena, nombreArchivo='NFE_computado'))
except:
    pass




input ()
try:
    print("Factor 33 lista cadenas:")
    print(nfe.procesarListaCadenas(lista))
except:
    pass


lista=['aabba', 'sasd', 'ccaac',' aaccaba']
input ()
try:
    print("Factor 34 to AFN")
    afn1= nfe.AFN_LambdaToAFN(nfe1=nfe, imprimir=True)
    print(afn1.toString(graficar=True))
except:
    pass



input ()
try:
    print("Factor 35 to afd:")
    afd1= nfe.AFN_LambdaToAFD(nfe1=nfe, imprimir=True)
    print(afd1.toString(graficar=True))
except:
    pass


input ()
try:
 
    print("Factor 36 to afd y procesar con detalles:")
    print(nfe.procesarCadenaConDetallesConversion(cadena=cadena))
except:
    pass


input ()



input ()
 
print("Factor 37 to afd y procesar lista con detalles:")
nfe.procesarListaCadenasConversion(listaCadenas=lista)

input ()
 
print("Factor 38 manejo alfabeto:")
print(nfe.Sigma.simbolos, type(nfe.Sigma.simbolos))

input ()
 
print("Factor 39 validacion afn to afd:")
print(nfe.delta)
print(afd1.delta)
nfe.graficarAutomata()
afd1.graficarAutomata()

input ()
 
print("Factor 40 validacion afn to afn:")
print(nfe.delta)
print(afn1.delta)
nfe.graficarAutomata()
afn1.graficarAutomata()




# es esnecillo solo es un input para cada enter, limpiar la pantalla antes de ejecutar cada funcion y luego imprimir