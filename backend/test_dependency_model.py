from backend.dependency_model import (
    Dependency,
    DependencyModel
)


model = DependencyModel()


dependency = Dependency(
    source_file="backend/main.py",
    source_symbol="analyze_resume",
    target_file="backend/engine/skill_gap_analyzer.py",
    target_symbol="analyze_skill_gap",
    relationship_type="calls",
    evidence="Function call detected"
)


model.add_dependency(dependency)


print("=== Dependency Model Test ===")

print(
    "Dependency count:",
    model.summary()["dependency_count"]
)


print("\nAll dependencies:")

for item in model.get_all():

    print(
        f"  {item.source_file}:"
        f"{item.source_symbol}()"
        f" ---> "
        f"{item.target_file}:"
        f"{item.target_symbol}()"
    )


print("\nDependencies FROM main.py:")

for item in model.get_dependencies_from(
    "backend/main.py"
):

    print(
        f"  {item.source_symbol}"
        f"() ---> "
        f"{item.target_symbol}()"
    )


print("\nDependencies TO skill_gap_analyzer.py:")

for item in model.get_dependencies_to(
    "backend/engine/skill_gap_analyzer.py"
):

    print(
        f"  {item.source_symbol}"
        f"() ---> "
        f"{item.target_symbol}()"
    )


print("\nTEST PASSED")