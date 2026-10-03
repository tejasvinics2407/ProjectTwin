import ast

from backend.project_model import (
    ProjectFile,
    Symbol
)


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
    Capture information about function calls.

    Example:

        skill_gap = analyze_skill_gap(...)

    becomes:

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

    # =========================================================
    # IMPORTS
    # =========================================================

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

    # =========================================================
    # FUNCTIONS
    # =========================================================

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

    # =========================================================
    # CLASSES
    # =========================================================

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.ClassDef
        ):

            classes.append(
                node.name
            )

    # =========================================================
    # FUNCTION DETAILS
    # =========================================================

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

    # =========================================================
    # CLASS DETAILS
    # =========================================================

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

    # =========================================================
    # EXISTING PROJECTTWIN FORMAT
    # =========================================================

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


def parse_python_file_to_model(
    file_path,
    project_relative_path=None
):
    """
    Convert a Python source file into the
    language-independent ProjectTwin model.

    The existing parse_python_file() function
    remains unchanged in purpose so that the
    current dependency and impact system keeps
    working.

    This function creates:

        ProjectFile
            +
        Symbol objects
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        source_code = file.read()

    tree = ast.parse(
        source_code
    )

    if project_relative_path:

        project_path = project_relative_path

    else:

        project_path = file_path

    project_file = ProjectFile(
        path=str(
            project_path
        ).replace(
            "\\",
            "/"
        ),

        language="python"
    )

    # =========================================================
    # IMPORTS
    # =========================================================

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.Import
        ):

            for name in node.names:

                project_file.imports.append(
                    name.name
                )

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            if node.module:

                project_file.imports.append(
                    node.module
                )

    project_file.imports = sorted(
        set(
            project_file.imports
        )
    )

    # =========================================================
    # FUNCTIONS
    # =========================================================

    for node in ast.walk(tree):

        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):
            continue

        symbol = Symbol(
            name=node.name,

            symbol_type="function",

            file=project_file.path,

            language="python",

            line_start=node.lineno,

            line_end=getattr(
                node,
                "end_lineno",
                node.lineno
            ),

            calls=get_called_names(
                node
            ),

            imports=[]
        )

        project_file.symbols.append(
            symbol
        )

    # =========================================================
    # CLASSES
    # =========================================================

    for node in ast.walk(tree):

        if not isinstance(
            node,
            ast.ClassDef
        ):
            continue

        class_symbol = Symbol(
            name=node.name,

            symbol_type="class",

            file=project_file.path,

            language="python",

            line_start=node.lineno,

            line_end=getattr(
                node,
                "end_lineno",
                node.lineno
            ),

            calls=get_called_names(
                node
            ),

            imports=[]
        )

        project_file.symbols.append(
            class_symbol
        )

        # -----------------------------------------------------
        # Class methods
        # -----------------------------------------------------

        for child in node.body:

            if not isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef
                )
            ):
                continue

            method_symbol = Symbol(
                name=child.name,

                symbol_type="method",

                file=project_file.path,

                language="python",

                line_start=child.lineno,

                line_end=getattr(
                    child,
                    "end_lineno",
                    child.lineno
                ),

                parent=node.name,

                calls=get_called_names(
                    child
                ),

                imports=[]
            )

            project_file.symbols.append(
                method_symbol
            )

    return project_file