from models.model_interface import ModelInterface
import GPyOpt
from typing import Tuple, Optional, List
import deminf_data
import functools
import tqdm
import tqdm.notebook
import numpy as np
from models.utils import log
from models.draw_interface import DrawModelInterface


class BayesianOptimization(ModelInterface):
    def __init__(self, num_evaluations: int, objective_name: str, notebook: bool = True,
                 verbose: bool = False, progress_bar=None, model_kwargs: Optional[dict] = None):
        self.f = deminf_data.Objective.from_name(objective_name, negate=True, type_of_transform='logarithm')
        self.num_evaluations = num_evaluations

        bounds = []
        for i, (l, r) in enumerate(zip(self.f.lower_bound, self.f.upper_bound), start=1):
            bounds.append({'name': f'var_{i}', 'type': 'continuous', 'domain': (l, r)})

        self.set_progress_bar(num_evaluations, notebook, verbose, progress_bar)

        log_kwargs = {'batch': True}
        if progress_bar is not None:
            log_kwargs['progress_bar'] = self.progress_bar
        self.f = log(**log_kwargs)(self.f)

        self.model_default_kwargs = {'model_type': 'GP', 'acquisition_type': 'EI',
                                     'normalize_Y': True, 'initial_design_numdata': 5,
                                     'exact_feval': True}

        if model_kwargs is not None:
            self.model_default_kwargs.update(model_kwargs)

        self.model = GPyOpt.methods.BayesianOptimization(f=self.f, domain=bounds, **self.model_default_kwargs)

    def run(self) -> Tuple[list, list]:
        self.model.run_optimization(self.num_evaluations - self.model_default_kwargs['initial_design_numdata'], eps=-1)
        return self.f.X, self.f.Y

    def get_model_kwargs(self) -> dict:
        return self.model_default_kwargs

    def get_num_evaluations(self) -> int:
        return self.num_evaluations

    @staticmethod
    def get_model_name():
        return "GPyOpt"


class BayesianOptimizationDraw(DrawModelInterface):
    def __init__(self, objective_name: str, X: List[List], Y: List[List], model_kwargs: Optional[dict] = None):
        self.f = deminf_data.Objective.from_name(objective_name, negate=True, type_of_transform='logarithm')

        bounds = []
        for i, (l, r) in enumerate(zip(self.f.lower_bound, self.f.upper_bound), start=1):
            bounds.append({'name': f'var_{i}', 'type': 'continuous', 'domain': (l, r)})

        log_kwargs = {'batch': True}
        self.f = log(**log_kwargs)(self.f)

        self.model_default_kwargs = {'model_type': 'GP', 'acquisition_type': 'EI',
                                     'normalize_Y': True, 'initial_design_numdata': 5,
                                     'exact_feval': True}

        if model_kwargs is not None:
            self.model_default_kwargs.update(model_kwargs)

        self.model = GPyOpt.methods.BayesianOptimization(f=self.f, domain=bounds, X=X, Y=Y, **self.model_default_kwargs)

    def acquisition(self, X: List[List]) -> List:
        return self.model.acquisition(X)

    def predict(self, X: List[List]) -> Tuple[List, List]:
        return self.model.model.predict(X)
