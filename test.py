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


def procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla):
    if not nombreArchivo:
        nombreArchivo = "default.txt"

    with open(nombreArchivo, "w") as f:
        for cadena in listaCadenas:
            # Realizar procesamiento de la cadena y obtener los resultados
            aceptacion = True
            num_posibles_procesamientos = 10
            num_procesamientos_aceptacion = 5
            num_procesamientos_rechazo = 5

            # Construir la línea de salida con los campos separados por tabulación
            linea = f"{cadena}\t{aceptacion}\t{num_posibles_procesamientos}\t{num_procesamientos_aceptacion}\t{num_procesamientos_rechazo}\t{'yes' if aceptacion else 'no'}\n"

            # Escribir la línea en el archivo
            f.write(linea)

            # Imprimir la línea en pantalla si imprimirPantalla es True
            if imprimirPantalla:
                print(linea, end="")

# Ejemplo de uso
listaCadenas = ["abc", "def", "xyz"]
nombreArchivo = "resultados.txt"
imprimirPantalla = True

procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla)
