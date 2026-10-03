from backend.parser_manager import (
    parser_status,
    can_parse_file
)


test_files = [
    "main.py",
    "app.js",
    "server.ts",
    "Main.java",
    "program.cpp"
]


print(
    "=== Parser Manager Test ==="
)


for file in test_files:

    status = parser_status(
        file
    )

    print(
        f"\nFile: "
        f"{status['file']}"
    )

    print(
        f"Language: "
        f"{status['language']}"
    )

    print(
        f"Parser available: "
        f"{status['parser_available']}"
    )

    print(
        f"can_parse_file(): "
        f"{can_parse_file(file)}"
    )


print(
    "\nTEST PASSED"
)