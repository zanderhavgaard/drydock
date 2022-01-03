"""
Provides global configuration
"""
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
        print("foo")

        # which CI platform format to parse pipeline files with
        self.platform = ""

        # which pipeline file to operate on
        self.filename = ""

    def add_args_to_config(self, args: Namespace) -> None:

        if args.platform:
            self.platform = args.platform

        if args.filename:
            self.filename = args.filename
