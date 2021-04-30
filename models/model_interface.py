from abc import abstractmethod
import abc
from typing import Tuple, Optional


class ModelInterface(metaclass=abc.ABCMeta):

    @abstractmethod
    def __init__(self, num_evaluations: int, objective_name: str, notebook: bool = True,
                 verbose: bool = False, progress_bar=None, model_kwargs: Optional[dict] = None):
        pass

    @abstractmethod
    def run(self) -> Tuple[list, list]:
        pass

    @abstractmethod
    def get_model_kwargs(self):
        pass

    @staticmethod
    def get_model_name():
        raise NotImplemented

    @abstractmethod
    def get_num_evaluations(self) -> int:
        pass
