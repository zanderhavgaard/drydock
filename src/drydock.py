import logging
from argparse import Namespace
from rich.logging import RichHandler
import cli_args
import utils
import config

# setup logging
logging.basicConfig(format="%(message)s", datefmt="[%X]", level=config.LOG_LEVEL, handlers=[RichHandler()])
log = logging.getLogger("rich")


def entrypoint(args: Namespace = None) -> None:

    if config.PRINT_BANNER:
        utils.print_banner()

    log.info("Starting drydock.")

    if args is None:
        log.debug("Parsing cli args")
        # parse the cli args
        args = cli_args.parse_cli_args()
        # update the global config with args
        config.add_args_to_config(args)

    # create importer based on config
    importer = utils.create_importer()

    # create a run from a pipeline file
    run = importer.import_pipeline_file(config.FILENAME)

    # execute taks in containers for the run
    run.execute_run()

    print("sanity")

    #  docker_utils.run_test_container()


# execute the entrypoint
entrypoint()
