#coding: utf-8

'''
Build a graph from a json
'''

import json
import sys
import os
import networkx as nx
from util import validator

# Encontra o diretório pai da pasta 'core' (que é a raiz do projeto)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def build_graph(path):
    '''
    Abre o arquivo através do seu caminho e transforma o conteudo json em variaveis
    Tudo vira um dicionario no formato -> 'edges': [['A', 'B', 5], ['B', 'C', 7]]
    O valor da chave é uma lista de listas de tamanho 3 sendo [node, terminal, weight]
    '''
    validator.validate_path(path)
    validator.validate_graph_entry(path)
    with open(path, encoding='utf-8') as file:
        data = json.load(file)

    # Inicia e constrói o grafo
    digraph = nx.DiGraph()
    for node, terminal, w in data["edges"]:
        digraph.add_edge(node, terminal, weight=w)

    return digraph
# testing
archive_path = os.path.abspath("data/dataset.json")
graph = build_graph(archive_path)

# print("Nodes: ", graph.nodes())
# print("Edges: ", graph.edges(data=True))

assert set(graph.nodes()) == {'A', 'B', 'C', 'D', 'E', 'F'}

assert graph.number_of_nodes() == 6
assert graph.number_of_edges() == 5

assert graph['A']['B']['weight'] == 5.0
assert graph['A']['C']['weight'] == 3.0
assert graph['B']['C']['weight'] == 10.0
assert graph['C']['D']['weight'] == 1.0
assert graph['E']['F']['weight'] == 5.0
