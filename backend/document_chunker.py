import json


def create_chunks(knowledge_base_file):
    with open(knowledge_base_file, "r", encoding="utf-8") as file:
        knowledge_base = json.load(file)

    chunks = []

    for item in knowledge_base:
        file_name = item["file"]

        chunk = {
            "file": file_name,
            "content": {
                "imports": item["imports"],
                "functions": item["functions"],
                "classes": item["classes"]
            }
        }

        chunks.append(chunk)

    return chunks