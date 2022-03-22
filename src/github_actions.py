import sys
import yaml
import logging
from rich.logging import RichHandler
from model import Run, Container, Task
from abstract_importer import AbstractImporter

# setup logging
logging.basicConfig(format="%(message)s", datefmt="[%X]", level=logging.DEBUG, handlers=[RichHandler()])
log = logging.getLogger("rich")


class GithubActionsImporter(AbstractImporter):
    def load_pipeline_file(self, file_path: str) -> Run:

        loaded = None

        with open(file_path, "r") as _file:
            loaded = yaml.load(_file, Loader=yaml.FullLoader)

        if loaded is not None:
            return self.create_run_from_pipeline_file(loaded)
        else:
            raise RuntimeError("There was an error loading the pipeline file.")

    def create_run_from_pipeline_file(self, pipeline_yaml: dict) -> Run:
        # name of the pipeline / run
        # TODO what should the default name be?
        name = pipeline_yaml["name"] if "name" in pipeline_yaml else "run"

        # list for holding containers of the run
        containers = []

        # each GH actions job will be a container
        for job_name, job in pipeline_yaml["jobs"].items():
            container = self.create_container_from_gha_job(job_name, job)
            containers.append(container)

        return Run(name=name, containers=containers)

    def create_container_from_gha_job(self, job_name: str, job: dict) -> Container:

        # the name of container
        name = job_name

        # setup which container image to use
        if "container" in job:
            image = job["container"]
        elif "runs-on" in job:
            if job["runs-on"] == "ubuntu-latest":
                image = "ubuntu"
            else:
                log.error(f"{job['runs-on']} is not a supported runs-on value")
                sys.exit(1)
        else:
            log.error("Could not choose a suitable container image in the following job")
            log.error(job)
            sys.exit(1)

        # setup the tasks for this container

        # list for holding the tasks of this container
        tasks = []

        # each step of a GHA job will be a task
        for step in job["steps"]:
            task = self.create_task_from_gha_step(step)
            tasks.append(task)

        return Container(name=name, image=image, tasks=tasks)

    def create_task_from_gha_step(self, step: dict) -> Task:
        # figure out the name of the task
        if "name" in step:
            name = step["name"]
        else:
            name = step["run"]

        # figure out the type of the task
        # TODO how ot handle different types
        type = "shell"

        # figure out the command to run
        command = step["run"]

        # create task object
        return Task(name=name, type=type, command=command)
