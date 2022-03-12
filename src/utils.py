from config import Config
from github_actions import GithubActionsImporter
from abstract_importer import AbstractImporter

config = Config.get()


def create_importer() -> AbstractImporter:

    match config.platform:
        case "githubactions":
            return GithubActionsImporter()
        case _:
            print(f"ERROR: {config.platform} is not a supported pipeline platform.")
            print(f"Supported platforms are: {config.supported_platforms}")
            exit(1)
