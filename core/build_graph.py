#coding: utf-8

'''
Build a graph from a json
'''

import networkx as nx
import json


def build_graph(path):

    # Abre o arquivo 'graph.json' (caminho do arquvio), transforma o conteudo json em variaveis 
    # Tudo vira um dicionario no formato -> 'edges': [['A', 'B', 5], ['B', 'C', 7]]
    # O valor da chave é uma lista de tuplas com 2 nós terminais e o peso da aresta que os conectam
    with open(path) as graph:
        data = json.load(graph)

    # Inicia e constrói o grafo
    G = nx.Graph()
    for node, terminal, w in data["edges"]:
        G.add_edge(node, terminal, weight=w)
    
    return G

# testing

G = build_graph("data/testing_building.json")

print("Nodes: ", G.nodes())
print("Edges: ", G.edges(data=True))

assert G.nodes() == {['A', 'B', 'C', 'D', 'E', 'F']} 
assert G.edges(data=True) == "[('A', 'B', 5), ('A', 'C', 3), ('B', 'C', 10), ('C', 'D', 1), ('E', 'F', 5)]"


