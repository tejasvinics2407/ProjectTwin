from backend.project_model import (
    ProjectModel,
    ProjectFile,
    Symbol
)

from backend.dependency_extractor import (
    build_dependency_model
)


project = ProjectModel()


main_file = ProjectFile(
    path="backend/main.py",
    language="python",
    imports=["backend.engine.skill_gap_analyzer"]
)

main_file.symbols.append(
    Symbol(
        name="analyze_resume",
        symbol_type="function",
        file="backend/main.py",
        language="python",
        calls=["analyze_skill_gap"]
    )
)


skill_file = ProjectFile(
    path="backend/engine/skill_gap_analyzer.py",
    language="python"
)

skill_file.symbols.append(
    Symbol(
        name="analyze_skill_gap",
        symbol_type="function",
        file="backend/engine/skill_gap_analyzer.py",
        language="python"
    )
)


project.add_file(main_file)
project.add_file(skill_file)


dependency_model = build_dependency_model(
    project
)


print("=== Dependency Extractor Test ===")

print(
    "Dependency count:",
    dependency_model.summary()["dependency_count"]
)


for dependency in dependency_model.get_all():

    print(
        f"{dependency.source_file}:"
        f"{dependency.source_symbol}"
        f" ---> "
        f"{dependency.target_file}:"
        f"{dependency.target_symbol}"
        f" [{dependency.relationship_type}]"
    )


print("\nTEST PASSED")