from models.model_interface import ModelInterface
import GPyOpt
from typing import Tuple
import deminf_data
from tqdm.notebook import tqdm
from models.error import StopModel


class BayesianOptimization(ModelInterface):

    def __init__(self, total, progress_bar=None, verbose=True):
        self.num_iter = total
        objective1 = deminf_data.Objective.from_name('1_Bot_4_Sim', negate=True, type_of_transform='logarithm')
        bounds = []
        for i, (l, r) in enumerate(zip(objective1.lower_bound, objective1.upper_bound), start=1):
            bounds.append({'name': f'var_{i}', 'type': 'continuous', 'domain': (l, r)})

        def f(x):
            x = x.copy()
            Y = []
            for point in x:
                f.count += 1
                f.X.append(point)
                y = objective1(point)
                if len(f.Y_best) == 0:
                    f.Y_best.append(y)
                else:
                    f.Y_best.append(min(f.Y_best[-1], y))

                if verbose:
                    f.progress_bar.update(1)
                Y.append(y)
            return Y

        f.count = 0
        f.X = []
        f.Y_best = []
        if verbose:
            if progress_bar is not None:
                f.progress_bar = progress_bar
            else:
                f.progress_bar = tqdm(total=total, desc='BayesianOptimization')
        self.f = f
        self.model = GPyOpt.methods.BayesianOptimization(f=f,
                                                         domain=bounds,
                                                         model_type='GP',
                                                         acquisition_type='EI',
                                                         normalize_Y=True,
                                                         acquisition_weight=2,
                                                         model_update_interval=1,
                                                         verbosity=True)

    def fit(self) -> Tuple[int, list]:
        self.model.run_optimization(self.num_iter, eps=-1)
        return self.f.count, self.f.Y_best
