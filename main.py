"""
Classe responsável pela CLI com o usuário.
"""
import json
import argparse

from core.build_graph import build_graph
from core.dijkstra import dijkstra


def main():
    """
    Fluxo principal do programa.
    Define os parâmetros de entrada e faz as chamadas ao módulo build_graph e dijkstra.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("json", type=str, help="Path to the json file")
    parser.add_argument("-s", "--start", type=str, required=True, help="Origin city")
    parser.add_argument("-e", "--end", type=str, required=True, help="Destination city")

    args = parser.parse_args()

    try:
        graph = build_graph(args.json)
    except FileNotFoundError as exc:
        print(f"JSON file can't be found: {exc}")
    except json.JSONDecodeError as exc:
        print(f"JSON file isn't valid: {exc}")
    except ValueError as exc:
        print(f"The graph isn't valid: {exc}")
    try:
        dist, path = dijkstra(graph, args.start, args.end)
    except AttributeError as exc:
        print(f"Some of the parameters are None: {exc}")
    except ValueError as exc:
        print(f"Graph empty or with invalid nodes/weights: {exc}")

    print(f"The shortest path distance is {dist:.1f} km")
    print("Path:", ", ".join(path))

    return 0


if __name__ == '__main__':
    main()
