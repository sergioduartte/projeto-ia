"""
Implementação do algoritmo de Dijkstra para encontrar o caminho mais curto em um grafo direcionado.
"""
#coding: utf-8
import heapq
import networkx as nx
from util import validator

def dijkstra(digraph: nx.DiGraph, start: str, end: str) -> tuple[float|None, list[str]]:
    """
    Encontra o caminho mais curto entre os nós start e end
    Retorna uma tupla com a distância total e a lista de nós no caminho.
    Se não houver caminho, retorna (float('inf'), None).
    """
    validator.validate_objects(digraph, start, end)
    if start == end:
        return 0, [start]

    pred = {start: None} # keep predecessors nodes
    dist = {start: 0} # keep distance of node to start
    unvisited = []
    heapq.heappush(unvisited, (0, start))

    while unvisited:
        curr_dist, curr_node = heapq.heappop(unvisited)

        if curr_dist > dist.get(curr_node, float('inf')):
            continue
        if curr_node == end:
            path = []
            node = end
            while node is not None:
                path.append(node)
                node = pred[node]
            path.reverse()
            return curr_dist, path

        for neighbor in digraph.neighbors(curr_node):
            edge = digraph.get_edge_data(curr_node, neighbor)
            edge_weight = edge.get("weight", 1)
            new_dist = curr_dist + edge_weight

            if new_dist < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_dist
                pred[neighbor] = curr_node
                heapq.heappush(unvisited, (new_dist, neighbor))
    return float('inf'), None # no path of start to end

graph = nx.DiGraph()
graph.add_edge("A", "B", weight=4)
graph.add_edge("A", "C", weight=2)
graph.add_edge("C", "B", weight=1)
graph.add_edge("B", "D", weight=5)

# start = end
dist, path = dijkstra(graph, "A", "A")
assert dist == 0
assert path == ["A"]

# A → C → B < A → B
dist, path = dijkstra(graph, "A", "B")
assert dist == 3
assert path == ["A", "C", "B"]

# no path of B to C
dist, path = dijkstra(graph, "B", "C")
assert dist == float("inf")
assert path is None
