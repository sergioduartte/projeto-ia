#coding: utf-8
import networkx as nx


def has_negative_weight(graph: nx.Graph) -> bool:
    for _, _, data in graph.edges(data=True):
        if data.get('weight', 1) < 0:
            return True
    return False


# Retorna o peso total do grafo
# Soma todos os pesos das arestas 
def graph_weight(graph: nx.Graph) -> float:
    return graph.size(weight="weight")

# Retorna um dicionario com as arestas e seus pesos
# No formato {(a, b): peso}
def all_edges_sizes(graph: nx.Graph):
    return nx.get_edge_attributes(graph, "weight")


def djikstra(graph: nx.Graph, node_start: nx.Node, node_end: nx.Node):
    
    # validações que depois serão feitas pelo validation.py
    if graph is None or node_start is None or node_end is None:
        raise AttributeError("Graph and nodes can't be None")
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph can't be empty")
    if not graph.has_node(node_start) or not graph.has_node(node_end):
        raise ValueError("Graph must contain the specified nodes")
    if has_negative_weight(graph):
        raise ValueError("Graph can't contain edges with negative weight")
    
    dist = {}
    pred = {}
    unvisited = set()

    for node in graph.nodes:
        dist[node] = float('inf')
        pred[node] = None
        unvisited.add(node)
    dist[node_start] = 0

    while unvisited:
        curr_node = # pegar vértice com menor distância dentro de dist
