import pyfiglet
import logging
import config
from rich import print
from abstract_importer import AbstractImporter
from github_actions import GithubActionsImporter

# setup logging
log = logging.getLogger("rich")


def print_banner() -> None:
    banner = pyfiglet.figlet_format("drydock", font="slant")
    print(f"[magenta]{banner}[/magenta]")
    print(f"[blue]~ https://github.com/zanderhavgaard/drydock[/blue]")
    print(f"[cyan]-------------------------------------------[/cyan]")


def create_importer() -> AbstractImporter:

    # shiny new python pattern matching
    match config.PLATFORM:
        case "githubactions":
            return GithubActionsImporter()
        # default case
        case _:
            log.error(f"{config.platform} is not a supported pipeline platform.")
            log.error(f"Supported platforms are: {config.supported_platforms}")
            log.critical("EXITING with code 1")
            exit(1)
