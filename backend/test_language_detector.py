from backend.language_detector import (
    detect_language,
    is_supported_language
)


test_files = [
    "main.py",
    "app.js",
    "component.jsx",
    "server.ts",
    "component.tsx",
    "Main.java",
    "program.c",
    "header.h",
    "engine.cpp",
    "engine.hpp",
    "README.md"
]


print("=== Language Detection Test ===")


for file in test_files:

    language = detect_language(
        file
    )

    supported = is_supported_language(
        file
    )

    print(
        f"{file:20} "
        f"-> {language:12} "
        f"supported={supported}"
    )