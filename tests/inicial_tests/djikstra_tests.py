import pytest 
import networkx as nx

from core.djikstra import djikstra

def test_djikstra_with_graphNone():
    """
    GIVEN nenhum grafo passado para a função djikstra
    WHEN djikstra for chamado
    THEN deve lançar uma exceção AttributeError
    """

    with pytest.raises(AttributeError):
        djikstra(None, "A", "B")

def test_djikstra_with_nodes_none():
    """
    GIVEN nenhum nó ou apenas um dos nós é passado para a função djikstra
    WHEN djikstra for chamado
    THEN deve lançar uma exceção AttributeError
    """

    with pytest.raises(AttributeError):
        djikstra(nx.Graph(), None, "B")

    with pytest.raises(AttributeError):
        djikstra(nx.Graph(), "A", None)
    
    with pytest.raises(AttributeError):
        djikstra(nx.Graph(), None, None)

def test_djikstra_with_nonexistent_nodes():
    """
    GIVEN um grafo sem nós, vazio
    WHEN djikstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    G = nx.DiGraph()

    with pytest.raises(ValueError):
        djikstra(G, "A", "B")

def test_djikstra_with_nonexistent_start_node():
    """
    GIVEN um grafo com alguns nós, mas o nó inicial não existe
    WHEN djikstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    G = nx.DiGraph()
    G.add_nodes_from(["B", "C", "D"])

    with pytest.raises(ValueError):
        djikstra(G, "A", "B")

def test_djikstra_with_nonexistent_end_node():
    """
    GIVEN um grafo com alguns nós, mas o nó de destino não existe
    WHEN djikstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    G = nx.DiGraph()
    G.add_nodes_from(["A", "B", "C"])

    with pytest.raises(ValueError):
        djikstra(G, "A", "D")

def test_djikstra_with_nonexistent_start_and_end_nodes():
    """
    GIVEN um grafo com alguns nós, mas o nó de destino não existe
    WHEN djikstra for chamado
    THEN deve lançar uma exceção ValueError
    """ 
    G = nx.DiGraph()
    G.add_nodes_from(["B", "C", "D"])

    with pytest.raises(ValueError):
        djikstra(G, "A", "E")
    
def test_djikstra_with__negative_weights():
    """
    GIVEN um grafo com pesos negativos nas arestas
    WHEN djikstra for chamado
    THEN deve lançar uma exceção ValueError
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=-1)
    G.add_edge("B", "C", weight=2)

    with pytest.raises(ValueError):
        djikstra(G, "A", "C")

def test_djikstra_with_inexistent_path():
    """
    GIVEN um grafo onde não existe um caminho entre o nó inicial e o nó de destino
    WHEN djikstra for chamado
    THEN deve retornar a tupla (float('inf'), None)
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=1)
    G.add_edge("C", "D", weight=2)

    result = djikstra(G, "A", "D")
    assert result == (float('inf'), None)

def test_djikstra_with_same_start_and_end_node():
    """
    GIVEN um grafo onde o nó inicial e o nó de destino são o mesmo
    WHEN djikstra for chamado
    THEN deve retornar a tupla (0, [nó_inicial]), indicando que o custo é zero e o caminho é apenas o nó inicial
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=1)
    G.add_edge("B", "C", weight=2)

    result = djikstra(G, "A", "A")
    assert result == (0, ["A"])

def test_djikstra_with_only_one_valid_path():
    """
    GIVEN um grafo onde existe apenas um caminho válido entre o nó inicial e o nó de destino
    WHEN djikstra for chamado
    THEN deve retornar o custo e o caminho correto
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=1)
    G.add_edge("B", "C", weight=2)
    G.add_edge("A", "C", weight=5)

    result = djikstra(G, "A", "C")
    assert result == (3, ["A", "B", "C"])

def test_djikstra_with_two_paths_equivalent_in_cost():
    """
    GIVEN um grafo onde existem dois caminhos com o mesmo custo entre o nó inicial e o nó de destino
    WHEN djikstra for chamado
    THEN deve retornar o custo correto e o primeiro caminho encontrado
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=2)
    G.add_edge("B", "C", weight=2)
    G.add_edge("A", "D", weight=1)
    G.add_edge("D", "C", weight=3)

    result = djikstra(G, "A", "C")
    assert result == (4, ["A", "B", "C"])