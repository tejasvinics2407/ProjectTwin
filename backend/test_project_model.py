from backend.project_model import (
    ProjectModel,
    ProjectFile,
    Symbol
)


project = ProjectModel()


file = ProjectFile(
    path="backend/example.py",
    language="python"
)


symbol = Symbol(
    name="hello",
    symbol_type="function",
    file="backend/example.py",
    language="python",
    line_start=1,
    line_end=3
)


file.symbols.append(symbol)

project.add_file(file)


print("=== Project Model Test ===")

print(
    "Summary:",
    project.summary()
)

print(
    "Symbol:",
    project.get_symbol(
        "backend/example.py",
        "hello"
    )
)