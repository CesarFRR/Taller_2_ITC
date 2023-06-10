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
#print('Ejecutando:...\n')
nfa1= AFN("ej1.nfa")
# nfa1.graficarAFN()
dfa1 = nfa1.AFNtoAFD(nfa1)
nfe1= AFN_Lambda('ej1.nfe')
print('\n')
#print('PROBANDO:\n', nfe1.toString())
print('\n')
nfe1= nfe1.AFN_LambdaToAFN()
print('\nnfeA AFN sin simplificar')
print(nfe1.toString())
print('\nnfeA AFN simplificado nfe1\n')
print(nfe1.imprimirAFNSimplificado())

print(dfa1.toString())
print('\n')