from pathlib import Path

# Folders that should not be analyzed as project source files.
IGNORED_DIRS = {
    ".venv",
    ".git",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
}

def scan_project(project_path):
    """
    Recursively scan a project directory and return its file paths.

    This is the first small building block of ProjectTwin:
    before we can understand a project, we need to discover what
    files exist inside it.
    """
    root = Path(project_path)
    found_files = []

    if not root.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_path}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        # Ignore files inside folders such as .venv and .git.
        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        found_files.append(path.relative_to(root).as_posix())

    return sorted(found_files)
