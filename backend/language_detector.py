from pathlib import Path


LANGUAGE_EXTENSIONS = {
    ".py": "python",

    ".js": "javascript",
    ".jsx": "javascript",

    ".ts": "typescript",
    ".tsx": "typescript",

    ".java": "java",

    ".c": "c",

    ".h": "c",

    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",

    ".hpp": "cpp",
}


def detect_language(file_path):
    """
    Detect the programming language from a file extension.

    Returns:
        language name as a string
        or 'unknown' when the extension is not supported.
    """

    extension = Path(
        file_path
    ).suffix.lower()

    return LANGUAGE_EXTENSIONS.get(
        extension,
        "unknown"
    )


def is_supported_language(file_path):
    """
    Check whether ProjectTwin currently recognizes
    the programming language of a file.
    """

    return detect_language(
        file_path
    ) != "unknown"


def get_supported_extensions():
    """
    Return all file extensions currently recognized
    by ProjectTwin.
    """

    return sorted(
        LANGUAGE_EXTENSIONS.keys()
    )