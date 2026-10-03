import json
from pathlib import Path


def save_knowledge_base(parsed_files, output_file):
    output_path = Path(output_file)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(parsed_files, file, indent=4)

    print(f"Knowledge base saved to: {output_path}")