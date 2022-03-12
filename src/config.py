"""
Provides global configuration
"""
from sys import exit
from argparse import Namespace


class Config:

    # only one config object allowed
    _instance = None

    @staticmethod
    def get():
        if Config._instance is None:
            Config()
        return Config._instance

    def __init__(self) -> None:
        if Config._instance is None:
            self.populate_configs()
            Config._instance = self
        else:
            # This should never happen.
            raise RuntimeError("Only one config object allowed.")

    def populate_configs(self) -> None:

        # which CI platform format to parse pipeline files with
        self.platform = ""

        # supported pipeline platforms
        self.supported_platforms = ["githubactions"]

        # which pipeline file to operate on
        self.filename = ""

    def add_args_to_config(self, args: Namespace) -> None:

        if args.platform:
            self.platform = args.platform

        if args.filename:
            self.filename = args.filename
