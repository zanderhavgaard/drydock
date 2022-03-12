from abc import ABC, abstractmethod
from model import Run


class AbstractImporter(ABC):
    @abstractmethod
    def load_pipeline_file() -> Run:
        pass
