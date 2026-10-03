import re

from backend.project_model import (
    ProjectFile,
    Symbol
)


# =========================================================
# IMPORT DETECTION
# =========================================================

IMPORT_PATTERNS = [
    re.compile(
        r'import\s+(?:[\s\S]*?\s+from\s+)?["\']([^"\']+)["\']'
    ),

    re.compile(
        r'import\s+["\']([^"\']+)["\']'
    ),

    re.compile(
        r'require\s*\(\s*["\']([^"\']+)["\']\s*\)'
    )
]


def extract_imports(source_code):
    """
    Extract ES module imports and CommonJS requires.
    """

    imports = []

    for pattern in IMPORT_PATTERNS:

        matches = pattern.findall(
            source_code
        )

        imports.extend(
            matches
        )

    return sorted(
        set(imports)
    )


# =========================================================
# FUNCTION DETECTION
# =========================================================

FUNCTION_PATTERNS = [
    re.compile(
        r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\('
    ),

    re.compile(
        r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)'
        r'\s*=\s*(?:async\s*)?\([^)]*\)\s*=>'
    ),

    re.compile(
        r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)'
        r'\s*=\s*(?:async\s*)?[A-Za-z_$][\w$]*\s*=>'
    )
]


def extract_functions(source_code):
    """
    Extract common JavaScript/TypeScript function forms.

    This is intentionally lightweight for the first
    multi-language version.
    """

    functions = []

    for pattern in FUNCTION_PATTERNS:

        matches = pattern.findall(
            source_code
        )

        functions.extend(
            matches
        )

    return sorted(
        set(functions)
    )


# =========================================================
# CLASS DETECTION
# =========================================================

CLASS_PATTERN = re.compile(
    r'\bclass\s+([A-Za-z_$][\w$]*)'
)


def extract_classes(source_code):
    """
    Extract JavaScript/TypeScript class names.
    """

    return sorted(
        set(
            CLASS_PATTERN.findall(
                source_code
            )
        )
    )


# =========================================================
# METHOD DETECTION
# =========================================================

METHOD_PATTERN = re.compile(
    r'^\s*(?:async\s+)?'
    r'([A-Za-z_$][\w$]*)\s*'
    r'\([^)]*\)\s*\{',
    re.MULTILINE
)


def extract_methods(source_code):
    """
    Extract common class/object method declarations.

    This is a lightweight first implementation.
    """

    methods = []

    for match in METHOD_PATTERN.finditer(
        source_code
    ):

        name = match.group(
            1
        )

        if name in {
            "if",
            "for",
            "while",
            "switch",
            "catch"
        }:
            continue

        methods.append(
            name
        )

    return sorted(
        set(methods)
    )


# =========================================================
# FUNCTION CALL DETECTION
# =========================================================

CALL_PATTERN = re.compile(
    r'\b([A-Za-z_$][\w$]*)\s*\('
)


def extract_calls(source_code):
    """
    Extract simple function-call names.

    This is not a full JavaScript semantic parser.
    It provides initial relationship information that
    will later be improved with a proper parser.
    """

    calls = []

    ignored = {
        "if",
        "for",
        "while",
        "switch",
        "catch",
        "function",
        "return",
        "typeof",
        "console"
    }

    for match in CALL_PATTERN.finditer(
        source_code
    ):

        name = match.group(
            1
        )

        if name in ignored:
            continue

        calls.append(
            name
        )

    return sorted(
        set(calls)
    )


# =========================================================
# LINE NUMBER
# =========================================================

def get_line_number(
    source_code,
    position
):
    """
    Convert a character position into a line number.
    """

    return (
        source_code.count(
            "\n",
            0,
            position
        )
        + 1
    )


# =========================================================
# PARSER
# =========================================================

def parse_javascript_file(
    file_path,
    project_relative_path=None
):
    """
    Parse a JavaScript or TypeScript file into
    the language-independent ProjectTwin model.

    Supported:

    .js
    .jsx
    .ts
    .tsx
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        source_code = file.read()

    if project_relative_path:

        project_path = str(
            project_relative_path
        ).replace(
            "\\",
            "/"
        )

    else:

        project_path = str(
            file_path
        ).replace(
            "\\",
            "/"
        )

    extension = (
        file_path.lower()
    )

    if extension.endswith(
        (".ts", ".tsx")
    ):

        language = "typescript"

    else:

        language = "javascript"

    project_file = ProjectFile(
        path=project_path,

        language=language
    )

    # =====================================================
    # IMPORTS
    # =====================================================

    project_file.imports = (
        extract_imports(
            source_code
        )
    )

    # =====================================================
    # FUNCTIONS
    # =====================================================

    function_names = (
        extract_functions(
            source_code
        )
    )

    for function_name in function_names:

        pattern = re.compile(
            r'\b'
            + re.escape(
                function_name
            )
            + r'\b'
        )

        match = pattern.search(
            source_code
        )

        line_start = None

        if match:

            line_start = (
                get_line_number(
                    source_code,
                    match.start()
                )
            )

        symbol = Symbol(
            name=function_name,

            symbol_type="function",

            file=project_path,

            language=language,

            line_start=line_start,

            line_end=line_start,

            calls=[],

            imports=[]
        )

        project_file.symbols.append(
            symbol
        )

    # =====================================================
    # CLASSES
    # =====================================================

    class_names = (
        extract_classes(
            source_code
        )
    )

    for class_name in class_names:

        pattern = re.compile(
            r'\bclass\s+'
            + re.escape(
                class_name
            )
        )

        match = pattern.search(
            source_code
        )

        line_start = None

        if match:

            line_start = (
                get_line_number(
                    source_code,
                    match.start()
                )
            )

        class_symbol = Symbol(
            name=class_name,

            symbol_type="class",

            file=project_path,

            language=language,

            line_start=line_start,

            line_end=line_start,

            calls=[],

            imports=[]
        )

        project_file.symbols.append(
            class_symbol
        )

    # =====================================================
    # CALL INFORMATION
    # =====================================================

    calls = extract_calls(
        source_code
    )

    for symbol in project_file.symbols:

        if symbol.symbol_type == "function":

            symbol.calls = calls

    return project_file