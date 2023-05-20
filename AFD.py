from Alfabeto import Alfabeto
import re, copy
import AFN
class AFD:
    Sigma = None  
    Q = None
    q0 = None
    F = None
    delta = None # se intentará hacer el delta como  un diccionario, cada estado q contiene otro diccionario --> clave:simbolo, valor: conjunto de estados resultantes tras evaluar con la funcion delta
    estadosLimbo = None
    estadosInaccesibles = None
    extension = "dfa"
    etiquetas=['#!dfa', '#alphabet', '#states', '#initial', '#accepting', '#transitions']
    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], str)):  # Inicializar por archivo txt
            if (not args[0].endswith("." + self.extension)):raise ValueError("El archivo proporcioando no es de formato ", self.extension)
            try:
                afc = {}
                key = ''
                with open(args[0], 'r', newline='', encoding='utf-8') as file:
                    file = file.read().replace('\r\n', '\n').replace('\r', '\n')  # problema de saltos de linea solucionados
                    string= f'''{file}'''
                    dictReader={}
                    afc={}
                    for i in string.split('\n'):
                        if i in self.etiquetas[1:]:
                            key = i
                        elif i != '':
                            if(key!='#transitions' and Alfabeto.validate_regex(i,r"^[^#;\n]+$")): # regex para que los estados no contengan ";", "#" ni \n
                                afc.setdefault(key, []).append(i)
                            elif key== '#transitions' and i.split(":")[1].split(">")[0]!= "$": # AFD: no contiene transiciones lambda
                                trans=re.split(r"[:>]", i)
                                if(len(trans)!=3 or ';' in trans[2]): raise ValueError("transición inválida: ", i) # "; " q no puede tener varias salidas con un simbolo
                                estado, simbolo, deltaResultado = trans
                                #print('trans: ', trans)
                                #===================================================================#
                                valor=dictReader.get(estado)
                                #print("i: ", i, " key: ", key, " trans", trans, " valor: ", valor)
                                if(valor==None): #No existe el estado? crearlo y agregar { simbolo:deltaResultado }
                                    dictReader[estado]={simbolo: set({deltaResultado}) }
                                else:
                                    dictReader[estado].update({simbolo:set({deltaResultado})})
                    self.Sigma = Alfabeto([afc['#alphabet'][0]])
                    self.Q = set(afc['#states'])
                    self.q0 = afc['#initial'][0]
                    self.F = set(afc['#accepting'])
                    self.delta = dictReader
                    #print('delta: ', self.delta)
            except Exception as e:
                print("Error en la lectura y procesamiento del archivo: ", e)
        elif (len(args) == 5):  # Inicializar por los 5 parametros: alfabeto, estados, estadoInicial, estadosAceptacion, delta
            self.Sigma, self.Q, self.qo, self.F, self.delta = args
            self.Q=set(self.Q)
        elif(len(args) == 0 and isinstance(args[0], AFD)):
            self.Sigma=copy.deepcopy(args[0].Sigma)
            self.Q=copy.deepcopy(args[0].Q)
            self.qo=args[0].q0
            self.F=copy.deepcopy(args[0].F)
            self.delta=copy.deepcopy(args[0].delta)
            self.extension=args[0].extension
            self.estadosInaccesibles=copy.deepcopy(args[0].estadosInaccesibles)
            self.estadosLimbo=copy.deepcopy(args[0].estadosLimbo)
            self.etiquetas=args[0].etiquetas
            pass
        self.estadosLimbo = set()
        self.estadosInaccesibles=set()
        self.verificarCorregirCompletitudAFD()
        self.hallarEstadosLimbo()

    def verificarCorregirCompletitudAFD(self):
        limbo = { 'L':{  s: set('L') for s in self.Sigma.simbolos} }
        faltalimbo=False
        for estado in self.delta:
            for simb in self.Sigma.simbolos:
                if(self.delta[estado].get(simb)==None):
                    if(not 'L' in self.delta.keys()): faltalimbo = True
                    self.delta[estado][simb]=limbo
                    self.estadosLimbo.add('L')

        if faltalimbo: self.delta.update(limbo)
        #print('verificarCorregirCompletitudAFD(): \n', self.toString())
        out = self.toString() #.get() retorna el conjunto del simbolo dado, si no existe retorna un conjunto vacío (esto es para evitar errores de KeyError: clave no encontrada)

    def hallarEstadosLimbo(self):
        if (self.estadosLimbo==None):
            #print('estadosLimbo= None!!!!')
            self.estadoslimbo =set()
        for estado in self.delta:
            if all( self.delta[estado][simb]=={estado} for simb in self.Sigma.simbolos):
                #estado limbo encontrado!
                if(estado==self.q0): raise ValueError('El estado inicial no puede ser un estado limbo')
                self.estadosLimbo.add(estado)
                self.Q.add(estado)

        #print('hallarEstadosLimbo(): \n', self.estadosLimbo , ' Q: ', self.Q)
    def hallarEstadosInaccesibles(self):
        pass

    def toString(self):
        simb=''
        out=self.etiquetas[0] + '\n' + self.etiquetas[1] +'\n'+self.Sigma.toStringEntrada()+'\n'+ self.etiquetas[2]+'\n'+'\n'.join(sorted(list(self.Q)))+'\n'+self.etiquetas[3] + '\n'+self.q0+'\n'+ self.etiquetas[4]+'\n'+ '\n'.join(sorted(list(self.F)))+ '\n'+ self.etiquetas[5]
        deltaLinea=''
        for q in self.delta:
            for simb in self.delta[q]:
                deltaSet= list(self.delta[q][simb])[0]
                deltaLinea=f'{q}:{simb}>{deltaSet}'
                out+='\n'+deltaLinea
                #print ('deltaLinea: ',deltaLinea)
        return out

    def imprimirAFDSimplificado(self):
        pass

    def exportar(self, archivo):
        with open(archivo, "w") as f:
                f.write(self.toString())

    def procesarCadena(self, cadena):   #Procesar cadena con delta como un diccionario
            actual = self.q0
            for i in cadena:
                if i not in self.Sigma:  #Comprobar que el simbolo leido se encuentre en el alfabeto
                    return False
                if self.delta.get(actual) is not None:  #Verificar que el estado actual exista
                    transicion = self.delta[actual]    #Lista de transiciones del estado actual
                    for j in transicion:    
                        if i in j: #Recorrer las transiciones verificando el simbolo actual y el estado resultado
                            actual = j[1] #Realizar transicion                    
                            break
                            
            if actual in self.F: #verificar si el estado actual es de aceptacion
                return True
            else:
                return False   

    def procesarCadenaConDetalles(self, cadena):
        return True

    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        pass

    def AFD_hallarComplemento(self, afdInput: "AFD"):
        print("hallando complemento: \n")
        complemento= AFD(afdInput)
        nuevosEstadosF= self.Q.difference(self.F)
        complemento.F=nuevosEstadosF
        return complemento

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

    def pruebas(self, cadena):
        out=''
        #print("usando delta: \n")
        limbo = { 'L':{  s: set('L') for s in self.Sigma.simbolos} }
        #print('limbo: ', limbo)
        for estado in self.delta:
            for simb in self.Sigma.simbolos:
                if(self.delta[estado].get(simb)==None):
                    self.delta[estado][simb]=limbo
        
        out = self.toString() #.get() retorna el conjunto del simbolo dado, si no existe retorna un conjunto vacío (esto es para evitar errores de KeyError: clave no encontrada)
        return out

#================================================

print('Ejecutando:...\n')
afd1= AFD("ej1.dfa")
#print(afd1.toString())
#afd1.toString()
print('\n')
afd1.exportar("ej2.dfa")
