from functools import update_wrapper
from models.utils import log, StopModel
from typing import Optional
from models.model_interface import ModelInterface
from gadma import *
import deminf_data
import tqdm
import tqdm.notebook


class Gadma(ModelInterface):
    def __init__(self, num_evaluations: int, objective_name: str, notebook: bool = True,
                 verbose: bool = False, progress_bar=None, model_kwargs: Optional[dict] = None):
        self.num_evaluations = num_evaluations
        self.f = deminf_data.Objective.from_name(objective_name, negate=True, type_of_transform='logarithm')
        variables = []

        for i, (l, r) in enumerate(zip(self.f.lower_bound, self.f.upper_bound)):
            variables.append(ContinuousVariable(f'var{i + 1}', [l, r]))

        self.set_progress_bar(num_evaluations, notebook, verbose, progress_bar)

        log_kwargs = {'batch': False, 'max_num_queries': num_evaluations}
        if self.progress_bar is not None:
            log_kwargs['progress_bar'] = self.progress_bar
        self.f = log(**log_kwargs)(self.f)
        self.opt = get_global_optimizer("Genetic_algorithm")
        self.opt.maximize = False
        self.variables = variables

    def run(self):
        try:
            self.opt.optimize(self.f, self.variables, verbose=False, maxiter=self.num_evaluations)
        except Exception as exc:
            if not isinstance(exc, StopModel):
                raise exc
        return self.f.X, self.f.Y

    def get_model_kwargs(self) -> dict:
        return dict()

    def get_num_evaluations(self) -> int:
        return self.num_evaluations

    @staticmethod
    def get_model_name():
        return "Gadma"





