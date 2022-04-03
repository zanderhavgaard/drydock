import sys
import docker
from rich.logging import RichHandler
import config
import docker_utils
from model import Run, Container, Task
import console

console = console.default_console


def execute_run(run: Run) -> bool:
    console.print(f"Executing run: {run.name}")

    for index, container in enumerate(run.containers):
        console.rule(f"Container {index + 1} / {len(run.containers)} in run.")
        execute_container(container)


def execute_container(container: Container) -> bool:

    console.print(f"Name:  {container.name}")
    console.print(f"Image: {container.image}")
    console.print(f"Tasks: {len(container.tasks)}")

    # start container to run tasks in
    docker_container = docker_utils.run_container(container.image)

    # execute each task
    for index, task in enumerate(container.tasks):
        console.rule(f"Task {index + 1} / {len(container.tasks)}: {task.name}")
        #  task.execute_task(docker_container)
        execute_task(task, docker_container)
        console.rule()

    # stop container after running all tasks
    docker_utils.stop_container(docker_container)


def execute_task(task: Task, container: docker.models.containers.Container) -> bool:
    console.print(f"Name:    {task.name}")
    console.print(f"type:    {task.type}")
    console.print(f"Command: {task.command}")

    task.execute(container)
