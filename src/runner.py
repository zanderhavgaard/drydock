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
        rule_text = f"Container {index + 1} / {len(run.containers)}"
        console.rule(rule_text, style="blue", align="center")
        execute_container(container)
        console.rule(style="blue")


def execute_container(container: Container) -> bool:

    console.print(f"Name:  {container.name}")
    console.print(f"Image: {container.image}")
    console.print(f"Tasks: {len(container.tasks)}")

    # start container to run tasks in
    docker_container = docker_utils.run_container(container.image)

    # execute each task
    for index, task in enumerate(container.tasks):
        rule_text = f"Task {index + 1} / {len(container.tasks)}: {task.name}"
        console.rule(rule_text, style="cyan", align="center")
        #  task.execute_task(docker_container)
        execute_success = execute_task(task, docker_container)
        if execute_success:
            console.rule(style="green")
        else:
            console.rule(style="red")

    # stop container after running all tasks
    docker_utils.stop_container(docker_container)


def execute_task(task: Task, container: docker.models.containers.Container) -> bool:
    console.print(f"Name:    {task.name}")
    console.print(f"type:    {task.type}")
    console.print(f"Command: {task.command}")

    task_success = task.execute(container)

    return task_success
