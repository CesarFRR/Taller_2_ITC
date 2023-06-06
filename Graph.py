import random
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from AFD import AFD
from AFN import AFN
from AFN_e import AFN_Lambda
class graficarAutomata:
    rad = .1
    automata =None
    # def __init__(self, *args):
    #     archivo1='impares' # AFD--> L: |w| impar
    #     afd1= AFD(archivo1+'.dfa') 
    #     #Crear un dataframe vacío
    #     nfa1= AFN("ej1.nfa")
    #     data = pd.DataFrame(columns=['source', 'to', 'label'])

    #     delta2 = {}
    #     for estado, transiciones in nfa1.delta.items():
    #         delta2[estado] = {}
    #         for simbolo, destinos in transiciones.items():
    #             for destino in destinos:
    #                 if destino in delta2[estado]:
    #                     delta2[estado][destino].add(simbolo)
    #                 else:
    #                     delta2[estado][destino] = {simbolo}

    #     for estado, transiciones in delta2.items():
    #         for destino, simbolos in transiciones.items():
    #             data = data.append({'source': estado, 'to': destino, 'label': ', '.join(simbolos)}, ignore_index=True)
    #     print(data)

        
    #     conn_style = f'arc3,rad={self.rad}'
    #     G = nx.from_pandas_edgelist(data, source='source', target='to', edge_attr='label', create_using=nx.DiGraph())
    #     node_fill_colors = ["lightgrey" if n == 'q0' else "white" for n in G.nodes()]
    #     node_border_colors = ['black'] * len(G.nodes())
    #     node_border_widths = [3 if node == "q3" else 1 for node in G.nodes()]
    #     node_sizes = [len(str(n))*300 for n in G.nodes()]
    #     weight = nx.get_edge_attributes(G, 'label')
    #     pos = nx.shell_layout(G, scale=1)

    #     nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_fill_colors, linewidths=node_border_widths, edgecolors=node_border_colors)
    #     nx.draw_networkx_labels(G, pos=pos, font_color='black', font_family='Times New Roman', font_size=10)
    #     edges=nx.draw_networkx_edges(G, pos=pos, edgelist=G.edges(), edge_color=self.random_edges_colors(G),
    #                         connectionstyle=conn_style)
    #     d = nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=weight, font_family='Times New Roman')
    #     self.edge_calibration(d, pos, asp = self.get_aspect(plt.gca()))
    #     plt.tight_layout()
    #     print('d: ',type(d),'edges: ', type(edges))
    #     plt.setp(edges, zorder=2)
    #     plt.setp(d.values(), zorder=3)
    #     plt.show()
    def graficar(self, automata):
        self.automata=automata
        #Crear un dataframe vacío
        data = pd.DataFrame(columns=['source', 'to', 'label'])
        delta2 = {}
        for estado, transiciones in self.automata.delta.items():

            delta2[estado] = {}
            for simbolo, destinos in transiciones.items():
                for destino in destinos:
                    if destino in delta2[estado]:
                        delta2[estado][destino].add(simbolo)
                    else:
                        delta2[estado][destino] = {simbolo}

        for estado, transiciones in delta2.items():
            for destino, simbolos in transiciones.items():
                data = data.append({'source': estado, 'to': destino, 'label': ', '.join(simbolos)}, ignore_index=True)
        print(data)

        
        conn_style = f'arc3,rad={self.rad}'
        G = nx.from_pandas_edgelist(data, source='source', target='to', edge_attr='label', create_using=nx.DiGraph())
        node_fill_colors = ["lightgrey" if n in self.automata.q0 else "white" for n in G.nodes()]
        node_border_colors = ['black'] * len(G.nodes())
        node_border_widths = [3 if node in self.automata.F else 1 for node in G.nodes()]
        node_sizes = [len(str(n))*300 for n in G.nodes()]
        weight = nx.get_edge_attributes(G, 'label')
        pos = nx.shell_layout(G, scale=1)

        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_fill_colors, linewidths=node_border_widths, edgecolors=node_border_colors)
        nx.draw_networkx_labels(G, pos=pos, font_color='black', font_family='Times New Roman', font_size=10)
        edges=nx.draw_networkx_edges(G, pos=pos, edgelist=G.edges(), edge_color=self.random_edges_colors(G),
                            connectionstyle=conn_style)
        d = nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=weight, font_family='Times New Roman')
        self.edge_calibration(d, pos, asp = self.get_aspect(plt.gca()))
        plt.tight_layout()
        plt.setp(edges, zorder=2)
        plt.setp(d.values(), zorder=3)
        tituloVentana=f"Gráfo del autómata: {self.automata.nombreArchivo}.{self.automata.extension}"
        print(tituloVentana)
        print(automata.Sigma.simbolos)
        plt.gcf().canvas.manager.set_window_title(tituloVentana)

        plt.show()


    def random_edges_colors(self, G):
        colors = [] # Aristas de diferentes colores ayuda a diferenciarlas mejor en el grafo
        for _ in G.edges():
            # Genera componentes RGB aleatorias
            r, g, b = random.random(), random.random(), random.random()

            # Ajusta el brillo para evitar colores demasiado claros
            while r + g + b > 2.5:
                r, g, b = random.random(), random.random(), random.random()

            # Agrega el color a la lista
            colors.append((r, g, b))
        return colors



    def edge_calibration(self, d, pos,dist=rad/2, loop_shift=0.2, asp=1):
        for (source, dest), obj in d.items():
            if source != dest:
                par = dist * (pos[dest] - pos[source])
                dx, dy = par[1] * asp, -par[0] / asp
                x, y = obj.get_position()
                obj.set_position((x + dx, y + dy))
                obj.set_rotation(0)
            else:
                x, y = obj.get_position()
                obj.set_position((x, y + loop_shift))
    def sub(self, a,b):
        return a-b

    def get_aspect(self, ax):
        # Total figure size
        figW, figH = ax.get_figure().get_size_inches()
        # Axis size on figure
        _, _, w, h = ax.get_position().bounds
        # Ratio of display units
        disp_ratio = (figH * h) / (figW * w)
        # Ratio of data units
        # Negative over negative because of the order of subtraction
        data_ratio = self.sub(*ax.get_ylim()) / self.sub(*ax.get_xlim())

        return disp_ratio / data_ratio

nfa1= AFN("ej1.nfa")
dfa1 =AFD("ej0.dfa")
nfe1= AFN_Lambda('ej1.nfe')
graficar = graficarAutomata()
graficar.graficar(dfa1)
graficar.graficar(nfa1)
graficar.graficar(nfe1)
print(dfa1.delta,'\n\n')
print(dfa1.Sigma.simbolos,'\n\n')

#plt.figure(figsize = (10,10))
