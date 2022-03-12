"""
Provides global configuration
"""
from argparse import Namespace

# whether to print the banner when starting
PRINT_BANNER = True

# which CI platform format to parse pipeline files with
PLATFORM = ""

# supported pipeline platforms
SUPPORTED_PLATFORMS = ["githubactions"]

# which pipeline file to operate on
FILENAME = ""


def add_args_to_config(args: Namespace) -> None:

    global PLATFORM, FILENAME

    if args.platform:
        PLATFORM = args.platform

    if args.filename:
        FILENAME = args.filename
