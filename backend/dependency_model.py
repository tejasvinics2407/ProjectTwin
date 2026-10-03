from dataclasses import dataclass
from typing import Optional


@dataclass
class Dependency:
    """
    Represents a relationship between two parts
    of a software project.
    """

    source_file: str
    source_symbol: Optional[str]

    target_file: str
    target_symbol: Optional[str]

    relationship_type: str

    evidence: Optional[str] = None


class DependencyModel:
    """
    Stores language-independent dependency relationships.
    """

    def __init__(self):
        self.dependencies = []

    def add_dependency(self, dependency: Dependency):
        """
        Add a dependency if it does not already exist.
        """

        if dependency not in self.dependencies:
            self.dependencies.append(dependency)

    def get_all(self):
        """
        Return all dependencies.
        """

        return self.dependencies

    def get_dependencies_from(self, source_file):
        """
        Return dependencies originating from a file.
        """

        return [
            dependency
            for dependency in self.dependencies
            if dependency.source_file == source_file
        ]

    def get_dependencies_to(self, target_file):
        """
        Return dependencies pointing to a file.
        """

        return [
            dependency
            for dependency in self.dependencies
            if dependency.target_file == target_file
        ]

    def summary(self):
        """
        Return a small summary of the dependency model.
        """

        return {
            "dependency_count": len(self.dependencies)
        }