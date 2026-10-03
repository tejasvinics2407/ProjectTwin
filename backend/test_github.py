from github_ingestion import clone_repository


repo_url = "https://github.com/octocat/Hello-World.git"

destination = "data/repos/Hello-World"

clone_repository(repo_url, destination)