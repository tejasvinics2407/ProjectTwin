import networkx as nx

from impact_analyzer import find_impact


# Create a small example dependency graph
graph = nx.DiGraph()

graph.add_edge("test_utils.py", "utils.py")
graph.add_edge("models.py", "utils.py")
graph.add_edge("api.py", "models.py")


# Imagine we want to change utils.py
changed_file = "utils.py"

result = find_impact(
    graph,
    changed_file
)

print("\n=== ProjectTwin Change Impact Analysis ===")
print("Changed file:", result["changed_file"])

print("\nImpact count:", result["impact_count"])

print("\nPotentially affected files:")

for file in result["affected_files"]:
    print("-", file)