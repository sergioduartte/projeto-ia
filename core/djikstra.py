#coding: utf-8
import heapq
import networkx as nx


def has_negative_weight(graph: nx.DiGraph) -> bool:
    for _, _, data in graph.edges(data=True):
        if data.get('weight', 1) < 0:
            return True
    return False


def djikstra(graph: nx.DiGraph, start: str, end: str) -> tuple[float|None, list[str]]:

    # validator.validate_objects(graph, start, end)

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
        
        for neighbor in graph.neighbors(curr_node):
            edge = graph.get_edge_data(curr_node, neighbor)
            edge_weight = edge.get("weight", 1)
            new_dist = curr_dist + edge_weight

            if new_dist < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_dist
                pred[neighbor] = curr_node
                heapq.heappush(unvisited, (new_dist, neighbor))
    
    return float('inf'), None


G = nx.DiGraph()
G.add_edge("A", "B", weight=4)
G.add_edge("A", "C", weight=2)
G.add_edge("C", "B", weight=1)
G.add_edge("B", "D", weight=5)

# start = end
dist, path = djikstra(G, "A", "A")
assert dist == 0
assert path == ["A"]

# A → C → B < A → B
dist, path = djikstra(G, "A", "B")
assert dist == 3
assert path == ["A", "C", "B"]

# no path of B to C
dist, path = djikstra(G, "B", "C")
assert dist == float("inf")
assert path == None
