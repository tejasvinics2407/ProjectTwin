from code_parser import parse_python_file


print("=== ProjectTwin Code Parser ===")

file_path = "backend/sample_project.py"

result = parse_python_file(file_path)

print(f"File: {result['file']}")

print("\nImports:")
for item in result["imports"]:
    print(f"- {item}")

print("\nFunctions:")
for item in result["functions"]:
    print(f"- {item}")

print("\nClasses:")
for item in result["classes"]:
    print(f"- {item}")

print("\nFunction Details:")

for function in result["function_details"]:

    print(f"\n- {function['name']}")

    print(
        f"  Lines: "
        f"{function['line_start']}"
        f"-"
        f"{function['line_end']}"
    )

    print("  Calls:")

    if function["calls"]:

        for call in function["calls"]:
            print(f"    - {call}")

    else:

        print("    - None")

print("\nClass Details:")

for class_info in result["class_details"]:

    print(f"\n- {class_info['name']}")

    print(
        f"  Lines: "
        f"{class_info['line_start']}"
        f"-"
        f"{class_info['line_end']}"
    )

    print("  Methods:")

    if class_info["methods"]:

        for method in class_info["methods"]:
            print(f"    - {method}")

    else:

        print("    - None")