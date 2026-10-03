from pathlib import Path
from backend.impact_analyzer import find_impact
from backend.git_history import get_git_history


def generate_impact_report(graph, repo_path, changed_file):

    # Step 1: Find affected files using the dependency graph
    impact = find_impact(
        graph,
        changed_file
    )

    # Step 2: Convert the full project path
    # into a Git-relative file path
    repo_path = Path(repo_path)
    changed_path = Path(changed_file)

    try:
        git_file_path = changed_path.relative_to(repo_path)
        git_file_path = git_file_path.as_posix()

    except ValueError:
        git_file_path = changed_file

    # Debug information
    print("\nDEBUG Git path:")
    print("Repository:", repo_path)
    print("File:", git_file_path)

    # Step 3: Get Git history
    history = get_git_history(
        str(repo_path),
        git_file_path
    )

    # Step 4: Create the complete impact report
    report = {
        "changed_file": changed_file,
        "git_file_path": git_file_path,
        "impact_count": impact["impact_count"],
        "affected_files": impact["affected_files"],
        "git_history": history
    }

    return report