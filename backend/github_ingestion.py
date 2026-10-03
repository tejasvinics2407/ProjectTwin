import subprocess
from pathlib import Path
from urllib.parse import urlparse


def get_repository_name(repo_url):
    """
    Extract the repository name from a GitHub URL.
    Example:
    https://github.com/user/project.git
    -> project
    """

    parsed_url = urlparse(repo_url)

    repository_name = parsed_url.path.rstrip("/").split("/")[-1]

    if repository_name.endswith(".git"):
        repository_name = repository_name[:-4]

    return repository_name


def get_existing_remote(destination):
    """
    Check which GitHub repository an existing local clone belongs to.
    """

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(destination),
                "remote",
                "get-url",
                "origin"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception:
        pass

    return None


def normalize_repo_url(repo_url):
    """
    Normalize GitHub URLs so equivalent URLs can be compared.
    """

    return repo_url.rstrip("/").removesuffix(".git").lower()


def clone_repository(repo_url, destination):
    """
    Clone a GitHub repository.

    If the destination already contains the same repository,
    reuse it.

    If the destination contains a different repository,
    create a separate destination instead of deleting the
    existing repository.
    """

    destination = Path(destination)

    # ---------------------------------------------------------
    # CASE 1: Destination does not exist
    # ---------------------------------------------------------

    if not destination.exists():

        print("Cloning repository...")

        subprocess.run(
            [
                "git",
                "clone",
                repo_url,
                str(destination)
            ],
            check=True
        )

        print("Repository cloned successfully!")

        return destination

    # ---------------------------------------------------------
    # CASE 2: Destination already contains a repository
    # ---------------------------------------------------------

    existing_remote = get_existing_remote(destination)

    if existing_remote:

        if normalize_repo_url(existing_remote) == normalize_repo_url(repo_url):

            print("Repository already exists.")

            return destination

        # Different repository already exists.
        # Create a new directory instead of deleting anything.

        repository_name = get_repository_name(repo_url)

        new_destination = destination.parent / (
            f"{destination.name}_{repository_name}"
        )

        counter = 2

        while new_destination.exists():

            new_destination = destination.parent / (
                f"{destination.name}_{repository_name}_{counter}"
            )

            counter += 1

        print(
            "Different repository already exists at the requested "
            "destination."
        )

        print(
            f"Using new destination: {new_destination}"
        )

        print("Cloning repository...")

        subprocess.run(
            [
                "git",
                "clone",
                repo_url,
                str(new_destination)
            ],
            check=True
        )

        print("Repository cloned successfully!")

        return new_destination

    # ---------------------------------------------------------
    # CASE 3: Destination exists but is not a Git repository
    # ---------------------------------------------------------

    repository_name = get_repository_name(repo_url)

    new_destination = destination.parent / (
        f"{destination.name}_{repository_name}"
    )

    counter = 2

    while new_destination.exists():

        new_destination = destination.parent / (
            f"{destination.name}_{repository_name}_{counter}"
        )

        counter += 1

    print(
        "Destination exists but is not a Git repository."
    )

    print(
        f"Using new destination: {new_destination}"
    )

    print("Cloning repository...")

    subprocess.run(
        [
            "git",
            "clone",
            repo_url,
            str(new_destination)
        ],
        check=True
    )

    print("Repository cloned successfully!")

    return new_destination