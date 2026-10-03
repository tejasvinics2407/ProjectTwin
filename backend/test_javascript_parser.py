from backend.javascript_parser import (
    parse_javascript_file
)


TEST_FILE = "backend/sample_test.js"


SOURCE = """
import React from "react";
import { analyze } from "./analyzer";

function analyzeProject(data) {
    return analyze(data);
}

const calculateScore = (value) => {
    return value * 2;
};

class ProjectManager {
    start() {
        analyzeProject({});
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


project_file = parse_javascript_file(
    TEST_FILE,
    "sample_test.js"
)


print(
    "=== JavaScript Parser Test ==="
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