#coding: utf-8
import heapq
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


def djikstra(graph: nx.Graph, start: nx.Node, end: nx.Node):
    
    # validations that will be performed by validation.py
    if graph is None or start is None or end is None:
        raise AttributeError("Graph and nodes can't be None")
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph can't be empty")
    if not graph.has_node(start) or not graph.has_node(end):
        raise ValueError("Graph must contain the specified nodes")
    if has_negative_weight(graph):
        raise ValueError("Graph can't contain edges with negative weight")
    
    pred = {start: None} # keep predecessors nodes
    dist = {start: 0} # keep distance of node to start

    unvisited = []
    heapq.heappush(unvisited, (0, start))

    while unvisited:
        curr_dist, curr_node = 
