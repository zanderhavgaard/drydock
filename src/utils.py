import pyfiglet
import config
from abstract_importer import AbstractImporter
from github_actions_importer import GithubActionsImporter
import console

console = console.default_console


def print_banner() -> None:
    banner = pyfiglet.figlet_format("drydock", font="slant")
    console.print(f"[magenta]{banner}[/magenta]")
    console.print("[blue]~ https://github.com/zanderhavgaard/drydock[/blue]")
    console.print("[cyan]-------------------------------------------[/cyan]")


def create_importer() -> AbstractImporter:

    # shiny new python pattern matching
    match config.PLATFORM:
        case "githubactions":
            return GithubActionsImporter()
        # default case
        case _:
            # TODO how to print errors??
            console.print(f"{config.platform} is not a supported pipeline platform.")
            console.print(f"Supported platforms are: {config.supported_platforms}")
            console.print("EXITING with code 1")
            exit(1)
