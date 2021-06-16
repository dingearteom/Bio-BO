import abc
from typing import List, Optional, Tuple


class DrawModelInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, objective_name: str, X: List[List], Y: List[List], model_kwargs: Optional[dict] = None):
        pass

    @abc.abstractmethod
    def acquisition(self, X: List[List]) -> List:
        pass

    @abc.abstractmethod
    def predict(self, X: List[List]) -> Tuple[List, List]:
        pass
