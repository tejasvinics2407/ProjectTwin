from pathlib import Path


def get_module_name(file_path, project_path):
    """
    Convert a Python file path into its Python module name.

    Example:
        backend/engine/skill_gap_analyzer.py

    becomes:
        backend.engine.skill_gap_analyzer
    """

    file_path = Path(file_path)
    project_path = Path(project_path)

    try:
        relative_path = file_path.resolve().relative_to(
            project_path.resolve()
        )
    except ValueError:
        relative_path = file_path

    relative_path = relative_path.with_suffix("")

    return relative_path.as_posix().replace("/", ".")


def build_dependencies(project_path, parsed_files):
    """
    Build file-level dependencies using Python imports.
    """

    dependencies = []
    module_map = {}

    for file_info in parsed_files:

        file_path = Path(file_info["file"])

        if file_path.suffix != ".py":
            continue

        module_name = get_module_name(
            file_path,
            project_path
        )

        module_map[module_name] = file_info["file"]

    for file_info in parsed_files:

        source_file = file_info["file"]

        for imported_module in file_info.get(
            "imports",
            []
        ):

            for module_name, target_file in module_map.items():

                if (
                    imported_module == module_name
                    or imported_module.startswith(
                        module_name + "."
                    )
                    or module_name.endswith(
                        "." + imported_module
                    )
                ):

                    if source_file != target_file:

                        dependency = {
                            "source": source_file,
                            "target": target_file
                        }

                        if dependency not in dependencies:
                            dependencies.append(
                                dependency
                            )

    return dependencies


def build_function_dependencies(
    project_path,
    parsed_files
):
    """
    Build function-level dependencies.

    Also preserves information about how the
    result of a function call is used.

    Example:

        analyze_resume()
            |
            | calls
            v
        analyze_skill_gap()

    and:

        skill_gap = analyze_skill_gap(...)

    means the result is stored in:

        skill_gap
    """

    function_map = {}

    # ---------------------------------------------------------
    # Create map of all functions
    # ---------------------------------------------------------

    for file_info in parsed_files:

        file_name = file_info["file"]

        for function in file_info.get(
            "function_details",
            []
        ):

            function_name = function["name"]

            function_map[
                (
                    file_name,
                    function_name
                )
            ] = {
                "file": file_name,
                "function": function_name
            }

    # ---------------------------------------------------------
    # Create module map
    # ---------------------------------------------------------

    module_map = {}

    for file_info in parsed_files:

        file_path = Path(
            file_info["file"]
        )

        if file_path.suffix != ".py":
            continue

        module_name = get_module_name(
            file_path,
            project_path
        )

        module_map[
            module_name
        ] = file_info["file"]

    function_dependencies = []

    # ---------------------------------------------------------
    # Analyze every source file
    # ---------------------------------------------------------

    for file_info in parsed_files:

        source_file = file_info["file"]

        # -----------------------------------------------------
        # Find imported target files
        # -----------------------------------------------------

        imported_target_files = []

        for imported_module in file_info.get(
            "imports",
            []
        ):

            target_file = module_map.get(
                imported_module
            )

            if target_file:

                imported_target_files.append(
                    target_file
                )

        # -----------------------------------------------------
        # Analyze functions
        # -----------------------------------------------------

        for function in file_info.get(
            "function_details",
            []
        ):

            source_function = function["name"]

            called_functions = function.get(
                "calls",
                []
            )

            call_details = function.get(
                "call_details",
                []
            )

            # -------------------------------------------------
            # Build lookup for extra call information
            # -------------------------------------------------

            call_detail_map = {}

            for call in call_details:

                call_name = call.get(
                    "function"
                )

                if call_name:

                    call_detail_map[
                        call_name
                    ] = call

            # -------------------------------------------------
            # Check every called function
            # -------------------------------------------------

            for called_function in called_functions:

                # ---------------------------------------------
                # Imported function
                # ---------------------------------------------

                for target_file in imported_target_files:

                    target_key = (
                        target_file,
                        called_function
                    )

                    if target_key not in function_map:
                        continue

                    call_detail = call_detail_map.get(
                        called_function,
                        {}
                    )

                    dependency = {
                        "source_file": source_file,

                        "source_function": source_function,

                        "target_file": target_file,

                        "target_function": called_function,

                        "assigned_to": call_detail.get(
                            "assigned_to"
                        ),

                        "call_line": call_detail.get(
                            "line"
                        )
                    }

                    if dependency not in function_dependencies:

                        function_dependencies.append(
                            dependency
                        )

                # ---------------------------------------------
                # Same-file function
                # ---------------------------------------------

                target_key = (
                    source_file,
                    called_function
                )

                if target_key in function_map:

                    if called_function == source_function:
                        continue

                    call_detail = call_detail_map.get(
                        called_function,
                        {}
                    )

                    dependency = {
                        "source_file": source_file,

                        "source_function": source_function,

                        "target_file": source_file,

                        "target_function": called_function,

                        "assigned_to": call_detail.get(
                            "assigned_to"
                        ),

                        "call_line": call_detail.get(
                            "line"
                        )
                    }

                    if dependency not in function_dependencies:

                        function_dependencies.append(
                            dependency
                        )

    return function_dependencies