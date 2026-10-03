import re

from backend.project_model import (
    ProjectFile,
    Symbol
)


# =========================================================
# IMPORT DETECTION
# =========================================================

IMPORT_PATTERN = re.compile(
    r'^\s*import\s+(?:static\s+)?'
    r'([A-Za-z_][\w.]*)\s*;',
    re.MULTILINE
)


def extract_imports(source_code):
    """
    Extract Java import statements.
    """

    return sorted(
        set(
            IMPORT_PATTERN.findall(
                source_code
            )
        )
    )


# =========================================================
# CLASS DETECTION
# =========================================================

CLASS_PATTERN = re.compile(
    r'\b(?:public\s+|private\s+|protected\s+|abstract\s+|final\s+)*'
    r'class\s+([A-Za-z_][\w]*)'
)


def extract_classes(source_code):
    """
    Extract Java class names.
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
    r'^\s*'
    r'(?:public|private|protected|static|final|abstract|synchronized|native|'
    r'strictfp|\s)*'
    r'(?:<[^>]+>\s+)?'
    r'(?:[\w<>\[\], ?]+)\s+'
    r'([A-Za-z_][\w]*)'
    r'\s*\([^;{}]*\)'
    r'\s*(?:throws\s+[^{]+)?'
    r'\s*\{',
    re.MULTILINE
)


def extract_methods(source_code):
    """
    Extract common Java method declarations.

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
            (
                name,
                match.start()
            )
        )

    return methods


# =========================================================
# METHOD CALL DETECTION
# =========================================================

CALL_PATTERN = re.compile(
    r'\b([A-Za-z_][\w]*)\s*\('
)


def extract_calls(source_code):
    """
    Extract simple Java method-call names.

    This is intentionally lightweight for the
    first multi-language implementation.
    """

    calls = []

    ignored = {
        "if",
        "for",
        "while",
        "switch",
        "catch",
        "return",
        "new",
        "class",
        "super",
        "this",
        "try",
        "synchronized"
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

def parse_java_file(
    file_path,
    project_relative_path=None
):
    """
    Parse a Java source file into the
    language-independent ProjectTwin model.
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

    project_file = ProjectFile(
        path=project_path,

        language="java"
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

            language="java",

            line_start=line_start,

            line_end=line_start,

            calls=[],

            imports=[]
        )

        project_file.symbols.append(
            class_symbol
        )

    # =====================================================
    # METHODS
    # =====================================================

    methods = extract_methods(
        source_code
    )

    calls = extract_calls(
        source_code
    )

    for method_name, position in methods:

        line_start = (
            get_line_number(
                source_code,
                position
            )
        )

        method_symbol = Symbol(
            name=method_name,

            symbol_type="method",

            file=project_path,

            language="java",

            line_start=line_start,

            line_end=line_start,

            calls=calls,

            imports=[]
        )

        project_file.symbols.append(
            method_symbol
        )

    return project_file