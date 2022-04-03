import sys
import yaml
import config
from model import Run, Container, Task
from tasks import ShellTask
from abstract_importer import AbstractImporter
import console

console = console.default_console


class GithubActionsImporter(AbstractImporter):
    def import_pipeline_file(self, file_path: str) -> Run:

        imported = None

        with open(file_path, "r") as _file:
            imported = yaml.load(_file, Loader=yaml.FullLoader)

        if imported is not None:
            return self.create_run_from_pipeline_file(imported)
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
                image = "ubuntu:latest"
            else:
                console.print(f"{job['runs-on']} is not a supported runs-on value")
                sys.exit(1)
        else:
            console.print("Could not choose a suitable container image in the following job")
            console.print(job)
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
        return ShellTask(name=name, type=type, command=command)
