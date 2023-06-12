import sys
from Alfabeto import Alfabeto
from AFD import AFD
from AFN import AFN
from AFN_e import AFN_Lambda
from ProcesamientoCadenaAFD import ProcesamientoCadenaAFD
from ProcesamientoCadenaAFN import ProcesamientoCadenaAFN
import tkinter as tk
from tkinter import ttk

class Interfaz:
    def __init__(self, prueba):
        self.ventana = tk.Tk()
        self.prueba = prueba
        self.frame = tk.Canvas(self.ventana,background='white')
        self.mainMenu()
    
    def crear_interfaz(self):
        self.width = 500
        self.height = 500
        self.ventana.title("AFD y AFN")
        self.ventana.geometry(str(self.width)+'x'+str(self.height))
        self.ventana.configure(background="white")
        self.frame.place(relx=0.5,rely=0.5,anchor='center')
        

    def mainMenu(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        tk.Label(self.frame, text="Seleccionar metodo").pack()
        tk.Button(self.frame, text="Construir automata" , command=self.construirAutomata).pack()
        tk.Button(self.frame, text="Importar desde archivo").pack()

    def construirAutomata(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        tk.Label(self.frame, text="Seleccione el tipo de automata").pack(pady=5)
        tk.Button(self.frame, text="AFD", command=self.crearAFD).pack(pady=5) 
        tk.Button(self.frame, text="AFN", command=None).pack(pady=5)
        tk.Button(self.frame, text="AFN Lambda", command=None).pack(pady=5)
        ttk.Separator(self.frame, orient='horizontal').pack(fill='both',expand=True, pady=5)
        tk.Button(self.frame, text="Volver", command=self.mainMenu).pack(side='left')
        tk.Button(self.frame, text="Salir", command=sys.exit).pack(side='right')

    def importarDesdeArchivo(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    
    def crearAFD(self):
        self.prueba.afd = AFD()
        for widgets in self.frame.winfo_children():
            widgets.destroy()

        
        tk.Label(self.frame, text='Ingrese el alfabeto del automata (ej: a-c, 0-9)').pack(pady=5)
        strAlfabeto = tk.StringVar()
        alfabeto = tk.Entry(self.frame, textvariable= strAlfabeto)
        alfabeto.pack(pady=5)
        alfabeto.bind('<Return>', lambda event, a = strAlfabeto:[self.crearNroEstados(event), self.prueba.getAlfabeto(a)])

    def crearNroEstados(self,event):
        tk.Label(self.frame, text='Ingrese el numero de estados del automata').pack(pady=5)
        nroEstados = tk.StringVar()
        nroEstadoslabel = tk.Entry(self.frame, textvariable= nroEstados)
        nroEstadoslabel.pack(pady=5)
        nroEstadoslabel.bind('<Return>', lambda event, a = nroEstados: [self.crearEstados(event), self.prueba.setNroEstados(nroEstados)])#lambda event, a = nroEstados.get():self.crearEstados(event, a))

    def crearEstados(self, event):
        tk.Label(self.frame, text='Ingrese el nombre de los estados').pack(pady=5)
        nombre = tk.StringVar()
        estadosNombre = tk.Entry(self.frame, textvariable= nombre) 
        estadosNombre.pack(pady=5)
        estadosNombre.bind('<Return>', lambda event, a = nombre:[ self.prueba.setEstados(nombre), self.elegirInicial(event)])
    
    def elegirInicial(self, event):
        tk.Label(self.frame, text = 'Seleccione el estado inicial').pack(pady=5)
        estadoInicial = ttk.Combobox(self.frame,values=self.prueba.afd.Q, width=10, state='readonly')
        estadoInicial.pack(pady=5)
        estadoInicial.bind('<Return>', lambda event, a = estadoInicial:[self.prueba.setInicial(a), self.crearAceptacion(event)])
    
    def crearAceptacion(self, event ,button=None, ok=None, label=True):
        if label == True:
            tk.Label(self.frame, text='Ingrese los estados de aceptacion').pack(pady = 5)
        if button is not None:
            button.destroy()
        if ok is not None:
            ok.destroy()
        aceptacion = ttk.Combobox(self.frame, values= self.prueba.afd.Q, state='readonly', width=10)
        aceptacion.pack(pady = 5)
        
        ok = tk.Button(self.frame, text='ok', command= lambda event = None, a = aceptacion:[self.prueba.getAceptacion(a), self.crearTransiciones(event)])
        ok.pack(side='right',pady=5)

        add = tk.Button(self.frame, text= '+')
        add.config(command = lambda event = None, a = add, b = ok, c = aceptacion:[self.crearAceptacion(event, a,b, False), self.prueba.getAceptacion(c)])
        add.pack(pady = 5, side='left')

    def crearTransiciones(self, event):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        
        boxes = []
        tk.Label(self.frame, text='Ingrese las transiciones del automata').pack(pady=5)
        for state in self.prueba.afd.Q:
            tk.Label(self.frame, text=state).pack(pady=3)
            for symbol in self.prueba.afd.Sigma.simbolos:
                canvas = tk.Canvas(self.frame)
                canvas.pack()
                tk.Label(canvas, text=f'    {symbol}').pack(pady=3, side='left')
                box = ttk.Combobox(canvas, values=self.prueba.afd.Q, width=10)
                box.pack(pady=3, side='right')
                boxes.append(box)
        tk.Button(self.frame, text='Ok',command=lambda event = None, a = boxes:[self.prueba.getTransiciones(a), self.AFDMenu(event)]).pack(pady=3)
    
    def AFDMenu(self, event):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

        tk.Label(self.frame, text='Seleccione el metodo de procesamiento').pack(pady=5)
        metodos = [('Procesar cadena', 'Procesar cadena con detalles'), ('Procesar lista de cadenas', 'Ver estados limbo'),
                    ('Ver estados inaccesibles', 'Imprimir automata'), ('Graficar automata',)]
        commands = [(self.menuProcesamiento)]

        for i in range(len(metodos)):
            canvas = tk.Canvas(self.frame)
            canvas.pack()
            tk.Button(canvas, text = metodos[i][0], command= commands[0]).pack(pady=5,side='left')
            tk.Button(canvas, text= metodos[i][1], command=None).pack(pady=5,side='right')
    
    def menuProcesamiento(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        tk.Button(self.frame, text='volver', command = lambda event = None:self.AFDMenu(event)).pack(pady=5,side='top')
        ttk.Separator(self.frame, orient='horizontal').pack(fill='both',expand=True, pady=5)

        tk.Label(self.frame, text='Ingrese una cadena').pack(pady=5)
        canvas = tk.Canvas(self.frame)
        cadena = tk.Entry(self.frame)
        cadena.pack(pady=5)
        cadena.bind('<Return>', lambda event, a = cadena, b = canvas :[self.prueba.procesarCadena(event, a), self.procesoMostrar(event, b)])
    
    def procesoMostrar(self, event, canvas):
        for widgets in canvas.winfo_children():
            widgets.destroy()
        canvas.pack()
        tk.Label(canvas, text=str(self.prueba.ProcesamientoAFD.esAceptada)).pack(pady=5)

        
class ClasePrueba:
    afn = None
    afd = None
    afn_lambda = None
    nroEstados = None
    ProcesamientoAFD = ProcesamientoCadenaAFD()

    def __init__(self, *args):
        #self.interfaz = args[0]
        pass

    def procesarCadena(self, event, cadena):
        self.ProcesamientoAFD.cadena = cadena.get()
        self.ProcesamientoAFD.esAceptada = self.afd.procesarCadena(self.ProcesamientoAFD.cadena)
        print(self.ProcesamientoAFD.esAceptada)

    def getAlfabeto(self, alfabeto):
        self.afd.Sigma = alfabeto.get().split(',')
        self.afd.Sigma = Alfabeto(self.afd.Sigma)
    
    def setNroEstados(self, nroEstados):
        self.nroEstados = nroEstados.get()
    
    def setEstados(self, nombre):
        nombre = nombre.get()
        self.estados = [nombre+str(i) for i in range(int(self.nroEstados))]
        self.afd.Q = self.estados

    def setInicial(self, inicial):
        self.afd.q0 = inicial.get()
    
    def getAceptacion(self, aceptacion):
        self.afd.F.add(aceptacion.get())

    def getTransiciones(self, boxes):
        self.transiciones = dict()
        a = 0
        for i in range(len(self.estados)):
            self.transiciones[self.estados[i]] = dict()
            for j in range(len(self.afd.Sigma.simbolos)):
                if boxes[j+a].get() == '':
                    next
                else:
                    self.transiciones[self.estados[i]][self.afd.Sigma.simbolos[j]] = set()
                    self.transiciones[self.estados[i]][self.afd.Sigma.simbolos[j]].add(boxes[j+a].get())
            a+=len(self.afd.Sigma.simbolos)
        self.afd.delta = self.transiciones
        self.afd.Q = set(self.afd.Q)
        self.afd.verificarCorregirCompletitudAFD()
        self.afd.hallarEstadosLimbo()
        print(self.transiciones)
        
start = ClasePrueba()
ui = Interfaz(start)
#Start = ClasePrueba()
#Start.main()
ui.crear_interfaz()
ui.ventana.mainloop()