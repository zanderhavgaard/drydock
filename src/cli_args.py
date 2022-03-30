import sys
from argparse import ArgumentParser


def parse_cli_args():
    description = "Run CI pipelines locally in docker containers"
    epilog = "By @zanderhavgaard ~ github.com/zanderhavgaard/drydock"
    # create the main parser
    parser = ArgumentParser(description=description, epilog=epilog)
    # create arguments
    #  parser.add_argument("--dryrun", action="store_true", default=False, help="Perform a dryrun")
    #  parser.add_argument("--debug", action="store_true", default=False, help="Enable debug features")
    #  parser.add_argument("--verbose", action="store_true", default=False, help="Enable more verbose prints")

    parser.add_argument(
        "--platform",
        action="store",
        dest="platform",
        type=str,
        help="The CI platform format to use to parse the pipeline file",
    )
    parser.add_argument("--file", action="store", dest="filename", type=str, help="The .yaml CI pipeline file to run")

    args = parser.parse_args()

    # if no subcommand is specified, print help
    if args.platform is None:
        parser.print_help()
        sys.exit(0)
    if args.filename is None:
        parser.print_help()
        sys.exit(0)

    # actually parse the arguments
    return parser.parse_args()
