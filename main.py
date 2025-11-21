import argparse

from core.build_graph import build_graph
from core.dijkstra import dijkstra


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json", type=str, help="Path to the json file")
    parser.add_argument("-s", "--start", type=str, required=True, help="Origin city")
    parser.add_argument("-e", "--end", type=str, required=True, help="Destination city")

    args = parser.parse_args()

    # queria colocar alguma instrução em caso de erro

    try:
        graph = build_graph(args.json)
    except Exception as exc:
        print("Error in building graph: {exc}") 
    
    try:
        dist, path = dijkstra(graph, args.start, args.end)
    except Exception as exc:
        print("Error in running Dijkstra: {exc}") 

    print(f"The shortest path distance is {dist:.1f} km")
    print("Path:", ", ".join(path))

    return 0


if __name__ == '__main__':
    main()
