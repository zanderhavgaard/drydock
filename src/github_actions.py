import yaml
from model import Run
from abstract_importer import AbstractImporter
from config import Config
from pprint import pprint

config = Config.get()


class GithubActionsImporter(AbstractImporter):
    def load_pipeline_file(self, file_path: str) -> Run:

        loaded = None

        with open(file_path, "r") as _file:
            loaded = yaml.load(_file, Loader=yaml.FullLoader)

        if loaded is not None:
            return self.create_run_from_pipeline(loaded)
        else:
            raise RuntimeError("There was an error loading the pipeline file.")

    def create_run_from_pipeline(self, pipeline_yaml: dict) -> Run:
        # name of the pipeline / run
        # TODO what should the default name be?
        name = pipeline_yaml["name"] if "name" in pipeline_yaml else "run"

        # list for holding containers of the run
        containers = []

        pprint(pipeline_yaml)

        for key, val in pipeline_yaml["jobs"].items():
            print(key)
            print(val)

        return Run(name=name, containers=containers)
