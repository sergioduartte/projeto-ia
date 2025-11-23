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
    file = tmp_path / "data.json"
    content = {"edges": []}
    file.write_text(json.dumps(content), encoding="utf-8")

    result = validate_path(str(file))
    assert result == content

def test_validate_path_file_not_found():
    with pytest.raises(FileNotFoundError):
        validate_path("nonexistent.json")

def test_validate_path_invalid_json(tmp_path):
    file = tmp_path / "broken.json"
    file.write_text("{invalid_json}", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        validate_path(str(file))

def test_validate_graph_entry_valid(tmp_path):
    file = tmp_path / "graph.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 3], ["B", "C", 2]]
    }), encoding="utf-8")

    edges = validate_graph_entry(str(file))
    assert edges == [["A", "B"], ["B", "C"]]

def test_validate_graph_entry_empty_graph(tmp_path):
    file = tmp_path / "empty.json"
    file.write_text(json.dumps({"edges": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="Graph can't be empty"):
        validate_graph_entry(str(file))

def test_validate_graph_entry_negative_weight(tmp_path):
    file = tmp_path / "neg.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", -1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError):
        validate_graph_entry(str(file))

def test_validate_graph_entry_invalid_weight_type(tmp_path):
    file = tmp_path / "invalid.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", "x"]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="needs to be a number"):
        validate_graph_entry(str(file))

def test_validate_graph_entry_loop_wrong_weight(tmp_path):
    file = tmp_path / "loop.json"
    file.write_text(json.dumps({
        "edges": [["A", "A", 5]]
    }), encoding="utf-8")

    with pytest.raises(ValueError):
        validate_graph_entry(str(file))

def test_validate_vertices_entry_found(tmp_path):
    file = tmp_path / "valid.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 1], ["B", "C", 2]]
    }), encoding="utf-8")

    validate_vertices_entry(str(file), "A", "C")

def test_validate_vertices_entry_missing_node(tmp_path):
    file = tmp_path / "missing.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="Node C not found"):
        validate_vertices_entry(str(file), "A", "C")

def test_validate_entries_valid(tmp_path):
    file = tmp_path / "ok.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", 2]]
    }), encoding="utf-8")

    validate_entries(str(file), "A", "B")

def test_validate_entries_invalid(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text(json.dumps({
        "edges": [["A", "B", -1]]
    }), encoding="utf-8")

    with pytest.raises(Exception):
        validate_entries(str(file), "A", "B")

def test_has_negative_weight_true():
    g = nx.Graph()
    g.add_edge("A", "B", weight=-5)
    assert has_negative_weight(g) is True

def test_has_negative_weight_false():
    g = nx.Graph()
    g.add_edge("A", "B", weight=3)
    assert has_negative_weight(g) is False

def test_validate_objects_valid():
    g = nx.Graph()
    g.add_edge("A", "B", weight=1)
    validate_objects(g, "A", "B")

def test_validate_objects_none():
    with pytest.raises(AttributeError):
        validate_objects(None, "A", "B")

def test_validate_objects_empty_graph():
    g = nx.Graph()
    with pytest.raises(ValueError, match="Graph can't be empty"):
        validate_objects(g, "A", "B")

def test_validate_objects_missing_nodes():
    g = nx.Graph()
    g.add_edge("A", "B", weight=1)
    with pytest.raises(ValueError, match="Graph must contain the specified nodes"):
        validate_objects(g, "A", "C")

def test_validate_objects_negative_weight():
    g = nx.Graph()
    g.add_edge("A", "B", weight=-1)
    with pytest.raises(ValueError, match="negative weight"):
        validate_objects(g, "A", "B")

def test_validate_graph_entry_vertex_a_empty(tmp_path):
    file = tmp_path / "emptyA.json"
    file.write_text(json.dumps({
        "edges": [["", "B", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="vertixA is empty"):
        validate_graph_entry(str(file))

def test_validate_graph_entry_vertex_b_empty(tmp_path):
    file = tmp_path / "emptyB.json"
    file.write_text(json.dumps({
        "edges": [["A", "", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="vertixB is empty"):
        validate_graph_entry(str(file))

def test_validate_vertices_entry_vertex_a_not_found(tmp_path):
    file = tmp_path / "missingA.json"
    file.write_text(json.dumps({
        "edges": [["B", "C", 1]]
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="Node A not found"):
        validate_vertices_entry(str(file), "A", "C")


