from argparse import Namespace
import cli_args
import utils
import config
import console

console = console.default_console


def entrypoint(args: Namespace = None) -> None:

    if config.PRINT_BANNER:
        utils.print_banner()

    console.print("Starting drydock.")

    if args is None:
        console.print("Parsing cli args")
        # parse the cli args
        args = cli_args.parse_cli_args()
        # update the global config with args
        config.add_args_to_config(args)

    # create importer based on config
    importer = utils.create_importer()

    # create a run from a pipeline file
    run = importer.import_pipeline_file(config.FILENAME)

    console.rule("Starting run")

    # execute taks in containers for the run
    run.execute_run()

    console.print("sanity")

    #  docker_utils.run_test_container()


# execute the entrypoint
entrypoint()
