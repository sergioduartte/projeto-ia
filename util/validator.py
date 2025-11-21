"""That file has functions that perform validations overall the code
"""

import json
import os


def validate_entries(path: str, vA: str, vB: str):
    """
    Validates the entry of user.

    Parameters:
    path (str): json's path with edges infos
    vA (str): vertexA.
    vB (str): vertexB.

    Raises:
    Exceptions if the graph and the vertices are not valid. 
    """
    
    excs = []
    
    try:
        # valida o caminho se existe, se o arquivo é .json
        validate_path(path)
    
        # valida se é possível gerar um grafo com o path, se o grafo é nulo e
        # checa se as arestas contém peso negativo
        validate_graph_entry(path)
    
        # valida se os vertices passados estao no grafo 
        validate_vertices_entry(path, vA, vB)
    
    except Exception as e:
        raise e


def validate_path(path: str):
    # testar schema posteriormente
    try:
        with open(path, 'r', encoding='utf-8') as jsonpath:
            data = json.load(jsonpath)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError('Please check the path and try again')
    except json.JSONDecodeError as j:
        raise json.JSONDecodeError(msg='Please check the path and try again',
                                   doc= path,
                                   pos= j.pos)


def validate_graph_entry(path: str):
    data = validate_path(path)
    if data != None:
        edges = []
        for vA, vB, w in data["edges"]:
            if vA == "" or vA == None:
                raise ValueError(f"The value of vertixA is empty")
            if vB == "" or vB == None:
                raise ValueError(f"The value of vertixB is empty")
            if type(w) != float and type(w) != int:
                raise ValueError(f"The value of Weight between {vA} " + 
                                 f"and {vB} needs to be a number")
            if w < 0:
                raise ValueError(f"The value of Weight between {vA} " + 
                                 f"and {vB} needs to be positive")
            if w > 0 and vA == vB:
                raise ValueError(f"The value of Weight between {vA} " + 
                                 f"and {vB} needs to be zero!(loop)")
            edges.append([vA, vB])

        if len(edges) == 0: 
            raise ValueError("Graph can't be empty")
        
        return edges


def validate_vertices_entry(path: str, vA: str, vB: str):
    edges = validate_graph_entry(path)
        
    if edges != None:
        not_foundA = True
        not_foundB = True
        for edge in edges:
            if vA in edge:
                foundA = False
            if vB in edge:
                foundB = False
            if vA and vB:
                break
        if not_foundA:
            raise ValueError(f"Node {vA} not found!")
        if not_foundB:
            raise ValueError(f"Node {vB} not found!")


def has_negative_weight(graph) -> bool:
    for _, _, data in graph.edges(data=True):
        if data.get('weight', 1) < 0:
            return True
    return False


def validate_objects(graph, start: str, end: str):
    if graph is None or start is None or end is None:
        raise AttributeError("Graph and nodes can't be None")
    if graph.number_of_edges() == 0:
        raise ValueError("Graph can't be empty")
    if not graph.has_node(start) or not graph.has_node(end):
        raise ValueError("Graph must contain the specified nodes")
    if has_negative_weight(graph):
        raise ValueError("Graph can't contain edges with negative weight")
