from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Symbol:
    """
    A language-independent representation of a code symbol.

    A symbol can represent:
    - a function
    - a method
    - a class
    - a variable
    """

    name: str

    symbol_type: str

    file: str

    language: str

    line_start: Optional[int] = None

    line_end: Optional[int] = None

    parent: Optional[str] = None

    calls: List[str] = field(
        default_factory=list
    )

    imports: List[str] = field(
        default_factory=list
    )


@dataclass
class ProjectFile:
    """
    Language-independent representation of a project file.
    """

    path: str

    language: str

    imports: List[str] = field(
        default_factory=list
    )

    symbols: List[Symbol] = field(
        default_factory=list
    )


@dataclass
class ProjectModel:
    """
    Common representation of an entire software project.

    Language-specific parsers will eventually convert
    Python, JavaScript, TypeScript, Java, C++, etc.
    into this common model.
    """

    files: List[ProjectFile] = field(
        default_factory=list
    )

    def add_file(
        self,
        project_file: ProjectFile
    ):
        """
        Add a file to the project model.
        """

        self.files.append(
            project_file
        )

    def get_file(
        self,
        path: str
    ) -> Optional[ProjectFile]:
        """
        Find a project file by its path.
        """

        for project_file in self.files:

            if project_file.path == path:
                return project_file

        return None

    def get_all_symbols(self) -> List[Symbol]:
        """
        Return every symbol in the project.
        """

        symbols = []

        for project_file in self.files:

            symbols.extend(
                project_file.symbols
            )

        return symbols

    def get_symbol(
        self,
        file_path: str,
        symbol_name: str
    ) -> Optional[Symbol]:
        """
        Find a specific symbol in a specific file.
        """

        project_file = self.get_file(
            file_path
        )

        if project_file is None:
            return None

        for symbol in project_file.symbols:

            if symbol.name == symbol_name:
                return symbol

        return None

    def summary(self):
        """
        Return a simple summary of the project model.
        """

        return {
            "file_count": len(
                self.files
            ),

            "symbol_count": len(
                self.get_all_symbols()
            ),

            "languages": sorted(
                set(
                    project_file.language
                    for project_file in self.files
                )
            )
        }