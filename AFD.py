from Alfabeto import Alfabeto
import re


class AFD:
    Sigma = None  # se intentará hacer el delta como  un diccionario en esta rama, debido a la complejidad del taller
    Q = None
    q0 = None
    F = None
    delta = {}
    estadosLimbo = None
    estadosInaccesibles = None
    automata_tipo = "afd"
    etiquetas=['#!dfa', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
    # def __init__(self, alfabeto, estados, estadoInicial, estadosAceptacion, delta):
    #     self.Sigma = alfabeto
    #     self.Q = estados
    #     self.q0 = estadoInicial
    #     self.F = estadosAceptacion
    #     self.delta = delta

    def __init__(self, *args):
        if (len(args) == 1):  # Inicializar por archivo txt
            automata_tipo = "dfa"
            if (not args[0].endswith("." + automata_tipo)):
                raise ValueError(
                    "El archivo proporcioando no es de formato ", automata_tipo)
            try:
                afc = {}
                key = ''
                with open(args[0], 'r', newline='', encoding='utf-8') as file:
                    file = file.read().replace('\r\n', '\n').replace('\r', '\n')  # problema de saltos de linea solucionados
                    string= f'''{file}'''
                    if(not string.startswith(self.etiquetas[0])):
                        print("si empieza con: ", self.etiquetas[0])
                    dictReader={}
                    for i in string.split('\n'):
                        if i in self.etiquetas[1:]:
                            key = i
                        elif i != '':
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")):
                                afc.setdefault(key, []).append(i)
                            elif(key=='#transitions' and i.split(":")[1].split(">")[0]!="$"):
                                trans=re.split(r"[:>]", i)
                                #print("transition: ", trans, "\nLength: ", len(trans))
                                if(len(trans)!=3): raise ValueError("transición inválida: ", i)
                                afc.setdefault(key, []).append(i)
                                print("\n trans: ", trans )
                                if(trans[0] in dictReader and trans[2] in dictReader[trans[0]]): #si existe ese Q y ya existe la etiqueta evaluada...
                                    raise ValueError("transición inválida --> AFD: no pueden haber dos transiciones de ", trans[0], " para la misma etiqueta ", trans[2], " --> ", i)
                                elif(trans[0] in dictReader):
                                    dictReader.setdefault(key, []).append(i)
                                    print("\n trans: ", trans )
                                    dictReader.setdefault(dictReader[trans[0]], {}).update({trans[1]:trans[2]}) #ej: para (q2, b)--> q5 ==> self.delta.setdefault("q2", {}).update({ "b": q5 })
                                    #setdefault --> si no existe la clave "key" se crea una con valor [] --> "key":[]
                    
                    self.Sigma = Alfabeto([afc['#alphabet'][0]])
                    self.Q = afc['#states']
                    self.q0 = afc['#initial'][0]
                    self.F = afc['#accepting']
                    self.delta = dictReader
                    print("dictreader: ", dictReader)
            
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)

        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma = args[0]
            self.Q = args[1]
            self.q0 = args[2]
            self.F = args[3]
            self.delta = args[4]
        # print("\n\n en orden:\n")
        # print("alfabeto: ", self.Sigma.toStringEntrada())
        # print("estados: ", self.Q)
        # print("estado incial: ", self.q0)
        # print("estados de aceptacion: ", self.F)
        #print("transiciones (delta): ", self.delta)
    def verificarCorregirCompletitudAFD(self):
        pass

    def hallarEstadosLimbo(self):
        pass

    def hallarEstadosInaccesibles(self):
        pass

    def toString(self):
        delta="d"
        #print("dellta: ", self.delta)
        for claveExterna, valorExterno in self.delta.items():
            print(4)
            for claveInterna, valorInterno in valorExterno.items():
                print("v"+claveExterna.toString())
                print(3)
                delta=delta+str(claveExterna)+":"+str(claveExterna)+">"+str(valorInterno)
        #print("asas--> ",delta)
        #print("delta: ", type(delta), "Q: ", type(self.Q), "aceptacion: ", type(self.F), "delta: ", delta)
        return ""#self.Sigma.formato_entrada+"\n".join(self.Q)+"\n"+self.q0+"\n".join(self.F)+delta

    def imprimirAFDSimplificado(self):
        pass

    def exportar(self, archivo):
        pass

    def procesarCadena(self, cadena):
        return True

    def procesarCadenaConDetalles(self, cadena):
        return True

    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        pass

    def AFD_hallarComplemento(self, afdInput: "AFD"):
        pass

    def AFD_hallarProductoCartesianoY(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesianoO(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesianoDiferencia(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesianoDiferenciaSimétrica(self, afd1: "AFD", afd2: "AFD"):
        pass

    def AFD_hallarProductoCartesiano(self, afd1: "AFD", afd2: "AFD", StringOperacion):
        pass

    def AFD_simplificarAFD(self, afdinput: "AFD"):
        pass

print('Ejecutando:...')
afd1= AFD("ej1.dfa")
print(afd1.toString())
# se pudo?
# sirve? haga algo y dele ctr s, se guardo en mi pc, el punto blanco se fue, sirve , por cierto, instalese el tabNine, es una IA que le ayuda a codear mas rapido
# listo, aunque ya lo tenia pero se borro xd
# Tabnine AI, aaah ya, cierto, lo otro e que se puede hablar por meet, mmm, si eso seria todo, aaah, reunirnos a tal hora para abrir el live share y sale
# pero ya sabemos que funciona
