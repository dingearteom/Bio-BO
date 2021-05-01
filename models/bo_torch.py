from model_interface import ModelInterface
from typing import Optional, Tuple, List
from ax import optimize
import deminf_data
from utils import log


class BoTorch(ModelInterface):

    def __init__(self, num_evaluations: int, objective_name: str, notebook: bool = True,
                 verbose: bool = False, progress_bar=None, model_kwargs: Optional[dict] = None):
        self.f = deminf_data.Objective.from_name(objective_name, negate=True, type_of_transform='logarithm')
        self.num_evaluations = num_evaluations
        self.objective_name = objective_name

        self.bounds = []
        for i, (l, r) in enumerate(zip(self.f.lower_bound, self.f.upper_bound), start=1):
            self.bounds.append({'name': f'x{i}', 'type': 'range', 'bounds': [l.item(), r.item()]})

        self.set_progress_bar(num_evaluations, notebook, verbose, progress_bar)

        log_kwargs = {'batch': False, 'args_to_dict': True}
        if progress_bar is not None:
            log_kwargs['progress_bar'] = self.progress_bar
        self.f = log(**log_kwargs)(self.f)

    def run(self) -> Tuple[List, List]:
        optimize(parameters=self.bounds, evaluation_function=self.f, minimize=True, total_trials=self.num_evaluations)
        return self.f.X, self.f.Y

    def get_model_kwargs(self):
        return {}

    @staticmethod
    def get_model_name():
        return "BoTorch"

    def get_num_evaluations(self) -> int:
        return self.num_evaluations




