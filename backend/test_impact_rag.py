from impact_rag import build_impact_prompt


# Example impact report
report = {
    "changed_file": "src/requests/utils.py",

    "impact_count": 3,

    "affected_files": [
        "src/requests/api.py",
        "src/requests/models.py",
        "tests/test_utils.py"
    ],

    "git_history": """
47914226 | 2026-02-12 | Nate Prewitt | Fix empty netrc entry usage (#7205)
f8bec2f7 | 2026-01-30 | Nate Prewitt | Fix CI and build failures (#7190)
5b4b64c3 | 2025-06-05 | Arthur Woimbée | Add more tests to prevent regression of CVE 2024 47081
"""
}


prompt = build_impact_prompt(report)


print("\n=== ProjectTwin Impact RAG ===")
print(prompt)