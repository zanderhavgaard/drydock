import sys
import logging
import docker
import docker_utils
import config
from rich.logging import RichHandler
from model import Run, Container, Task

# setup logging
logging.basicConfig(format="%(message)s", datefmt="[%X]", level=config.LOG_LEVEL, handlers=[RichHandler()])
log = logging.getLogger("rich")


class GithubActionsRun(Run):
    def __init__(self, name: str, containers: list[Container]) -> None:
        self.name = name
        self.containers = containers

    def execute_run(self) -> bool:

        log.info(f"Executing run: {self.name}")

        for index, container in enumerate(self.containers):
            log.info("---")
            log.info(f"Container {index + 1} / {len(self.containers)} in run.")
            container.execute_container()


class GithubActionsContainer(Container):
    def __init__(self, name: str, image: str, tasks: list[Task]) -> None:
        self.name = name
        self.image = image
        self.tasks = tasks

    def execute_container(self) -> bool:

        log.info(f"Executing container: {self.name}")
        log.info(f"Container image: {self.image}")
        log.info(f"Container will execute {len(self.tasks)} tasks")

        # start container to run tasks in
        container = docker_utils.run_container(self.image)

        # execute each task
        for task in self.tasks:
            task.execute_task(container)

        # stop container after running all tasks
        docker_utils.stop_container(container)


class GithubActionsTask(Task):
    def __init__(self, name: str, type: str, command: str) -> None:
        self.name = name
        self.type = type
        self.command = command

    def execute_task(self, container: docker.models.containers.Container) -> bool:
        print(f"task: {self.name}")

        docker_utils.exec_in_container(container, self.command)
