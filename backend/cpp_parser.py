import re

from backend.project_model import (
    ProjectFile,
    Symbol
)


# =========================================================
# IMPORT / INCLUDE DETECTION
# =========================================================

INCLUDE_PATTERN = re.compile(
    r'^\s*#include\s*[<"]([^>"]+)[>"]',
    re.MULTILINE
)


def extract_includes(source_code):
    """
    Extract C/C++ #include dependencies.
    """

    return sorted(
        set(
            INCLUDE_PATTERN.findall(
                source_code
            )
        )
    )


# =========================================================
# CLASS / STRUCT DETECTION
# =========================================================

CLASS_PATTERN = re.compile(
    r'\b(?:class|struct)\s+'
    r'([A-Za-z_][\w]*)'
)


def extract_classes(source_code):
    """
    Extract C/C++ class and struct names.
    """

    return sorted(
        set(
            CLASS_PATTERN.findall(
                source_code
            )
        )
    )


# =========================================================
# FUNCTION DETECTION
# =========================================================

FUNCTION_PATTERN = re.compile(
    r'^\s*'
    r'(?:static\s+|inline\s+|virtual\s+|extern\s+|'
    r'const\s+|unsigned\s+|signed\s+|long\s+|short\s+)*'
    r'(?:[\w:*&<>,~]+\s+)+'
    r'([A-Za-z_~][\w]*)'
    r'\s*\([^;{}]*\)'
    r'\s*(?:const\s*)?'
    r'(?:\{|;)',
    re.MULTILINE
)


def extract_functions(source_code):
    """
    Extract common C/C++ function declarations
    and definitions.

    This is a lightweight first implementation.
    """

    functions = []

    ignored = {
        "if",
        "for",
        "while",
        "switch",
        "catch"
    }

    for match in FUNCTION_PATTERN.finditer(
        source_code
    ):

        name = match.group(
            1
        )

        if name in ignored:
            continue

        functions.append(
            (
                name,
                match.start()
            )
        )

    return functions


# =========================================================
# FUNCTION CALL DETECTION
# =========================================================

CALL_PATTERN = re.compile(
    r'\b([A-Za-z_][\w]*)\s*\('
)


def extract_calls(source_code):
    """
    Extract simple C/C++ function-call names.
    """

    calls = []

    ignored = {
        "if",
        "for",
        "while",
        "switch",
        "catch",
        "sizeof",
        "return",
        "class",
        "struct",
        "main"
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
    Convert a character position into
    a source-code line number.
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

def parse_cpp_file(
    file_path,
    project_relative_path=None
):
    """
    Parse a C, C++, or header file into
    the language-independent ProjectTwin model.
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

    lower_path = file_path.lower()

    if lower_path.endswith(
        (".cpp", ".cc", ".cxx", ".hpp")
    ):

        language = "cpp"

    else:

        language = "c"

    project_file = ProjectFile(
        path=project_path,
        language=language
    )

    # =====================================================
    # INCLUDES
    # =====================================================

    project_file.imports = (
        extract_includes(
            source_code
        )
    )

    # =====================================================
    # CLASSES / STRUCTS
    # =====================================================

    class_names = (
        extract_classes(
            source_code
        )
    )

    for class_name in class_names:

        pattern = re.compile(
            r'\b(?:class|struct)\s+'
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
    # FUNCTIONS
    # =====================================================

    functions = extract_functions(
        source_code
    )

    calls = extract_calls(
        source_code
    )

    for function_name, position in functions:

        line_start = (
            get_line_number(
                source_code,
                position
            )
        )

        function_symbol = Symbol(
            name=function_name,
            symbol_type="function",
            file=project_path,
            language=language,
            line_start=line_start,
            line_end=line_start,
            calls=calls,
            imports=[]
        )

        project_file.symbols.append(
            function_symbol
        )

    return project_file