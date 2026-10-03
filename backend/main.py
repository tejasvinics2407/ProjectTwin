from pathlib import Path

from backend.project_scanner import scan_project
from backend.github_ingestion import clone_repository
from backend.code_parser import parse_python_file

from backend.dependency_analyzer import (
    build_dependencies,
    build_function_dependencies
)

from backend.dependency_graph import (
    create_dependency_graph,
    display_graph
)

from backend.knowledge_base import save_knowledge_base
from backend.change_simulator import predict_change


def normalize_path(path):
    """
    Convert Windows paths to a consistent
    repository-relative POSIX path.
    """
    return str(path).replace("\\", "/").strip("/")


def analyze_project(project_path):

    project_root = Path(project_path).resolve()

    files = scan_project(project_root)

    print("\n=== ProjectTwin Analysis ===")
    print(f"Found {len(files)} files")

    parsed_files = []

    # =====================================================
    # PARSE PROJECT FILES
    # =====================================================

    for file_path in files:

        if not file_path.endswith(".py"):
            continue

        # Full path is used ONLY for reading the file.
        full_path = project_root / file_path

        try:

            result = parse_python_file(
                str(full_path)
            )

            # IMPORTANT:
            # Store ONLY the repository-relative path
            # inside the ProjectTwin knowledge graph.
            result["file"] = normalize_path(
                file_path
            )

            parsed_files.append(result)

            print(f"\n📄 {result['file']}")

            print("  Imports:")

            for item in result["imports"]:
                print(f"    - {item}")

            print("  Functions:")

            for item in result["functions"]:
                print(f"    - {item}")

            print("  Classes:")

            for item in result["classes"]:
                print(f"    - {item}")

        except Exception as error:

            print(
                f"  Could not parse {file_path}: "
                f"{error}"
            )

    # =====================================================
    # SAVE KNOWLEDGE BASE
    # =====================================================

    save_knowledge_base(
        parsed_files,
        "data/knowledge_base.json"
    )

    # =====================================================
    # BUILD FILE DEPENDENCIES
    # =====================================================

    dependencies = build_dependencies(
        str(project_root),
        parsed_files
    )

    print("\n=== Dependency Relationships ===")

    if dependencies:

        for dependency in dependencies:

            print(
                f"  "
                f"{dependency['source']}"
                f"  --->  "
                f"{dependency['target']}"
            )

        graph = create_dependency_graph(
            dependencies
        )

        display_graph(graph)

    else:

        print(
            "  No internal project dependencies found."
        )

        graph = create_dependency_graph([])

    # =====================================================
    # BUILD FUNCTION DEPENDENCIES
    # =====================================================

    function_dependencies = build_function_dependencies(
        project_path,
        parsed_files
    )

    print("\n=== Function Dependencies ===")

    if function_dependencies:

        for dependency in function_dependencies:

            print(
                f"  "
                f"{dependency['source_file']}:"
                f"{dependency['source_function']}()"
                f" ---> "
                f"{dependency['target_file']}:"
                f"{dependency['target_function']}()"
            )

    else:

        print(
            "  No function dependencies found."
        )

    return graph, function_dependencies


if __name__ == "__main__":

    # =====================================================
    # GET REPOSITORY
    # =====================================================

    repo_url = input(
        "Enter GitHub repository URL: "
    )

    destination = Path(
        "data/repos/requests_git_project"
    )

    clone_repository(
        repo_url,
        destination
    )

    # =====================================================
    # ANALYZE PROJECT
    # =====================================================

    graph, function_dependencies = (
        analyze_project(
            destination
        )
    )

    # =====================================================
    # GET PROPOSED CHANGE
    # =====================================================

    changed_file = input(
        "\nEnter the file you want to change: "
    )

    changed_file = normalize_path(
        changed_file
    )

    change_description = input(
        "\nDescribe the change you want to make: "
    )

    changed_function = input(
        "\nEnter the function you want to change "
        "(press Enter if the whole file is changing): "
    ).strip()

    if not changed_function:
        changed_function = None

    # =====================================================
    # SIMULATE CHANGE
    # =====================================================

    simulation = predict_change(
        graph,
        changed_file,
        change_description,
        function_dependencies,
        changed_function
    )

    # =====================================================
    # DISPLAY RESULT
    # =====================================================

    print("\n=== CHANGE SIMULATION ===")

    print(
        f"\nChanged file: "
        f"{simulation['changed_file']}"
    )

    print(
        f"Change type: "
        f"{simulation['change_type']}"
    )

    print(
        f"Impact count: "
        f"{simulation['impact_count']}"
    )

    print("\nDirect dependencies:")

    for file in simulation[
        "direct_dependencies"
    ]:

        print(f"  - {file}")

    print("\nIndirect dependencies:")

    for file in simulation[
        "indirect_dependencies"
    ]:

        print(f"  - {file}")

    print("\nFunction-level impact:")

    for relationship in simulation[
        "function_impact"
    ]:

        print(
            f"  - "
            f"{relationship['dependent_function']}() "
            f"in "
            f"{relationship['dependent_file']} "
            f"depends on "
            f"{relationship['changed_function']}()"
        )

    print("\nPredicted removed:")

    for file in simulation["removed"]:

        print(f"  - {file}")

    print("\nPredicted modified:")

    for file in simulation["modified"]:

        print(f"  - {file}")

    print("\nPredicted added:")

    for file in simulation["added"]:

        print(f"  - {file}")

    print("\nPossible breakage:")

    for item in simulation[
        "possible_breakage"
    ]:

        print(
            f"  - {item['file']}: "
            f"{item['reason']}"
        )