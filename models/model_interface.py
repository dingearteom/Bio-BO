from abc import abstractmethod
import abc
from typing import Tuple, Optional
import tqdm
import tqdm.notebook


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

    def set_progress_bar(self, num_evaluations, notebook, verbose, progress_bar):
        self.progress_bar = progress_bar

        if verbose:
            if progress_bar is not None:
                self.progress_bar = progress_bar
            elif notebook:
                self.progress_bar = tqdm.notebook.tqdm(total=num_evaluations, desc=self.get_model_name())
            else:
                self.progress_bar = tqdm.tqdm(total=num_evaluations, desc=self.get_model_name())
