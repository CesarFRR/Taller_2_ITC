import tkinter as tk
from ClasePrueba import ClasePrueba
from Alfabeto import Alfabeto

class AutomataInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz de Autómata Finito")
        
        self.prueba = ClasePrueba()
        # Variables para almacenar los valores ingresados por el usuario
        self.estados = tk.StringVar()
        self.simbolos = tk.StringVar()
        self.estado_inicial = tk.StringVar()
        self.estados_aceptacion = tk.StringVar()
        self.transiciones_start = tk.StringVar()
        self.transiciones_symbol = tk.StringVar()
        self.transiciones_end = tk.StringVar()
        self.cadena_entrada = tk.StringVar()
        self.tipo_automata = tk.StringVar(value="AFD")
        self.lista_cadenas = tk.StringVar()
        self.delta = dict()
        self.archivo_lista = tk.StringVar()
        self.archivo_exportar = tk.StringVar()
        self.archivo_importar = tk.StringVar()
        self.st = tk.Entry(self, textvariable=self.transiciones_start, width=10)
        self.sy= tk.Entry(self, textvariable=self.transiciones_symbol, width=10)
        self.en = tk.Entry(self, textvariable=self.transiciones_end, width=10)
        self.main_menu()

    def main_menu(self):

        self.create_labels()
        self.create_entries()
        self.create_selector()
        self.create_button()
        
        # Crear los elementos de la interfaz
    
    def create_labels(self):
        '''Crear etiquetas del menu principal'''
        tk.Label(self, text="Estados (separados por comas):").grid(row=1, column=0, sticky="w")
        tk.Label(self, text="Alfabeto (ej: a-c):").grid(row=2, column=0, sticky="w")
        tk.Label(self, text="Estado Inicial:").grid(row=3, column=0, sticky="w")
        tk.Label(self, text="Estados de Aceptación (separados por comas):").grid(row=4, column=0, sticky="w")
        tk.Label(self, text="Transiciones (estado,símbolo,estado):").grid(row=5, column=0, sticky="w")
        tk.Label(self, text="Importar desde archivo:").grid(row=7, column=0, columnspan=3)
        tk.Label(self, text="Tipo de Autómata:").grid(row=6, column=0, sticky="w")
        
    def create_entries(self):
        '''Crear campos de texto del menu principal'''
        tk.Entry(self, textvariable=self.estados).grid(row=1, column=1, columnspan= 3)
        tk.Entry(self, textvariable=self.simbolos).grid(row=2, column=1, columnspan= 3)
        tk.Entry(self, textvariable=self.estado_inicial).grid(row=3, column=1, columnspan= 3)
        tk.Entry(self, textvariable=self.estados_aceptacion).grid(row=4, column=1, columnspan= 3)
        tk.Entry(self, textvariable=self.archivo_importar).grid(row=8, column=0, columnspan= 2)
        self.st.grid(row=5, column=1, columnspan= 1)
        self.sy.grid(row=5, column=2, columnspan= 1)
        self.en.grid(row=5, column=3, columnspan= 1)
        
    def create_selector(self):
        '''Crear selector para el tipo de automata a crear'''
        options = ["AFD", "AFN", "AFNLambda", 'AFPD', 'AFPN', 'AF2P', 'MT']
        tk.OptionMenu(self, self.tipo_automata, *options).grid(row=6, column=1, columnspan= 3, sticky="w")
        
    def create_button(self):
        '''Crear botones del menu principal'''
        tk.Button(self, text= '+', command=self.add_transition).grid(row=5, column=4, columnspan=1)
        tk.Button(self, text= 'Importar', command=self.importar).grid(row=8, column=3, columnspan=2)
        tk.Button(self, text="Continuar", command=self.pressed_button).grid(row=11, column=0, columnspan=2)
        tk.Button(self, text="Salir", command=self.close).grid(row=11, column=1, columnspan=2)
    
    def importar(self):
        '''Crear automata desde archivo'''
        archivo = self.archivo_importar.get().strip(' ')
        tipo_automata = self.tipo_automata.get()
        self.prueba.main([tipo_automata, None], [archivo])
        self.mostrar_ventana_metodo(tipo_automata)


    def add_transition(self):
        '''Boton '+' presionado, añade una transicion'''
        start = self.transiciones_start.get()
        symbol = self.transiciones_symbol.get()
        end = self.transiciones_end.get()
        if self.delta.get(start) is None:
            self.delta[start] = {symbol: {end}}
        elif self.delta[start].get(symbol) is None:
            self.delta[start][symbol]={end}
        else:
            self.delta[start][symbol].add(end)

        self.st.delete(0, tk.END)
        self.sy.delete(0,tk.END)
        self.en.delete(0,tk.END)
        
    def pressed_button(self):
        '''Boton 'Continuar' presionado, crear automata usando los elementos ingresados en los campos de texto'''
        # Obtener los valores ingresados por el usuario
        estados = self.estados.get().split(",")
        simbolos = self.simbolos.get().split(",")
        estado_inicial = self.estado_inicial.get()
        estados_aceptacion = self.estados_aceptacion.get().split(",")
        print(self.delta)
        tipo_automata = self.tipo_automata.get()
        elementos = [Alfabeto(simbolos), set(estados), estado_inicial, set(estados_aceptacion), self.delta]
        self.prueba.main([tipo_automata, None], elementos)
        
        self.mostrar_ventana_metodo(tipo_automata)
    
    def mostrar_ventana_metodo(self, tipoAutomata):
        '''Ventana donde se selecciona el metodo para procesar cadena o se imprime/exporta el automata'''
        # Ocultar la ventana actual
        self.withdraw()
        
        # Crear una nueva ventana para elegir el método de procesamiento
        ventana_metodo = tk.Toplevel(self)
        ventana_metodo.title("Elegir Método de Procesamiento")
        
        tk.Label(ventana_metodo, text="Ingresar cadena:").grid(row=0, column=0, columnspan=2)
        tk.Entry(ventana_metodo, textvariable=self.cadena_entrada).grid(row=1,column=0, columnspan=2)
        tk.Button(ventana_metodo, text="Procesar Cadena", command= lambda:self.prueba.main([tipoAutomata, 'Procesar cadena'],self.cadena_entrada.get())).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(ventana_metodo, text="Procesar con Detalles", command=lambda:self.prueba.main([tipoAutomata, 'Procesar cadena con detalles'], self.cadena_entrada.get())).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(ventana_metodo, text = 'Ingresar lista de cadenas(separadas por coma)').grid(row=3, column=0)
        tk.Label(ventana_metodo, text = 'Nombre archivo').grid(row=3, column=1)
        tk.Entry(ventana_metodo, textvariable=self.lista_cadenas).grid(row=4,column=0)
        tk.Entry(ventana_metodo, textvariable=self.archivo_lista).grid(row=4,column=1)
        tk.Button(ventana_metodo, text="Procesar Lista de Cadenas", command=lambda:self.prueba.main([tipoAutomata, 'Procesar lista de cadenas'],[self.lista_cadenas.get().split(','),self.archivo_lista.get()])).grid(row=5, column=0, padx=10, pady=5, columnspan=2)
        
        tk.Label(ventana_metodo, text = 'Nombre archivo para exportar AFD').grid(row=6, column=0)
        tk.Entry(ventana_metodo, textvariable=self.archivo_exportar).grid(row=7,column=0,columnspan=2)
        tk.Button(ventana_metodo, text="Exportar Autómata", command=lambda:self.prueba.main([tipoAutomata, 'Exportar'],self.archivo_exportar.get())).grid(row=8, column=0, padx=10, pady=5, columnspan=2)
        tk.Button(ventana_metodo, text="Imprimir automata", command=lambda:self.prueba.main([tipoAutomata, 'Imprimir'])).grid(row=9, column=0)
        tk.Button(ventana_metodo, text="Mostrar grafo", command=lambda:self.prueba.main([tipoAutomata, 'Graficar'])).grid(row=9, column=1)
        
        if tipoAutomata == 'AFD':
            tk.Button(ventana_metodo, text = 'Producto cartesiano', command= lambda:[self.volver_ventana_principal(ventana_metodo)]).grid(row=10, column=0)
            tk.Button(ventana_metodo, text = 'Simplificar', command= self.prueba.probarSimplificacion).grid(row=10, column=1)
            tk.Button(ventana_metodo, text = 'Hallar complemento', command= self.prueba.probarComplemento).grid(row=11, column=0, columnspan= 2)
        
        elif tipoAutomata == 'AFN':
            tk.Entry(ventana_metodo, textvariable=self.cadena_entrada).grid(row=10,column=0)
            tk.Button(ventana_metodo, text = 'AFN a AFD', command=lambda:self.prueba.main([tipoAutomata, 'AFNtoAFD'], self.cadena_entrada.get())).grid(row=10,column=1)
        
        elif tipoAutomata == 'AFNLambda':
            tk.Entry(ventana_metodo, textvariable=self.cadena_entrada).grid(row=10,column=0)
            tk.Button(ventana_metodo, text = 'AFNLambda a AFD', command=lambda:self.prueba.main([tipoAutomata, 'AFNLambdaToAFD'], self.cadena_entrada.get())).grid(row=10,column=0, columnspan=2)

        tk.Button(ventana_metodo, text="Salir", command=self.close).grid(row=0, column=1, columnspan=2)
        
    def volver_ventana_principal(self, ventana):
        # Cerrar la ventana actual
        ventana.destroy()
        
        # Mostrar nuevamente la ventana principal
        self.deiconify()

    def close(self):
        '''Cerrar ventana y finalizar programa'''
        self.destroy()
        self.quit()

interfaz = AutomataInterface()
interfaz.mainloop()