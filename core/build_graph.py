#coding: utf-8

'''
Build a graph from a json
'''

import sys
import os
import networkx as nx
import json

# Encontra o diretório pai da pasta 'core' (que é a raiz do projeto)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util import validator


'''
Abre o arquivo através do seu caminho e transforma o conteudo json em variaveis 
Tudo vira um dicionario no formato -> 'edges': [['A', 'B', 5], ['B', 'C', 7]]
O valor da chave é uma lista de listas de tamanho 3 sendo [node, terminal, weight]
'''
def build_graph(path):
    validator.validate_path(path)
    validator.validate_graph_entry(path)
    with open(path) as file:
        data = json.load(file)

    # Inicia e constrói o grafo
    G = nx.DiGraph()
    for node, terminal, w in data["edges"]:
        G.add_edge(node, terminal, weight=w)
    
    return G


# testing 

'''
This is how the json looks like:
{
    "edges" : [
            ["A", "B", 5],
            ["A", "C", 3],
            ["B", "C", 10],
            ["C", "D", 1],
            ["E", "F", 5]
    ]
}
'''
archive_path = os.path.abspath("data/dataset.json")
G = build_graph(archive_path)

# print("Nodes: ", G.nodes())
# print("Edges: ", G.edges(data=True))

assert set(G.nodes()) == {'A', 'B', 'C', 'D', 'E', 'F'}

assert G.number_of_nodes() == 6
assert G.number_of_edges() == 5

assert G['A']['B']['weight'] == 5.0
assert G['A']['C']['weight'] == 3.0
assert G['B']['C']['weight'] == 10.0
assert G['C']['D']['weight'] == 1.0
assert G['E']['F']['weight'] == 5.0



