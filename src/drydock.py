import cli_args
from argparse import Namespace
from config import Config

config = Config.get()


def entrypoint(args: Namespace = None) -> None:

    if args is None:
        # parse the cli args
        args = cli_args.parse_cli_args()
        # update the global config with args
        config.add_args_to_config(args)

    print(config)

# execute the entrypoint
entrypoint()
