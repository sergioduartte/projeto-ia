#coding: utf-8

'''
Build a graph from a json
'''

import networkx as nx
import json

# Abre o arquivo 'graph.json' (caminho do arquvio), transforma o conteudo json em variaveis 
# Tudo vira um dicionario
with open("graph.json") as graph:
    data = json.load(f)


