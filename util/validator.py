"""
That file has functions that perform validations overall the code
"""
import json

def validate_entries(path: str, v_a: str, v_b: str):
    """
    Validates the entry of user.

    Parameters:
    path (str): json's path with edges infos
    vA (str): vertexA.
    vB (str): vertexB.

    Raises:
    Exceptions if the graph and the vertices are not valid.
    """

    try:
        # valida o caminho se existe, se o arquivo é .json
        validate_path(path)

        # valida se é possível gerar um grafo com o path, se o grafo é nulo e
        # checa se as arestas contém peso negativo
        validate_graph_entry(path)

        # valida se os vertices passados estao no grafo
        validate_vertices_entry(path, v_a, v_b)

    except Exception as e:
        raise e


def validate_path(path: str):
    """
    Validate if a JSON file exists and can be loaded.

    Parameters
    ----------
    path : str
        Path to the JSON file.

    Returns
    -------
    dict
        Parsed JSON content.

    Raises
    ------
    FileNotFoundError
        If the file cannot be found.
    JSONDecodeError
        If the file is not valid JSON.
    """
    try:
        with open(path, 'r', encoding='utf-8') as jsonpath:
            data = json.load(jsonpath)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError('Please check the path and try again') from e
    except json.JSONDecodeError as j:
        raise json.JSONDecodeError(msg='Please check the path and try again',
                                   doc= path,
                                   pos= j.pos)


def validate_graph_entry(path: str):
    """
    Validates graph structure:
    - No empty graph
    - No empty vertices
    - No non-numeric weights
    - No negative weights
    - No loops with non-zero weights

    Parameters
    ----------
    path : str
        Path to the JSON file.

    Returns
    -------
    list[list]
        List of edges (without weights).

    Raises
    ------
    ValueError
        If the graph is invalid.
    """
    data = validate_path(path)
    edges = []

    if data is not None:
        for v_a, v_b, w in data["edges"]:
            if not v_a:
                raise ValueError("The value of vertixA is empty")
            if not v_b:
                raise ValueError("The value of vertixB is empty")
            if not isinstance(w, (int, float)):
                raise ValueError(
                    f"The value of Weight between {v_a} and {v_b} needs to be a number"
                )
            if w < 0:
                raise ValueError(
                    f"The value of Weight between {v_a} and {v_b} needs to be positive"
                )
            if w > 0 and v_a == v_b:
                raise ValueError(
                    f"The value of Weight between {v_a} and {v_b} needs to be zero!(loop)"
                )

            edges.append([v_a, v_b])

    if len(edges) == 0:
        raise ValueError("Graph can't be empty")

    return edges



def validate_vertices_entry(path: str, v_a: str, v_b: str):
    """
    Validate whether the given vertices exist in the graph.

    Parameters
    ----------
    path : str
        JSON file path.
    v_a : str
        Vertex A.
    v_b : str
        Vertex B.

    Raises
    ------
    ValueError
        If one or both vertices are not found.
    """
    edges = validate_graph_entry(path)

    if edges is not None:
        found_a = False
        found_b = False
        for edge in edges:
            if v_a in edge:
                found_a = True
            if v_b in edge:
                found_b = True
            if found_a and found_b:
                break
        if not found_a:
            raise ValueError(f"Node {v_a} not found!")
        if not found_b:
            raise ValueError(f"Node {v_b} not found!")

def has_negative_weight(graph) -> bool:
    """
    Check if any edge in the graph has negative weight.

    Parameters
    ----------
    graph : networkx.Graph
        Graph to be checked.

    Returns
    -------
    bool
        True if a negative weight exists, else False.
    """
    for _, _, data in graph.edges(data=True):
        if data.get('weight', 1) < 0:
            return True
    return False


def validate_objects(graph, start: str, end: str):
    """
    Validate graph object and nodes used for pathfinding.

    Parameters
    ----------
    graph : networkx.Graph
        Graph to validate.
    start : str
        Source node.
    end : str
        Target node.

    Raises
    ------
    AttributeError
        If graph or nodes are None.
    ValueError
        If graph is empty or has invalid nodes/weights.
    """
    if graph is None or start is None or end is None:
        raise AttributeError("Graph and nodes can't be None")
    if graph.number_of_edges() == 0:
        raise ValueError("Graph can't be empty")
    if not graph.has_node(start) or not graph.has_node(end):
        raise ValueError("Graph must contain the specified nodes")
    if has_negative_weight(graph):
        raise ValueError("Graph can't contain edges with negative weight")
