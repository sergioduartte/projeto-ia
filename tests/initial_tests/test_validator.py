"""
Testes unitários para o módulo util.validator.
Valida funções de validação de grafos, arquivos JSON e detecção erros nos grafos.
"""

import json
import pytest
import networkx as nx
from util.validator import (
    validate_path,
    validate_graph_entry,
    validate_vertices_entry,
    validate_entries,
    validate_objects,
    has_negative_weight,
)

def test_validate_path_valid_json(tmp_path):
    """Testa se validate_path retorna o conteúdo correto de um arquivo JSON válido."""
    file = tmp_path / "data.json"
    content = {"edges": []}
    file.write_text(json.dumps(content), encoding="utf-8")

    result = validate_path(str(file))
    assert result == content

def test_validate_path_file_not_found():
    """Testa se validate_path lança FileNotFoundError para arquivo inexistente."""
    with pytest.raises(FileNotFoundError):
        validate_path("nonexistent.json")

def test_validate_path_invalid_json(tmp_path):
    """Testa se validate_path lança JSONDecodeError para JSON com formato inválido."""
    file = tmp_path / "broken.json"
    file.write_text("{invalid_json}", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        validate_path(str(file))

def test_validate_graph_entry_valid(tmp_path):
    """Testa se validate_graph_entry retorna as arestas corretas de um grafo válido."""
    file = tmp_path / "graph.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 3], ["B", "C", 2]]
    }), encoding="utf-8")

    edges = validate_graph_entry(str(file))
    assert edges == [["A", "B"], ["B", "C"]]

def test_validate_graph_entry_empty_graph(tmp_path):
    """Testa se validate_graph_entry lança ValueError para grafo vazio."""
    file = tmp_path / "empty.json"
    file.write_text(json.dumps({"edges": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="Graph can't be empty"):
        validate_graph_entry(str(file))

def test_validate_graph_entry_negative_weight(tmp_path):
    """Testa se validate_graph_entry lança ValueError para pesos negativos."""
    file = tmp_path / "neg.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", -1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError):
        validate_graph_entry(str(file))

def test_validate_graph_entry_invalid_weight_type(tmp_path):
    """Testa se validate_graph_entry lança ValueError para peso com tipo inválido."""
    file = tmp_path / "invalid.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", "x"]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="needs to be a number"):
        validate_graph_entry(str(file))

def test_validate_graph_entry_loop_wrong_weight(tmp_path):
    """Testa se validate_graph_entry lança ValueError para loop com peso incorreto."""
    file = tmp_path / "loop.json"
    file.write_text(json.dumps({
        "edges": [["A", "A", 5]]
    }), encoding="utf-8")

    with pytest.raises(ValueError):
        validate_graph_entry(str(file))

def test_validate_vertices_entry_found(tmp_path):
    """Testa se validate_vertices_entry funciona corretamente para vértices existentes."""
    file = tmp_path / "valid.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 1], ["B", "C", 2]]
    }), encoding="utf-8")

    validate_vertices_entry(str(file), "A", "C")

def test_validate_vertices_entry_missing_node(tmp_path):
    """Testa se validate_vertices_entry lança ValueError para nó inexistente."""
    file = tmp_path / "missing.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="Node C not found"):
        validate_vertices_entry(str(file), "A", "C")

def test_validate_entries_valid(tmp_path):
    """Testa se validate_entries funciona corretamente com dados válidos."""
    file = tmp_path / "ok.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 2]]
    }), encoding="utf-8")

    validate_entries(str(file), "A", "B")

def test_validate_entries_invalid(tmp_path):
    """Testa se validate_entries lança exceção para dados inválidos."""
    file = tmp_path / "bad.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", -1]]
    }), encoding="utf-8")

    with pytest.raises(Exception):
        validate_entries(str(file), "A", "B")

def test_has_negative_weight_true():
    """Testa se has_negative_weight retorna True para grafo com peso negativo."""
    g = nx.Graph()
    g.add_edge("A", "B", weight=-5)
    assert has_negative_weight(g) is True

def test_has_negative_weight_false():
    """Testa se has_negative_weight retorna False para grafo sem peso negativo."""
    g = nx.Graph()
    g.add_edge("A", "B", weight=3)
    assert has_negative_weight(g) is False

def test_validate_objects_valid():
    """Testa se validate_objects funciona corretamente com objetos válidos."""
    g = nx.Graph()
    g.add_edge("A", "B", weight=1)
    validate_objects(g, "A", "B")

def test_validate_objects_none():
    """Testa se validate_objects lança AttributeError para objeto None."""
    with pytest.raises(AttributeError):
        validate_objects(None, "A", "B")

def test_validate_objects_empty_graph():
    """Testa se validate_objects lança ValueError para grafo vazio."""
    g = nx.Graph()
    with pytest.raises(ValueError, match="Graph can't be empty"):
        validate_objects(g, "A", "B")

def test_validate_objects_missing_nodes():
    """Testa se validate_objects lança ValueError para nós ausentes no grafo."""
    g = nx.Graph()
    g.add_edge("A", "B", weight=1)
    with pytest.raises(ValueError, match="Graph must contain the specified nodes"):
        validate_objects(g, "A", "C")

def test_validate_objects_negative_weight():
    """Testa se validate_objects lança ValueError para peso negativo."""
    g = nx.Graph()
    g.add_edge("A", "B", weight=-1)
    with pytest.raises(ValueError, match="negative weight"):
        validate_objects(g, "A", "B")

def test_validate_graph_entry_vertex_a_empty(tmp_path):
    """Testa se validate_graph_entry lança ValueError para vertixA vazio."""
    file = tmp_path / "emptyA.json"
    file.write_text(json.dumps({
        "edges": [["", "B", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="vertixA is empty"):
        validate_graph_entry(str(file))

def test_validate_graph_entry_vertex_b_empty(tmp_path):
    """Testa se validate_graph_entry lança ValueError para vertixB vazio."""
    file = tmp_path / "emptyB.json"
    file.write_text(json.dumps({
        "edges": [["A", "", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="vertixB is empty"):
        validate_graph_entry(str(file))

def test_validate_vertices_entry_vertex_a_not_found(tmp_path):
    """Testa se validate_vertices_entry lança ValueError quando vertixA não é encontrado."""
    file = tmp_path / "missingA.json"
    file.write_text(json.dumps({
        "edges": [["B", "C", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="Node A not found"):
        validate_vertices_entry(str(file), "A", "C")
