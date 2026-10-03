from git_history import get_git_history


repo_path = "data/repos/requests_git_project"

file_path = "src/requests/utils.py"

history = get_git_history(
    repo_path,
    file_path
)


print("\n=== ProjectTwin Git History ===")
print("File:", file_path)
print("\nHistory:")
print(history)