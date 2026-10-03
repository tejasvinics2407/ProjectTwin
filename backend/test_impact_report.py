from impact_report import generate_impact_report

import networkx as nx


# Create a small test dependency graph
graph = nx.DiGraph()

graph.add_edge(
    "src/requests/models.py",
    "src/requests/utils.py"
)

graph.add_edge(
    "src/requests/api.py",
    "src/requests/models.py"
)

graph.add_edge(
    "tests/test_utils.py",
    "src/requests/utils.py"
)


# Repository containing Git history
repo_path = "data/repos/requests_git_project"

# File we want to change
changed_file = "src/requests/utils.py"


# Generate combined impact report
report = generate_impact_report(
    graph,
    repo_path,
    changed_file
)


# Display the report
print("\n=== ProjectTwin Impact Report ===")

print("\nChanged file:")
print(report["changed_file"])

print("\nImpact count:")
print(report["impact_count"])

print("\nAffected files:")

for file in report["affected_files"]:
    print("-", file)

print("\nGit History:")
print(report["git_history"])