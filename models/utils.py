import functools
from typing import Optional, Any, List, Union, Iterable
from copy import copy
import numpy as np


def log(**kwargs):
    def decorator(f):
        return Log(f, **kwargs)
    return decorator


class Log:
    def __init__(self, f, batch: bool, progress_bar: Optional[Any] = None, max_num_queries: Optional[int] = None,
                 args_to_dict: bool = False):
        self.f = f
        self.batch = batch
        self.progress_bar = progress_bar
        self.max_num_queries = max_num_queries
        self.args_to_dict = args_to_dict
        self.count = 0
        self.X = []
        self.Y = []
        functools.update_wrapper(self, f)

    def __call__(self, x: Union[float, Iterable, dict]):
        x = copy(x)
        if self.args_to_dict:
            assert isinstance(x, dict)
            _x = []
            for i in range(1, len(x) + 1):
                _x.append(x[f'x{i}'])
            x = _x

        if isinstance(x, np.ndarray):
            x = x.tolist()

        def evaluate(_x, container: List[Any]):
            if (self.max_num_queries is not None) and self.max_num_queries == self.count:
                raise StopModel()

            _y = self.f(_x)
            self.X.append(_x)
            self.Y.append(_y)
            container.append(_y)
            if self.progress_bar is not None:
                self.progress_bar.update(1)
            self.count += 1

        y = []
        if self.batch:
            for _x in x:
                evaluate(_x, y)
        else:
            evaluate(x, y)
            y = y[0]
        return y


class StopModel(Exception):
    pass