import networkx as nx


def create_dependency_graph(dependencies):
    graph = nx.DiGraph()

    for dependency in dependencies:
        source = dependency["source"]
        target = dependency["target"]

        graph.add_node(source)
        graph.add_node(target)

        graph.add_edge(source, target)

    return graph


def display_graph(graph):
    print("\n=== Dependency Graph ===")

    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")

    print("\nRelationships:")

    for source, target in graph.edges():
        print(f"  {source} ---> {target}")