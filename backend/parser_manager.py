from pathlib import Path

from backend.language_detector import (
    detect_language
)

from backend.code_parser import (
    parse_python_file_to_model
)

from backend.javascript_parser import (
    parse_javascript_file
)

from backend.java_parser import (
    parse_java_file
)

from backend.cpp_parser import (
    parse_cpp_file
)


def parse_file(
    file_path,
    project_relative_path=None
):
    """
    Select the correct parser based on language.
    """

    language = detect_language(
        file_path
    )

    if language == "python":

        return parse_python_file_to_model(
            file_path,
            project_relative_path
        )

    if language == "javascript":

        return parse_javascript_file(
            file_path,
            project_relative_path
        )

    if language == "typescript":

        return parse_javascript_file(
            file_path,
            project_relative_path
        )

    if language == "java":

        return parse_java_file(
            file_path,
            project_relative_path
        )

    if language in {
        "c",
        "cpp"
    }:

        return parse_cpp_file(
            file_path,
            project_relative_path
        )

    return None


def can_parse_file(file_path):
    """
    Check whether ProjectTwin currently has
    a parser for the file.
    """

    language = detect_language(
        file_path
    )

    return language in {
        "python",
        "javascript",
        "typescript",
        "java",
        "c",
        "cpp"
    }


def parser_status(file_path):
    """
    Return parser support information.
    """

    language = detect_language(
        file_path
    )

    supported_languages = {
        "python",
        "javascript",
        "typescript",
        "java",
        "c",
        "cpp"
    }

    return {
        "file": str(
            Path(file_path)
        ),

        "language": language,

        "parser_available": (
            language
            in supported_languages
        )
    }