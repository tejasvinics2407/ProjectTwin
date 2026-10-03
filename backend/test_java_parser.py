from backend.java_parser import (
    parse_java_file
)


TEST_FILE = "backend/SampleProject.java"


SOURCE = """
package example;

import java.util.List;

public class ProjectManager {

    public void start() {
        analyzeProject();
    }

    private void analyzeProject() {
        System.out.println("Analyzing project");
    }
}
"""


with open(
    TEST_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        SOURCE
    )


project_file = parse_java_file(
    TEST_FILE,
    "SampleProject.java"
)


print(
    "=== Java Parser Test ==="
)

print(
    "Language:",
    project_file.language
)

print(
    "Imports:",
    project_file.imports
)

print(
    "Symbols:"
)

for symbol in project_file.symbols:

    print(
        f"  - "
        f"{symbol.symbol_type}: "
        f"{symbol.name}"
    )

print(
    "\nTEST PASSED"
)