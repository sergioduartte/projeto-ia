"""
Testes para a função build_graph.
Garante que o grafo é criado corretamente e que as conexões são válidas.
"""

import json
import pytest
from core.build_graph import build_graph

def test_graph_none(tmp_path):
    """
    GIVEN um conjunto de arestas vazio
    WHEN build_graph for chamado
    THEN deve lançar uma exceção ValueError
    """
    data = {"edges": []}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    with pytest.raises(Exception):
        build_graph(str(json_file))

def test_graph_edge_wrong_format(tmp_path):
    """
    GIVEN um conjunto de arestas inválido
    WHEN build_graph for chamado
    THEN deve lançar uma exceção ValueError
    """
    data = {"edges": [["A"]]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    with pytest.raises(Exception):
        build_graph(str(json_file))

def test_graph_wrong_edge_length(tmp_path):
    """
    GIVEN uma aresta com tamanho faltando 
    WHEN build_graph for chamado
    THEN deve lançar ValueError
    """
    data = {"edges": [["A", "B"]]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    with pytest.raises(ValueError):
        build_graph(str(json_file))

def test_graph_negative_weight(tmp_path):
    """
    GIVEN um conjunto de arestas válido
    WHEN build_graph for chamado
    THEN deve lançar uma exceção ValueError
    """
    data = {"edges": [["A", "B", -3]]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    with pytest.raises(ValueError):
        build_graph(str(json_file))

def test_graph_loop_positive_weight(tmp_path):
    """
    GIVEN um conjunto de aresta com nós iguais mas peso diferente de zero
    WHEN build_graph for chamado
    THEN deve lançar uma exceção ValueError
    """
    data = {"edges": [["A", "A", 4]]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    with pytest.raises(ValueError):
        build_graph(str(json_file))

def test_graph_weight_not_number(tmp_path):
    """
    GIVEN um conjunto de arestas com peso diferente de um número
    WHEN build_graph for chamado
    THEN deve lançar uma exceção ValueError
    """
    data = {"edges": [["A", "B", "cinco"]]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    with pytest.raises(ValueError):
        build_graph(str(json_file))

def test_graph_file_not_found():
    """
    GIVEN um caminho de arquivo que não existe
    WHEN build_graph for chamado
    THEN deve lançar FileNotFoundError
    """
    with pytest.raises(FileNotFoundError):
        build_graph("arquivo_que_nao_existe.json")

def test_graph_invalid_json_format(tmp_path):
    """
    GIVEN um arquivo JSON mal formatado
    WHEN build_graph for chamado
    THEN deve lançar json.JSONDecodeError
    """
    json_file = tmp_path / "graph.json"
    json_file.write_text('{"edges": [ ["A", "B", 10], }')

    with pytest.raises(json.JSONDecodeError):
        build_graph(str(json_file))

def test_graph_valid(tmp_path):
    """
    GIVEN um conjunto de arestas válido
    WHEN build_graph for chamado
    THEN deve verificar que o grafo resultante está correto
    """
    data = {"edges": [["A", "B", 5],["B", "C", 2],["C", "D", 1],]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    graph = build_graph(str(json_file))

    assert set(graph.nodes()) == {"A", "B", "C", "D"}
    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 3
    assert graph["A"]["B"]["weight"] == 5
    assert graph["B"]["C"]["weight"] == 2
    assert graph["C"]["D"]["weight"] == 1

def test_graph_multiple_edges(tmp_path):
    """
    GIVEN várias arestas válidas
    WHEN build_graph for chamado
    THEN o grafo deve ser criado com todos os nós e arestas corretamente
    """
    data = {"edges": [["A", "B", 3],["A", "C", 5],["B", "D", 2],
                      ["C", "D", 1],["D", "E", 4],]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    graph = build_graph(str(json_file))

    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 5
    assert graph["A"]["B"]["weight"] == 3
    assert graph["C"]["D"]["weight"] == 1

def test_graph_numeric_nodes(tmp_path):
    """
    GIVEN nós representados como números
    WHEN build_graph for chamado
    THEN o grafo deve ser criado corretamente
    """
    data = {"edges": [[1, 2, 10], [2, 3, 5]]}
    json_file = tmp_path / "graph.json"
    json_file.write_text(json.dumps(data))

    graph = build_graph(str(json_file))

    assert set(graph.nodes()) == {1, 2, 3}
    assert graph.number_of_nodes() == 3
    assert graph.number_of_edges() == 2
    assert graph[1][2]["weight"] == 10
    assert graph[2][3]["weight"] == 5
