"""
Classes for holding data loaded from a pipeline
"""
from abc import ABC, abstractmethod


class Task:
    def __init__(name: str, type: str, command: str) -> None:
        pass

    @abstractmethod
    def execute_task(self) -> bool:
        pass


class Container:
    def __init__(name: str, image: str, tasks: list[Task]) -> None:
        pass
    @abstractmethod
    def execute_container(self) -> bool:
        pass


class Run:
    def __init__(name: str, containers: list[Container]) -> None:
        pass

    @abstractmethod
    def execute_run(self) -> bool:
        pass
