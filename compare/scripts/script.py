import os
from pathlib import Path
import sys
os.chdir(str(Path(os.path.realpath(__file__)).parent))
path = Path(os.path.realpath(__file__)).parent.parent.parent
del sys.path[0]
sys.path.insert(0, str(path))

import json
import random
import tqdm
from tqdm_multiprocess import TqdmMultiProcessPool
import numpy as np
from datetime import datetime
from compare.scripts.write_log import write_log
from models.Bayesian_Optimization import BayesianOptimization
from models.Gadma import Gadma
from models.bo_torch import BoTorch

model_name_to_class = {'GPyOpt': BayesianOptimization, 'Gadma': Gadma, 'BoTorch': BoTorch}


def error_callback(result):
    print("Error!")


def done_callback(result):
    pass


with open('models_to_run.json', 'r') as file:
    models_to_run = json.load(file)

    for (model_name, objective_name, num_run, num_evaluations, model_num, model_kwargs) in models_to_run:
        model_class = model_name_to_class[model_name]

        def run_model(tqdm_func, global_tqdm):
            seed = random.randrange(int(1e7))
            np.random.seed(seed)
            global num_evaluations, objective_name, model_kwargs
            model = model_class(num_evaluations=num_evaluations, objective_name=objective_name,
                                progress_bar=global_tqdm, model_kwargs=model_kwargs)
            return model.run()

        process_count = 6
        pool = TqdmMultiProcessPool(process_count)

        initial_tasks = [(run_model, tuple()) for i in range(num_run)]

        total_iterations = num_run * num_evaluations

        start_time = datetime.now()

        desc = f'{model_name}_{objective_name}_{num_evaluations}_{model_num}_{model_kwargs}'
        with tqdm.tqdm(total=total_iterations, dynamic_ncols=True, desc=desc) as global_progress:
            results = pool.map(global_progress, initial_tasks, error_callback, done_callback)

        time_of_execution = datetime.now() - start_time

        write_log(results, model_name, objective_name, num_run, num_evaluations,
                  model_num, model_kwargs, time_of_execution)


