class nonBinaryTree():
    def __init__(self, val):
        self.val = val
        self.children = []
        self.leaf = True
        self.rutas = []
    
    def insert(self, val):
        self.children.append(nonBinaryTree(val))
        self.leaf = False


    def recorrer(self,  tree, rutas = None, ruta = None):
        if rutas == None:
            rutas = []
        if ruta == None:
            ruta = []
        ruta.append(tree.val)
        
        if tree.leaf == True:
            rutas.append(ruta.copy())
            return ruta
        elif tree.leaf == False:
            for i in tree.children:
                self.recorrer(i, rutas, ruta)
                ruta.pop()
            return rutas
        
            
    def __repr__(self):
        return f' {self.val}:{self.children}'

class nonBinaryTreePila():
    def __init__(self, val1, val2, val3):
        self.val = (val1, val2, val3)
        self.children = []
        self.leaf = True
        self.rutas = []
    
    def insert(self, val1,val2,val3):
        self.children.append(nonBinaryTreePila(val1,val2,val3))
        self.leaf = False


    def recorrer(self,  tree, rutas = None, ruta = None):
        if rutas == None:
            rutas = []
        if ruta == None:
            ruta = []
        ruta.append(tree.val)
        
        if tree.leaf == True:
            rutas.append(ruta.copy())
            return ruta
        elif tree.leaf == False:
            for i in tree.children:
                self.recorrer(i, rutas, ruta)
                ruta.pop()
            return rutas
        
            
    def __repr__(self):
        return f' {self.val}:{self.children}'

# transitions = {'q0':{'a':{'q0','q1'},'b':{'q0','q2'} }, 'q1':{'a':{'q1','q2'}}, 'q2':{'a':{'q2','q0'}, 'b':{'q1','q2'}}}

# actual = 'q0'
# Mayortree = nonBinaryTree(actual)
# cadena = 'abbb'
# estados = transitions.keys()


# def recorrerCadena(cadena, tree):
#     for index, simbolo in enumerate(cadena):
#         if transitions.get(tree.val) is not None:
#             if transitions[tree.val].get(simbolo) is not None:
#                 for i in sorted(transitions[tree.val][simbolo]):
#                     tree.insert(i)
#                 for child in tree.children:
#                     recorrerCadena(cadena[index+1:], child)
#                 return 0
                
#             else:
#                 return 0
        


# recorrerCadena(cadena, Mayortree)
# Mayortree.recorrer()
# print(Mayortree.rutas)
#print(tree)