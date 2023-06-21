# import json

# alphabet = None
# states =None
# initial = None
# accepting = None
# transitions = None
# afc = {}
# key = ''

# url= "ej1.afd"
# automata_tipo="afd"
# print("."+automata_tipo)
# if not url.endswith("."+ automata_tipo):
#       raise ValueError("El archivo proporcioando no es de formato ", automata_tipo)

# try:
#     with open(url, 'r',newline='', encoding='utf-8') as file:
#         contenido = (file.read()).replace('\r\n', '\n').replace('\r', '\n') #probelma de 
#         archivo = f'''{contenido}'''
#         for i in archivo.split('\n'):
#             print(i)
#             if i in ['#alphabet', '#states', '#initial', '#accepting', '#transitions']:
#                 key = i
#             elif i != '':
#                 if(key=='#alphabet'):
#                     print(i)
#                 afc.setdefault(key, []).append(i)
#         alphabet = afc['#alphabet']
#         states = afc['#states']
#         initial = afc['#initial'][0]
#         accepting = afc['#accepting']
#         transitions = afc['#transitions']

# except Exception as e:
#     print("Error: ", e)



# def validate_regex(s: str) -> bool:
#     return True



# print("\n\n en orden:\n")
# print("alfabeto: ", alphabet)
# print("estados: ", states)
# print("estado incial: ", initial)
# print("estados de aceptacion: ", accepting)
# print("transiciones (delta): ", transitions)

# #############################################################################
# pda_delta = {
#     'q0': {
#         'a': [['B', '$', 'q1']],
#         'b': [['B', '$', 'q0']]
#     },
#     'q1': {
#         'a': [['A', 'B', 'q0']],
#         'b': [['A', 'B', 'q2']]
#     },
#     'q2': {
#         'a': [['A', 'B', 'q2']],
#         'b': [['A', 'B', 'q1']]
#     }
# }

# afd_delta = {
#     'q0': {
#         'a': {'q2'},
#         'b': {'q0'}
#     },
#     'q1': {
#         'a': {'q0'},
#         'b': {'q3'}
#     },
#     'q2': {
#         'a': {'q2'},
#         'b': {'q1'}
#     }
# }

# pda_afd_product_delta = {}

# for pda_state in pda_delta:
#     for afd_state in afd_delta:
#         pda_afd_product_delta[(pda_state, afd_state)] = {}

#         for symbol in afd_delta[afd_state]:
#             pda_transitions = pda_delta[pda_state][symbol]

#             for pda_transition in pda_transitions:
#                 pda_afd_product_delta[(pda_state, afd_state)][symbol] = set()
#                 pda_afd_product_delta[(pda_state, afd_state)][symbol].add(pda_transition[2])

# for clave, valor in pda_afd_product_delta.items():
#     print(clave, ' : ', valor, '\n')


# arr = [10, 20, 30, 40, 50]
# a, b = arr[0], arr[1]

# print(a)  # Output: 10
# print(b)  # Output: 20
from AFD import AFD
from AFN_e import AFN_Lambda
from AFN import AFN
from MT import MT
from AFPD import AFPD
from AF2P import AF2P
from AFPN import AFPN
import random
from Graph import graficarAutomata
#print('Ejecutando:...\n')
#nfa1= AFN('ej1.nfa')
# nfa1.graficarAFN()
#dfa1 = nfa1.AFNtoAFD(nfa1)
#dfa1.graficarAutomata()
#nfa1.graficarAutomata()
#nfe1= AFN_Lambda('ej1.nfe')
#print(nfe1.procesarCadena('aab'))
#nfe1.graficarAutomata()
# cadenasx= []
# for i in range(70):
#     cadena= nfa1.Sigma.generarCadenaAleatoria(random.randint(0, 10))
#     cadenasx.append(cadena)

# for c in cadenasx:
#     print(c)

# print('ordenadas: \n')


# for c in sorted(cadenasx):
#     print(c)

# mi_lista = ['elemento1', 'elemento2', 'elemento3']
# index=0
# if index == 0:
#     mi_lista.insert(0, '!')  # Agregar '!' en la primera posición

# print(mi_lista)

# print('\nAFN_Lambda  a  AFD:\n')
# dfa0= nfe1.AFN_LambdaToAFD()
#print('PROBANDO:\n', nfe1.toString())
# print('\n')
# nfe1= nfe1.AFN_LambdaToAFN()
# print('\nnfeA AFN sin simplificar')
# print(nfe1.toString())
# print('\nnfeA AFN simplificado nfe1\n')
# print(nfe1.imprimirAFNSimplificado())
# print('\ndfa1 toString:\n')
# print(dfa1.toString())
# print('\nAFD (dfa1) simplificado:\n')
# print(dfa1.imprimirAFDSimplificado())

# tm1= MT('ej1.tm')
# # #print(tm1.toString())
# cadena2 = 'aabb'
# listaCadena= ['aabb', 'ab', 'bbbba', 'bbbaaa', 'abababa', 'a', 'b']
# # print('procesarCadena:\n')
# for c in listaCadena:
#     print(tm1.procesarCadena(c))
# print(tm1.procesarCadena(cadena2))
# # print('procesarCadenaConDetalles\n')
# # print(tm1.procesarCadenaConDetalles(cadena2))
# # print('procesarFunción\n')
# # print(tm1.procesarFunción(cadena2))
# # print('procesarListaCadenas\n')
# # tm1.procesarListaCadenas(listaCadenas=listaCadena,nombreArchivo='salidaDeImprimirlistaMT', imprimirPantalla=True)
# # print('graficarAutomata\n')
# # tm1.graficarAutomata()

# dpda1 = AFPD('ej1.dpda')
# dpda1.graficarAutomata()
# print()
# nfa1.graficarAutomata()
# graf1= graficarAutomata()
# graf1.exportarGrafo(automata=nfa1)
# listaM=[dfa1, nfa1, dpda1, tm1]

# graf1.exportarGrafos(listaAutomatas=listaM)

# pda2p_1= AF2P('ej1.msm')
# print('\n To string y graficar: \n')
# print(pda2p_1.toString(graficar=True))
import os, string, time


class InterfazConsola:
    automatas=None
    listaAutomatas=None
    listaNombreArchivos=None
    listaNombreArchivos2=None
    def __init__(self):
        self.automatas = []
        self.importarArchivosEntrada()


    def mostrar_menu(self):
        while True:
            menu= "\n----- MENÚ -----\nBienvenido, ésta interfaz se encarga de una rápida manipulación de todos los autómatas que usted ingrese a la carpeta /archivosEntrada, los autómatas son:\n"
            listaA=[]
            for i, elemento in enumerate(self.listaNombreArchivos):
                opcion = string.ascii_lowercase[i]
                listaA.append(f"{opcion}. {elemento}")
            self.listaNombreArchivos2
            menu+='\n'.join(listaA)
            print(menu)

            print("\nQue desea hacer?")
            print("1. procesarCadena")
            print("2. procesarCadenaConDetalles")
            print("3. procesarListaCadenas")
            print('4. Mostrar la información del autómata (toString)')
            print('5. Mostrar los grafos (se exportará un archivo pdf a /archivosSalida)')
            print("6. seleccionar un solo autómata")
            print("0. SALIR")
            opcion = self.filter(mode='int', args=[0, 6])

            if opcion == 1: #procesar cadena
                print("\nEscriba cuantas cadenas quiere que cada autómata procese (numero positivo de máximo 1 millón):")
                n=   self.filter(mode='int', args=[0, 1000000])
                print("\nEscriba que tan larga quiere que sea la cadena (numero positivo de máximo 1 millón):")
                l=   self.filter(mode='int', args=[0, 1000000])
                print('Se van a generar ',n, ' cadenas de tamaño ', l, ' para ', len(self.listaAutomatas), ' autómata(s) en los próximos 3 segundos:')
                time.sleep(3)

                for i,M in enumerate(self.listaAutomatas):
                    print(string.ascii_lowercase[i]+'. Autómata: ', M.nombreArchivo, M.extension)
                    for i in range(n):
                        c= M.Sigma.generarCadenaAleatoria(l)
                        print(c, M.procesarCadena(c))
                    print()
                pass
            elif opcion == 2:  #procesar cadena con detalles
                print("\nEscriba cuantas cadenas quiere que cada autómata procese (numero positivo de máximo 1 millón):")
                n=   self.filter(mode='int', args=[0, 1000000])
                print("\nEscriba que tan larga quiere que sea la cadena (numero positivo de máximo 1 millón):")
                l=   self.filter(mode='int', args=[0, 1000000])
                print('Se van a generar ',n, ' cadenas de tamaño ', l, ' para ', len(self.listaAutomatas), ' autómata(s) en los próximos 3 segundos:')
                time.sleep(3)

                for i,M in enumerate(self.listaAutomatas):
                    print(string.ascii_lowercase[i]+'. Autómata: ', M.nombreArchivo, M.extension)
                    for i in range(n):
                        c= M.Sigma.generarCadenaAleatoria(l)
                        print(c, M.procesarCadenaConDetalles(c))
                    print()
                pass
                pass
            elif opcion == 3:
                print("\nEscriba cuantas cadenas quiere que cada autómata procese (numero positivo de máximo 1 millón):")
                n=   self.filter(mode='int', args=[0, 1000000])
                print("\nEscriba que tan larga quiere que sea la cadena (numero positivo de máximo 1 millón):")
                l=   self.filter(mode='int', args=[0, 1000000])
                print('Se van a generar ',n, ' cadenas de tamaño ', l, ' para ', len(self.listaAutomatas), ' autómata(s) en los próximos 3 segundos:')
                time.sleep(3)

                for i,M in enumerate(self.listaAutomatas):
                    c=[]
                    for i in range(n):
                        c.append( M.Sigma.generarCadenaAleatoria(l))
                    print(string.ascii_lowercase[i]+'. Autómata: ', M.nombreArchivo, M.extension)
                    print(c, M.procesarListaCadenas(listaCadenas=c, imprimirPantalla=True))
                    print()
            elif opcion ==0:
                print('\nPrograma Terminado.\n')
                break



    def importarArchivosEntrada(self):
            carpeta= './archivosEntrada'
            nombres_archivos = []
            automatas=[]
            for nombre_archivo in os.listdir(carpeta):
                ruta_archivo = os.path.join(carpeta, nombre_archivo)
                if os.path.isfile(ruta_archivo):
                    nombre_archivo_sin_ruta = os.path.basename(ruta_archivo)
                    nombres_archivos.append(nombre_archivo_sin_ruta)
            for url in nombres_archivos:
                url=str(url)
                if(url.endswith('dfa')):
                    automatas.append(AFD(url))
                elif(url.endswith('nfa')):
                    automatas.append(AFN(url))
                elif(url.endswith('nfe')):
                    automatas.append(AFN_Lambda(url))
                elif(url.endswith('dpda')):
                    automatas.append(AFPD(url))
                elif(url.endswith('pda')):
                    automatas.append(AFPN(url))
                elif(url.endswith('msm')):
                    automatas.append(AF2P(url))
                elif(url.endswith('tm')):
                    automatas.append(MT(url))
            self.listaNombreArchivos= nombres_archivos
            self.listaAutomatas= automatas
            return automatas

    def filter(self, mode='int', args=[0,10]):
        if(mode=='int'):
            while True:
                opcion = input(">> ")
                if(opcion.isdigit()):
                    opcion= int(opcion)
                    if opcion >=  args[0] and opcion<=args[1]:
                        return opcion
        else:
            pass

# Ejemplo de uso

# afdSimp = AFD('ej4_simplificar_.dfa')
# afdSimp.toString(graficar=True)
# def obtener_nombres_archivos(carpeta):
#     nombres_archivos = []
#     for nombre_archivo in os.listdir(carpeta):
#         ruta_archivo = os.path.join(carpeta, nombre_archivo)
#         if os.path.isfile(ruta_archivo):
#             nombre_archivo_sin_ruta = os.path.basename(ruta_archivo)
#             nombres_archivos.append(nombre_archivo_sin_ruta)
#     return nombres_archivos

# # Ejemplo de uso
# carpeta_archivos = './archivosEntrada'
# nombres_archivos = obtener_nombres_archivos(carpeta_archivos)
# print(nombres_archivos)

ux = InterfazConsola().mostrar_menu()