import docker
from model import Container, Task
import docker_utils
import console

console = console.default_console


class ShellTask(Task):
    def __init__(self, name: str, type: str, command: str) -> None:
        super().__init__(name, type, command)

    def execute(self, container: docker.models.containers.Container) -> bool:

        docker_utils.exec_in_container(container, self.command)
