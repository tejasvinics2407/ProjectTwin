from backend.dependency_model import Dependency, DependencyModel
from backend.project_model import ProjectModel


def build_dependency_model(project_model: ProjectModel):
    """
    Build a language-independent dependency model
    from the common ProjectModel.
    """

    dependency_model = DependencyModel()

    # --------------------------------------------------
    # Create lookup tables
    # --------------------------------------------------

    files = {
        project_file.path: project_file
        for project_file in project_model.files
    }

    symbols = {}

    for project_file in project_model.files:

        for symbol in project_file.symbols:

            symbols.setdefault(
                symbol.name,
                []
            ).append(symbol)

    # --------------------------------------------------
    # Analyze every file
    # --------------------------------------------------

    for project_file in project_model.files:

        source_file = project_file.path

        # --------------------------------------------------
        # Import dependencies
        # --------------------------------------------------

        for imported in project_file.imports:

            imported_name = imported.strip()

            target_file = None

            # Try to match import against project files
            for file_path in files:

                file_stem = (
                    file_path.rsplit("/", 1)[-1]
                    .rsplit(".", 1)[0]
                )

                normalized_import = (
                    imported_name
                    .replace("/", ".")
                    .replace("\\", ".")
                )

                if (
                    normalized_import == file_stem
                    or normalized_import.endswith(
                        "." + file_stem
                    )
                    or file_stem in normalized_import
                ):

                    target_file = file_path
                    break

            if target_file is None:
                continue

            if target_file == source_file:
                continue

            dependency_model.add_dependency(
                Dependency(
                    source_file=source_file,
                    source_symbol=None,
                    target_file=target_file,
                    target_symbol=None,
                    relationship_type="imports",
                    evidence=f"Import detected: {imported}"
                )
            )

        # --------------------------------------------------
        # Function / method call dependencies
        # --------------------------------------------------

        for symbol in project_file.symbols:

            for called_name in symbol.calls:

                called_name = (
                    called_name.split(".")[-1]
                )

                possible_targets = (
                    symbols.get(
                        called_name,
                        []
                    )
                )

                for target_symbol in possible_targets:

                    if (
                        target_symbol.file
                        == source_file
                        and target_symbol.name
                        == symbol.name
                    ):
                        continue

                    dependency_model.add_dependency(
                        Dependency(
                            source_file=source_file,
                            source_symbol=symbol.name,
                            target_file=target_symbol.file,
                            target_symbol=target_symbol.name,
                            relationship_type="calls",
                            evidence=(
                                f"{symbol.name}() "
                                f"calls "
                                f"{target_symbol.name}()"
                            )
                        )
                    )

    return dependency_model