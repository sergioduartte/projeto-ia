"""
Testes para a implementação do algoritmo de Dijkstra.
Verifica se os caminhos estão sendo calculados corretamente 
e se está lidando corretamente com os paramentros passados.
"""

import networkx as nx
import pytest

from core.dijkstra import dijkstra

def test_dijkstra_with_graph_none():
    """
    GIVEN nenhum grafo passado para a função dijkstra
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção AttributeError
    """
    with pytest.raises(AttributeError):
        dijkstra(None, "A", "B")

def test_dijkstra_with_empty_graph():
    """
    GIVEN um grafo com nós e sem arestas (grafo vazio)
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(["A", "B", "C"])

    with pytest.raises(ValueError):
        dijkstra(graph, "A", "B")


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
    graph = nx.DiGraph()

    with pytest.raises(ValueError):
        dijkstra(graph, "A", "B")

def test_djikstra_with_nonexistent_start_node():
    """
    GIVEN um grafo com alguns nós, mas o nó inicial não existe
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(["B", "C", "D"])
    graph.add_edges_from([("B", "C"), ("C", "D")])

    with pytest.raises(ValueError):
        dijkstra(graph, "A", "B")

def test_djikstra_with_nonexistent_end_node():
    """
    GIVEN um grafo com alguns nós, mas o nó de destino não existe
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(["A", "B", "C"])
    graph.add_edges_from([("A", "B"), ("B", "C")])

    with pytest.raises(ValueError):
        dijkstra(graph, "A", "D")

def test_djikstra_with_nonexistent_start_and_end_nodes():
    """
    GIVEN um grafo com alguns nós, mas o nó de destino não existe
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(["B", "C", "D"])
    graph.add_edges_from([("B", "C"), ("C", "D")])

    with pytest.raises(ValueError):
        dijkstra(graph, "A", "E")

def test_djikstra_with__negative_weights():
    """
    GIVEN um grafo com pesos negativos nas arestas
    WHEN dijkstra for chamado
    THEN deve lançar uma exceção ValueError
    """
    graph = nx.DiGraph()
    graph.add_edge("A", "B", weight=10)
    graph.add_edge("A", "C", weight=17)
    graph.add_edge("A", "D", weight=10)
    graph.add_edge("B", "C", weight=-5)
    graph.add_edge("B", "E", weight=7)
    graph.add_edge("C", "F", weight=3)
    graph.add_edge("C", "H", weight=4)
    graph.add_edge("D", "F", weight=10)
    graph.add_edge("E", "graph", weight=12)
    graph.add_edge("E", "H", weight=12)
    graph.add_edge("F", "H", weight=-7)
    graph.add_edge("F", "I", weight=10)
    graph.add_edge("graph", "J", weight=7)
    graph.add_edge("H", "I", weight=3)
    graph.add_edge("H", "J", weight=-2)
    graph.add_edge("I", "J", weight=5)

    with pytest.raises(ValueError):
        dijkstra(graph, "A", "C")

    with pytest.raises(ValueError):
        dijkstra(graph, "A", "J")

def test_djikstra_with_inexistent_path():
    """
    GIVEN um grafo onde não existe um caminho entre o nó inicial e o nó de destino
    WHEN dijkstra for chamado
    THEN deve retornar a tupla (float('inf'), None)
    """
    graph = nx.DiGraph()
    graph.add_edge("A", "B", weight=10)
    graph.add_edge("A", "C", weight=17)
    graph.add_edge("A", "D", weight=10)
    graph.add_edge("B", "C", weight=5)
    graph.add_edge("B", "E", weight=7)
    graph.add_edge("C", "F", weight=3)
    graph.add_edge("C", "H", weight=4)
    graph.add_edge("D", "F", weight=10)
    graph.add_edge("E", "graph", weight=12)
    graph.add_edge("E", "H", weight=12)
    graph.add_edge("F", "H", weight=7)
    graph.add_edge("F", "I", weight=10)
    graph.add_edge("graph", "J", weight=7)
    graph.add_edge("H", "I", weight=3)
    graph.add_edge("H", "J", weight=2)
    graph.add_edge("I", "J", weight=5)

    result = dijkstra(graph, "B", "D")
    assert result == (float('inf'), None)

def test_djikstra_with_same_start_and_end_node():
    """
    GIVEN um grafo onde o nó inicial e o nó de destino são o mesmo
    WHEN dijkstra for chamado
    THEN deve retornar a tupla (0, [nó_inicial]), 
    indicando que o custo é zero e o caminho é apenas o nó inicial
    """
    graph = nx.DiGraph()
    graph.add_edge("A", "B", weight=10)
    graph.add_edge("A", "C", weight=17)
    graph.add_edge("A", "D", weight=10)
    graph.add_edge("B", "C", weight=5)
    graph.add_edge("B", "E", weight=7)
    graph.add_edge("C", "F", weight=3)
    graph.add_edge("C", "H", weight=4)
    graph.add_edge("D", "F", weight=10)
    graph.add_edge("E", "graph", weight=12)
    graph.add_edge("E", "H", weight=12)
    graph.add_edge("F", "H", weight=7)
    graph.add_edge("F", "I", weight=10)
    graph.add_edge("graph", "J", weight=7)
    graph.add_edge("H", "I", weight=3)
    graph.add_edge("H", "J", weight=2)
    graph.add_edge("I", "J", weight=5)

    result = dijkstra(graph, "A", "A")
    assert result == (0, ["A"])

def test_djikstra_with_only_one_valid_path():
    """
    GIVEN um grafo onde existe apenas um caminho válido entre o nó inicial e o nó de destino
    WHEN dijkstra for chamado
    THEN deve retornar o custo e o caminho correto
    """
    graph = nx.DiGraph()
    graph.add_edge("A", "B", weight=10)
    graph.add_edge("A", "C", weight=17)
    graph.add_edge("A", "D", weight=10)
    graph.add_edge("B", "C", weight=5)
    graph.add_edge("B", "E", weight=7)
    graph.add_edge("C", "F", weight=3)
    graph.add_edge("C", "H", weight=4)
    graph.add_edge("D", "F", weight=10)
    graph.add_edge("E", "graph", weight=12)
    graph.add_edge("E", "H", weight=12)
    graph.add_edge("F", "H", weight=7)
    graph.add_edge("F", "I", weight=10)
    graph.add_edge("graph", "J", weight=7)
    graph.add_edge("H", "I", weight=3)
    graph.add_edge("H", "J", weight=2)
    graph.add_edge("I", "J", weight=5)

    result = dijkstra(graph, "A", "J")
    assert result == (21, ['A', 'B', 'C', 'H', 'J'])

def test_djikstra_with_two_paths_equivalent_in_cost():
    """
    GIVEN um grafo onde existem dois caminhos com o mesmo custo entre o nó inicial e o nó de destino
    WHEN dijkstra for chamado
    THEN deve retornar o custo correto e o primeiro caminho encontrado
    """
    graph = nx.DiGraph()
    graph.add_edge("A", "B", weight=10)
    graph.add_edge("A", "C", weight=15)
    graph.add_edge("A", "D", weight=10)
    graph.add_edge("B", "C", weight=5)
    graph.add_edge("B", "E", weight=7)
    graph.add_edge("C", "F", weight=3)
    graph.add_edge("C", "H", weight=7)
    graph.add_edge("D", "F", weight=10)
    graph.add_edge("E", "graph", weight=12)
    graph.add_edge("E", "H", weight=12)
    graph.add_edge("F", "H", weight=4)
    graph.add_edge("F", "I", weight=10)
    graph.add_edge("graph", "J", weight=7)
    graph.add_edge("H", "I", weight=1)
    graph.add_edge("H", "J", weight=2)
    graph.add_edge("I", "J", weight=1)

    result = dijkstra(graph, "A", "J")
    assert result == (24, ['A', 'C', 'H', 'J'])

def test_dijkstra_direct_path_more_expensive():
    """
    GIVEN um grafo onde existe um caminho direto entre o nó inicial e o nó de destino,
    porém esse caminho direto é mais caro que um caminho alternativo
    WHEN dijkstra for chamado
    THEN deve retornar o custo e o caminho mais barato (mesmo tendo mais arestas)
    """
    graph = nx.DiGraph()
    graph.add_edge("M", "N", weight=10)
    graph.add_edge("M", "O", weight=15)
    graph.add_edge("M", "P", weight=10)
    graph.add_edge("M", "Z", weight=30) # Caminho direto
    graph.add_edge("N", "O", weight=5)
    graph.add_edge("N", "Q", weight=7)
    graph.add_edge("O", "R", weight=3)
    graph.add_edge("O", "T", weight=7)
    graph.add_edge("P", "R", weight=10)
    graph.add_edge("Q", "U", weight=12)
    graph.add_edge("Q", "T", weight=12)
    graph.add_edge("R", "T", weight=4)
    graph.add_edge("R", "V", weight=10)
    graph.add_edge("U", "W", weight=7)
    graph.add_edge("T", "V", weight=1)
    graph.add_edge("T", "Z", weight=2)
    graph.add_edge("V", "Z", weight=1)

    result = dijkstra(graph, "M", "Z")
    assert result == (24, ['M', 'O', 'T', 'Z'])

def test_dijkstra_direct_path_vs_two_alternatives():
    """
    GIVEN um grafo onde existe um caminho direto caro entre o nó inicial e o nó de destino,
    e rotas alternativas mais baratas ou mais caras com múltiplas cidades intermediárias,
    WHEN dijkstra for chamado,
    THEN deve retornar o caminho de menor custo, mesmo que seja mais longo.
    """
    graph = nx.DiGraph()
    graph.add_edge("L", "Z", weight=90) # caminho direto
    graph.add_edge("L", "A", weight=20)
    graph.add_edge("A", "D", weight=10)
    graph.add_edge("D", "Z", weight=40)
    graph.add_edge("A", "X", weight=5)
    graph.add_edge("X", "Z", weight=60)
    graph.add_edge("L", "B", weight=10)
    graph.add_edge("B", "C", weight=15)
    graph.add_edge("C", "E", weight=12)
    graph.add_edge("E", "Z", weight=18)
    graph.add_edge("C", "F", weight=50)
    graph.add_edge("F", "Z", weight=2)
    graph.add_edge("B", "graph", weight=5)
    graph.add_edge("graph", "H", weight=35)
    graph.add_edge("H", "Z", weight=40)

    result = dijkstra(graph, "L", "Z")
    assert result == (55, ["L", "B", "C", "E", "Z"])

def test_dijkstra_cycle_graph_with_shortcut():
    """
    GIVEN um grafo onde as cidades formam um ciclo
    e existe um caminho de menor custo alternativo entre duas cidades
    WHEN dijkstra for chamado
    THEN deve retornar o caminho direto mais barato
    """
    graph = nx.DiGraph()

    # ciclo
    graph.add_edge("A", "B", weight=10)
    graph.add_edge("B", "C", weight=10)
    graph.add_edge("C", "D", weight=10)
    graph.add_edge("D", "E", weight=10)
    graph.add_edge("E", "A", weight=10)
    # caminho alternativo
    graph.add_edge("A", "D", weight=15)

    result = dijkstra(graph, "A", "D")
    assert result == (15, ["A", "D"])

def test_dijkstra_bottleneck_path_ignored():
    """
    GIVEN um grafo com vários caminhos possíveis entre o nó inicial e o nó de destino,
    incluindo caminhos que parecem curtos mas possuem um gargalo no meio,
    WHEN dijkstra for chamado,
    THEN deve ignorar caminhos com arestas muito caras e escolher a rota realmente mais barata.
    """
    graph = nx.DiGraph()
    graph.add_edge("S", "A", weight=5)
    graph.add_edge("A", "B", weight=5)
    graph.add_edge("B", "X", weight=3)
    graph.add_edge("X", "Z", weight=50)
    graph.add_edge("B", "Y", weight=2)
    graph.add_edge("Y", "Z", weight=40)
    graph.add_edge("S", "C", weight=10)
    graph.add_edge("C", "D", weight=5)
    graph.add_edge("D", "E", weight=5)
    graph.add_edge("E", "F", weight=5)
    graph.add_edge("F", "Z", weight=5)
    graph.add_edge("S", "graph", weight=8)
    graph.add_edge("graph", "H", weight=10)
    graph.add_edge("H", "Z", weight=20)
    graph.add_edge("A", "K", weight=1)
    graph.add_edge("K", "Z", weight=80)

    result = dijkstra(graph, "S", "Z")

    assert result == (30, ["S", "C", "D", "E", "F", "Z"])
