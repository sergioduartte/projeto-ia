import pytest 
import networkx as nx

from core.dijkstra import dijkstra

def test_dijkstra_with_graphNone():
    """
    GIVEN nenhum grafo passado para a função dijkstra
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção AttributeError
    """

    with pytest.raises(AttributeError):
        dijkstra(None, "A", "B")

def test_dijkstra_with_nodes_none():
    """
    GIVEN nenhum nó ou apenas um dos nós é passado para a função dijkstra
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção AttributeError
    """

    with pytest.raises(AttributeError):
     dijkstra(nx.Graph(), None, "B")

    with pytest.raises(AttributeError):
     dijkstra(nx.Graph(), "A", None)
    
    with pytest.raises(AttributeError):
     dijkstra(nx.Graph(), None, None)

def test_djikstra_with_nonexistent_nodes():
    """
    GIVEN um grafo sem nós, vazio
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    G = nx.DiGraph()

    with pytest.raises(ValueError):
     dijkstra(G, "A", "B")

def test_djikstra_with_nonexistent_start_node():
    """
    GIVEN um grafo com alguns nós, mas o nó inicial não existe
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    G = nx.DiGraph()
    G.add_nodes_from(["B", "C", "D"])

    with pytest.raises(ValueError):
     dijkstra(G, "A", "B")

def test_djikstra_with_nonexistent_end_node():
    """
    GIVEN um grafo com alguns nós, mas o nó de destino não existe
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    G = nx.DiGraph()
    G.add_nodes_from(["A", "B", "C"])

    with pytest.raises(ValueError):
     dijkstra(G, "A", "D")

def test_djikstra_with_nonexistent_start_and_end_nodes():
    """
    GIVEN um grafo com alguns nós, mas o nó de destino não existe
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """ 
    G = nx.DiGraph()
    G.add_nodes_from(["B", "C", "D"])

    with pytest.raises(ValueError):
     dijkstra(G, "A", "E")
    
def test_djikstra_with__negative_weights():
    """
    GIVEN um grafo com pesos negativos nas arestas
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=10)
    G.add_edge("A", "C", weight=17)
    G.add_edge("A", "D", weight=10)
    G.add_edge("B", "C", weight=-5)
    G.add_edge("B", "E", weight=7)
    G.add_edge("C", "F", weight=3)
    G.add_edge("C", "H", weight=4)
    G.add_edge("D", "F", weight=10)
    G.add_edge("E", "G", weight=12)
    G.add_edge("E", "H", weight=12)
    G.add_edge("F", "H", weight=-7)
    G.add_edge("F", "I", weight=10)
    G.add_edge("G", "J", weight=7)
    G.add_edge("H", "I", weight=3)
    G.add_edge("H", "J", weight=-2)
    G.add_edge("I", "J", weight=5)

    with pytest.raises(ValueError): #deve lançar uma exceção ValueError mesmo se no caminho soliticitado nao houver pesos negativos?
        dijkstra(G, "A", "C")
    
    with pytest.raises(ValueError):
       dijkstra(G, "A", "J")


def test_djikstra_with_inexistent_path():
    """
    GIVEN um grafo onde não existe um caminho entre o nó inicial e o nó de destino
    WHEN dijkstra for chamado
    THEN deve retornar a tupla (float('inf'), None)
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=10)
    G.add_edge("A", "C", weight=17)
    G.add_edge("A", "D", weight=10)
    G.add_edge("B", "C", weight=5)
    G.add_edge("B", "E", weight=7)
    G.add_edge("C", "F", weight=3)
    G.add_edge("C", "H", weight=4)
    G.add_edge("D", "F", weight=10)
    G.add_edge("E", "G", weight=12)
    G.add_edge("E", "H", weight=12)
    G.add_edge("F", "H", weight=7)
    G.add_edge("F", "I", weight=10)
    G.add_edge("G", "J", weight=7)
    G.add_edge("H", "I", weight=3)
    G.add_edge("H", "J", weight=2)
    G.add_edge("I", "J", weight=5)

    result = dijkstra(G, "A", "K")
    assert result == (float('inf'), None)

def test_djikstra_with_same_start_and_end_node():
    """
    GIVEN um grafo onde o nó inicial e o nó de destino são o mesmo
    WHEN dijkstra for chamado
    THEN deve retornar a tupla (0, [nó_inicial]), indicando que o custo é zero e o caminho é apenas o nó inicial
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=10)
    G.add_edge("A", "C", weight=17)
    G.add_edge("A", "D", weight=10)
    G.add_edge("B", "C", weight=5)
    G.add_edge("B", "E", weight=7)
    G.add_edge("C", "F", weight=3)
    G.add_edge("C", "H", weight=4)
    G.add_edge("D", "F", weight=10)
    G.add_edge("E", "G", weight=12)
    G.add_edge("E", "H", weight=12)
    G.add_edge("F", "H", weight=7)
    G.add_edge("F", "I", weight=10)
    G.add_edge("G", "J", weight=7)
    G.add_edge("H", "I", weight=3)
    G.add_edge("H", "J", weight=2)
    G.add_edge("I", "J", weight=5)

    result = dijkstra(G, "A", "A")
    assert result == (0, ["A"])

def test_djikstra_with_only_one_valid_path():
    """
    GIVEN um grafo onde existe apenas um caminho válido entre o nó inicial e o nó de destino
    WHEN dijkstra for chamado
    THEN deve retornar o custo e o caminho correto
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=10)
    G.add_edge("A", "C", weight=17)
    G.add_edge("A", "D", weight=10)
    G.add_edge("B", "C", weight=5)
    G.add_edge("B", "E", weight=7)
    G.add_edge("C", "F", weight=3)
    G.add_edge("C", "H", weight=4)
    G.add_edge("D", "F", weight=10)
    G.add_edge("E", "G", weight=12)
    G.add_edge("E", "H", weight=12)
    G.add_edge("F", "H", weight=7)
    G.add_edge("F", "I", weight=10)
    G.add_edge("G", "J", weight=7)
    G.add_edge("H", "I", weight=3)
    G.add_edge("H", "J", weight=2)
    G.add_edge("I", "J", weight=5)

    result = dijkstra(G, "A", "J")
    assert result == (21, ['A', 'B', 'C', 'H', 'J'])

def test_djikstra_with_two_paths_equivalent_in_cost():
    """
    GIVEN um grafo onde existem dois caminhos com o mesmo custo entre o nó inicial e o nó de destino
    WHEN dijkstra for chamado
    THEN deve retornar o custo correto e o primeiro caminho encontrado
    """ 
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=10)
    G.add_edge("A", "C", weight=15)
    G.add_edge("A", "D", weight=10)
    G.add_edge("B", "C", weight=5)
    G.add_edge("B", "E", weight=7)
    G.add_edge("C", "F", weight=3)
    G.add_edge("C", "H", weight=7)
    G.add_edge("D", "F", weight=10)
    G.add_edge("E", "G", weight=12)
    G.add_edge("E", "H", weight=12)
    G.add_edge("F", "H", weight=4)
    G.add_edge("F", "I", weight=10)
    G.add_edge("G", "J", weight=7)
    G.add_edge("H", "I", weight=1)
    G.add_edge("H", "J", weight=2)
    G.add_edge("I", "J", weight=1) 

    result = dijkstra(G, "A", "J")
    assert result == (24, ['A', 'C', 'H', 'J'])