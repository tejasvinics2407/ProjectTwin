import ast


def get_called_names(node):
    """
    Find function names called inside an AST node.
    """

    called_names = []

    for child in ast.walk(node):

        if isinstance(child, ast.Call):

            if isinstance(child.func, ast.Name):

                called_names.append(
                    child.func.id
                )

            elif isinstance(child.func, ast.Attribute):

                called_names.append(
                    child.func.attr
                )

    return sorted(
        set(called_names)
    )


def get_function_call_details(node):
    """
    Capture more information about function calls.

    Example:

        skill_gap = analyze_skill_gap(...)

    becomes information describing:

        function: analyze_skill_gap
        assigned_to: skill_gap
    """

    calls = []

    for child in ast.walk(node):

        if not isinstance(child, ast.Call):
            continue

        called_function = None

        if isinstance(
            child.func,
            ast.Name
        ):
            called_function = child.func.id

        elif isinstance(
            child.func,
            ast.Attribute
        ):
            called_function = child.func.attr

        if not called_function:
            continue

        assigned_to = None

        parent_assignments = []

        # Search the function body for an assignment
        # containing this exact Call node.
        for parent in ast.walk(node):

            if not isinstance(
                parent,
                (
                    ast.Assign,
                    ast.AnnAssign
                )
            ):
                continue

            value = getattr(
                parent,
                "value",
                None
            )

            if value is not child:
                continue

            targets = getattr(
                parent,
                "targets",
                []
            )

            for target in targets:

                if isinstance(
                    target,
                    ast.Name
                ):
                    assigned_to = target.id

            if isinstance(
                parent,
                ast.AnnAssign
            ):

                target = getattr(
                    parent,
                    "target",
                    None
                )

                if isinstance(
                    target,
                    ast.Name
                ):
                    assigned_to = target.id

        calls.append(
            {
                "function": called_function,
                "assigned_to": assigned_to,
                "line": getattr(
                    child,
                    "lineno",
                    None
                )
            }
        )

    return calls


def parse_python_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        source_code = file.read()

    tree = ast.parse(
        source_code
    )

    imports = []
    functions = []
    classes = []

    # ---------------------------------------------------------
    # Imports
    # ---------------------------------------------------------

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.Import
        ):

            for name in node.names:

                imports.append(
                    name.name
                )

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            if node.module:

                imports.append(
                    node.module
                )

    # ---------------------------------------------------------
    # Functions
    # ---------------------------------------------------------

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):

            functions.append(
                node.name
            )

    # ---------------------------------------------------------
    # Classes
    # ---------------------------------------------------------

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.ClassDef
        ):

            classes.append(
                node.name
            )

    # ---------------------------------------------------------
    # Function details
    # ---------------------------------------------------------

    function_details = []

    for node in ast.walk(tree):

        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):
            continue

        function_details.append(
            {
                "name": node.name,

                "line_start": node.lineno,

                "line_end": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),

                "calls": get_called_names(
                    node
                ),

                "call_details": get_function_call_details(
                    node
                )
            }
        )

    # ---------------------------------------------------------
    # Class details
    # ---------------------------------------------------------

    class_details = []

    for node in ast.walk(tree):

        if not isinstance(
            node,
            ast.ClassDef
        ):
            continue

        class_details.append(
            {
                "name": node.name,

                "line_start": node.lineno,

                "line_end": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),

                "methods": [
                    child.name
                    for child in node.body
                    if isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef
                        )
                    )
                ]
            }
        )

    return {
        "file": file_path,

        "imports": sorted(
            set(imports)
        ),

        "functions": sorted(
            set(functions)
        ),

        "classes": sorted(
            set(classes)
        ),

        "function_details": function_details,

        "class_details": class_details
    }