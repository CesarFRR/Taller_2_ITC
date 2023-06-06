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
