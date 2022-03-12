import cli_args
from argparse import Namespace
from config import Config
import docker_utils
import abstract_importer
import utils

config = Config.get()


def entrypoint(args: Namespace = None) -> None:

    if args is None:
        # parse the cli args
        args = cli_args.parse_cli_args()
        # update the global config with args
        config.add_args_to_config(args)

    # create importer based on config
    importer = utils.create_importer()

    # create a run from a pipeline file
    run = importer.load_pipeline_file(config.filename)

    # execute taks in containers for the run
    run.execute()

    #  docker_utils.run_test_container()


# execute the entrypoint
entrypoint()
