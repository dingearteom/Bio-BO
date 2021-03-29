import tqdm
from models.Bayesian_Optimization import BayesianOptimization
import pickle
from tqdm_multiprocess import TqdmMultiProcessPool
from multiprocessing import Pool
import random
import numpy as np
import sys
import os

objective_name = str(sys.argv[-3])
num_run = int(sys.argv[-2])
num_evaluation = int(sys.argv[-1])


def error_callback(result):
    print("Error!")


def done_callback(result):
    pass


def run_model(num, objective_name, tqdm_func, global_tqdm):
    seed = random.randrange(10000000)
    np.random.seed(seed)
    global num_evaluation
    model = BayesianOptimization(total=num_evaluation, objective_name=objective_name, progress_bar=global_tqdm)
    _, Y_best = model.fit()
    return Y_best[:num_evaluation]


process_count = 6
pool = TqdmMultiProcessPool(process_count)

initial_tasks = [(run_model, (i, objective_name)) for i in range(num_run)]

total_iterations = num_run * num_evaluation

with tqdm.tqdm(total=total_iterations, dynamic_ncols=True) as global_progress:
    # BayesianOptimization_Y_best = []
    # for i in range(num_run):
    #     BayesianOptimization_Y_best.append(run_model(i, lambda x: x, global_progress))
    BayesianOptimization_Y_best = pool.map(global_progress, initial_tasks, error_callback, done_callback)


path_dir = 'compare/data/Y_best'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

with open(f"compare/data/Y_best/Y_best_BayesianOptimization_{objective_name}_saved.pickle", 'wb') as fp:
    pickle.dump(BayesianOptimization_Y_best, fp)
