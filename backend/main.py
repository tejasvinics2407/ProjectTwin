from pathlib import Path

from backend.project_scanner import scan_project
from backend.github_ingestion import clone_repository

from backend.code_parser import parse_python_file

from backend.parser_manager import parse_file

from backend.project_model import ProjectModel

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

    return str(path).replace(
        "\\",
        "/"
    ).strip("/")


def analyze_project(project_path):

    project_root = Path(
        project_path
    ).resolve()

    files = scan_project(
        project_root
    )

    print("\n=== ProjectTwin Analysis ===")

    print(
        f"Found {len(files)} files"
    )

    parsed_files = []

    # =====================================================
    # COMMON PROJECT MODEL
    # =====================================================

    project_model = ProjectModel()

    # =====================================================
    # PARSE PROJECT FILES
    # =====================================================

    for file_path in files:

        # -------------------------------------------------
        # Detect language + select parser automatically
        # -------------------------------------------------

        full_path = (
            project_root / file_path
        )

        try:

            project_file = parse_file(
                str(full_path),
                normalize_path(
                    file_path
                )
            )

            # -------------------------------------------------
            # Unsupported file type
            # -------------------------------------------------

            if project_file is None:

                continue

            # -------------------------------------------------
            # Add to common ProjectModel
            # -------------------------------------------------

            project_model.add_file(
                project_file
            )

            print(
                f"\n📄 {project_file.path}"
            )

            print(
                f"  Language: "
                f"{project_file.language}"
            )

            print(
                "  Imports:"
            )

            for item in project_file.imports:

                print(
                    f"    - {item}"
                )

            print(
                "  Symbols:"
            )

            for symbol in project_file.symbols:

                print(
                    f"    - "
                    f"{symbol.symbol_type}: "
                    f"{symbol.name}"
                )

            # -------------------------------------------------
            # Existing Python knowledge format
            # -------------------------------------------------

            if project_file.language == "python":

                python_result = parse_python_file(
                    str(full_path)
                )

                python_result["file"] = (
                    normalize_path(
                        file_path
                    )
                )

                parsed_files.append(
                    python_result
                )

        except Exception as error:

            print(
                f"  Could not parse "
                f"{file_path}: "
                f"{error}"
            )

    # =====================================================
    # PROJECT MODEL SUMMARY
    # =====================================================

    print(
        "\n=== Project Model ==="
    )

    model_summary = (
        project_model.summary()
    )

    print(
        f"  Files: "
        f"{model_summary['file_count']}"
    )

    print(
        f"  Symbols: "
        f"{model_summary['symbol_count']}"
    )

    print(
        f"  Languages: "
        f"{', '.join(model_summary['languages'])}"
    )

    # =====================================================
    # SAVE EXISTING KNOWLEDGE BASE
    # =====================================================

    save_knowledge_base(
        parsed_files,
        "data/knowledge_base.json"
    )

    # =====================================================
    # BUILD EXISTING PYTHON FILE DEPENDENCIES
    # =====================================================

    dependencies = build_dependencies(
        str(project_root),
        parsed_files
    )

    print(
        "\n=== Dependency Relationships ==="
    )

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

        display_graph(
            graph
        )

    else:

        print(
            "  No internal Python "
            "project dependencies found."
        )

        graph = create_dependency_graph(
            []
        )

    # =====================================================
    # BUILD EXISTING PYTHON FUNCTION DEPENDENCIES
    # =====================================================

    function_dependencies = (
        build_function_dependencies(
            project_path,
            parsed_files
        )
    )

    print(
        "\n=== Function Dependencies ==="
    )

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
            "  No Python function dependencies found."
        )

    # =====================================================
    # RETURN EXISTING FORMAT
    # =====================================================

    return (
        graph,
        function_dependencies
    )


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

    print(
        "\n=== CHANGE SIMULATION ==="
    )

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

    print(
        "\nDirect dependencies:"
    )

    for file in simulation[
        "direct_dependencies"
    ]:

        print(
            f"  - {file}"
        )

    print(
        "\nIndirect dependencies:"
    )

    for file in simulation[
        "indirect_dependencies"
    ]:

        print(
            f"  - {file}"
        )

    print(
        "\nFunction-level impact:"
    )

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

    print(
        "\nPredicted removed:"
    )

    for file in simulation[
        "removed"
    ]:

        print(
            f"  - {file}"
        )

    print(
        "\nPredicted modified:"
    )

    for file in simulation[
        "modified"
    ]:

        print(
            f"  - {file}"
        )

    print(
        "\nPredicted added:"
    )

    for file in simulation[
        "added"
    ]:

        print(
            f"  - {file}"
        )

    print(
        "\nPossible breakage:"
    )

    for item in simulation[
        "possible_breakage"
    ]:

        print(
            f"  - {item['file']}: "
            f"{item['reason']}"
        )