import deminf_data
from gadma import *
import tqdm
from models.error import StopModel


class Gadma:
    def __init__(self, total, objective_name, progress_bar=None, verbose=True):
        objective = deminf_data.Objective.from_name(objective_name, negate=True, type_of_transform='logarithm')
        variables = []

        for i, (l, r) in enumerate(zip(objective.lower_bound, objective.upper_bound)):
            variables.append(ContinuousVariable(f'var{i + 1}', [l, r]))

        def f(x):
            f.count += 1
            f.X.append(x)
            y = objective(x)
            f.Y.append(y)
            if len(f.Y_best) == 0 or f.Y_best[-1] > y:
                f.Y_best.append(y)
            else:
                f.Y_best.append(f.Y_best[-1])
            if verbose:
                f.progress_bar.update(1)
            if f.count == total:
                raise StopModel('nothing series, just stop of the model')
            return y

        f.count = 0
        f.Y = []
        f.X = []
        f.Y_best = []
        if progress_bar is not None:
            f.progress_bar = progress_bar
        elif verbose:
            f.progress_bar = tqdm.tqdm(total=total, desc='Gadma')

        self.f = f
        self.opt1 = get_global_optimizer("Genetic_algorithm")
        self.opt1.maximize = False
        self.variables = variables
        self.total = total

    def fit(self):
        try:
            self.opt1.optimize(self.f, self.variables, verbose=False, maxiter=self.total)
        except Exception as exc:
            if not isinstance(exc, StopModel):
                raise exc
        return self.f.Y_best
