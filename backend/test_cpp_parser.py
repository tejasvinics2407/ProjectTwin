from backend.cpp_parser import (
    parse_cpp_file
)


TEST_FILE = "backend/SampleProject.cpp"


SOURCE = """
#include <iostream>
#include "project.h"

class ProjectManager {

public:

    void start() {
        analyzeProject();
    }

    void analyzeProject() {
        std::cout << "Analyzing project";
    }
};

int main() {

    ProjectManager manager;

    manager.start();

    return 0;
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


project_file = parse_cpp_file(
    TEST_FILE,
    "SampleProject.cpp"
)


print(
    "=== C++ Parser Test ==="
)

print(
    "Language:",
    project_file.language
)

print(
    "Includes:",
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