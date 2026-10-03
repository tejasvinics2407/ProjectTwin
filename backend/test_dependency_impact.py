from backend.project_model import (
    ProjectModel,
    ProjectFile,
    Symbol
)

from backend.dependency_extractor import (
    build_dependency_model
)

from backend.dependency_impact import (
    analyze_dependency_impact
)


project = ProjectModel()


# --------------------------------------------------
# File A
# --------------------------------------------------

main_file = ProjectFile(
    path="main.py",
    language="python"
)

main_file.symbols.append(
    Symbol(
        name="main_function",
        symbol_type="function",
        file="main.py",
        language="python",
        calls=["calculate"]
    )
)


# --------------------------------------------------
# File B
# --------------------------------------------------

calculator_file = ProjectFile(
    path="calculator.py",
    language="python"
)

calculator_file.symbols.append(
    Symbol(
        name="calculate",
        symbol_type="function",
        file="calculator.py",
        language="python"
    )
)


# --------------------------------------------------
# File C
# --------------------------------------------------

report_file = ProjectFile(
    path="report.py",
    language="python"
)

report_file.symbols.append(
    Symbol(
        name="generate_report",
        symbol_type="function",
        file="report.py",
        language="python",
        calls=["main_function"]
    )
)


project.add_file(
    main_file
)

project.add_file(
    calculator_file
)

project.add_file(
    report_file
)


# --------------------------------------------------
# Build dependencies
# --------------------------------------------------

dependency_model = build_dependency_model(
    project
)


print(
    "=== Dependency Impact Test ==="
)


print(
    "Total dependencies:",
    dependency_model.summary()[
        "dependency_count"
    ]
)


# --------------------------------------------------
# Analyze change
# --------------------------------------------------

result = analyze_dependency_impact(
    dependency_model,
    changed_file="calculator.py",
    changed_symbol="calculate"
)


print(
    "\nChanged:"
)

print(
    f"  {result['changed_file']}:"
    f"{result['changed_symbol']}()"
)


print(
    "\nDirect impact:"
)

for item in result[
    "direct_impact"
]:

    print(
        f"  {item['source_file']}:"
        f"{item['source_symbol']}()"
        f" ---> "
        f"{item['target_file']}:"
        f"{item['target_symbol']}()"
    )


print(
    "\nIndirect impact:"
)

for file in result[
    "indirect_impact"
]:

    print(
        f"  {file}"
    )


print(
    "\nAffected files:"
)

for file in result[
    "affected_files"
]:

    print(
        f"  - {file}"
    )


print(
    "\nImpact count:",
    result["impact_count"]
)


print(
    "\nTEST PASSED"
)