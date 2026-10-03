import subprocess


def get_git_history(repo_path, file_path=None):

    command = [
        "git",
        "-C",
        repo_path,
        "log",
        "--oneline",
        "--date=short",
        "--pretty=format:%h | %ad | %an | %s"
    ]

    if file_path:
        command.append("--")
        command.append(file_path)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True
    )

    return result.stdout