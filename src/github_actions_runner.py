import sys
import docker
from rich.logging import RichHandler
import config
import docker_utils
from model import Run, Container, Task
import console

console = console.default_console


class GithubActionsRun(Run):
    def __init__(self, name: str, containers: list[Container]) -> None:
        self.name = name
        self.containers = containers

    def execute_run(self) -> bool:

        console.print(f"Executing run: {self.name}")

        for index, container in enumerate(self.containers):
            console.rule(f"Container {index + 1} / {len(self.containers)} in run.")
            container.execute_container()


class GithubActionsContainer(Container):
    def __init__(self, name: str, image: str, tasks: list[Task]) -> None:
        self.name = name
        self.image = image
        self.tasks = tasks

    def execute_container(self) -> bool:

        console.print(f"Executing container: {self.name}")
        console.print(f"Container image: {self.image}")
        console.print(f"Container will execute {len(self.tasks)} tasks")

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
        console.print(f"task: {self.name}")

        docker_utils.exec_in_container(container, self.command)
