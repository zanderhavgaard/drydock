"""
Classes for holding data loaded from a pipeline
"""


class Task:
    def __init__(self, name: str, type: str, command: str) -> None:
        self.name = name
        self.type = type
        self.command = command


class Container:
    def __init__(self, name: str, image: str, tasks: list[Task]) -> None:
        self.name = name
        self.image = image
        self.tasks = tasks


class Run:
    def __init__(self, name: str, containers: list[Container]) -> None:
        self.name = name
        self.containers = containers
