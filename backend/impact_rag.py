def build_impact_prompt(report):

    affected_files = "\n".join(
        f"- {file}"
        for file in report["affected_files"]
    )

    prompt = f"""
You are ProjectTwin, an AI-powered Digital Twin for software projects.

Analyze the proposed change using the project evidence below.

CHANGED FILE:
{report["changed_file"]}

NUMBER OF AFFECTED FILES:
{report["impact_count"]}

AFFECTED FILES:
{affected_files}

GIT HISTORY OF CHANGED FILE:
{report["git_history"]}

Explain:

1. What parts of the project may be affected?
2. Why are these files affected?
3. What does the Git history tell us about the changed file?
4. Which tests may need attention?
5. What should a developer check before making the change?

Use only the evidence provided above.
Clearly distinguish facts from reasonable inferences.
"""

    return prompt