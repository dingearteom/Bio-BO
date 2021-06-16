import shutil

from models.model_interface import ModelInterface
from typing import Optional, Tuple
import deminf_data
from ConfigSpace.hyperparameters import UniformFloatHyperparameter
from smac.configspace import ConfigurationSpace
from smac.facade.smac_bo_facade import SMAC4BO
from smac.scenario.scenario import Scenario
import functools
from models.utils import log
import numpy as np


class SMAC(ModelInterface):
    def __init__(self, num_evaluations: int, objective_name: str, notebook: bool = True,
                 verbose: bool = False, progress_bar=None, model_kwargs: Optional[dict] = None):
        self.f = deminf_data.Objective.from_name(objective_name, negate=True, type_of_transform='logarithm')
        self.num_evaluations = num_evaluations

        cs = ConfigurationSpace()
        for i, (l, r) in enumerate(zip(self.f.lower_bound, self.f.upper_bound), start=1):
            cs.add_hyperparameter(UniformFloatHyperparameter(f'x{i}', l, r, default_value=(l + r) / 2))

        self.set_progress_bar(num_evaluations, notebook, verbose, progress_bar)

        scenario = Scenario({"run_obj": "quality",
                             "runcount-limit": num_evaluations,
                             "cs": cs,
                             "deterministic": "true"
                             })

        log_kwargs = {'batch': False, 'args_to_dict': True,
                      'keys': [f'x{i}' for i in range(1, len(self.f.lower_bound) + 1)]}
        if progress_bar is not None:
            log_kwargs['progress_bar'] = self.progress_bar
        self.f = log(**log_kwargs)(self.f)

        self.model = SMAC4BO(scenario=scenario,
                             rng=np.random.RandomState(42),
                             tae_runner=self.f)

    def run(self) -> Tuple[list, list]:
        self.model.optimize()
        shutil.rmtree(self.model.output_dir.split('/')[0])
        return self.f.X, self.f.Y

    def get_model_kwargs(self) -> dict:
        return {}

    def get_num_evaluations(self) -> int:
        return self.num_evaluations

    @staticmethod
    def get_model_name():
        return "SMAC"

