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

# whether to remove container after run
REMOVE_CONTAINER = True

# stream output from each task
STREAM_EXEC_OUTPUT = True


def add_args_to_config(args: Namespace) -> None:

    global PLATFORM, FILENAME

    if args.platform:
        PLATFORM = args.platform

    if args.filename:
        FILENAME = args.filename
