import os
import json
from datetime import datetime


def write_log(data, model_name, objective_name, num_run, num_evaluations, model_num, model_kwargs, time_of_execution):
    dir = f'../data/log/{objective_name}/{model_name}'
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir += f'/{num_evaluations}_evaluations'
    if not os.path.exists(dir):
        os.mkdir(dir)

    dir += f"/model{model_num}"
    if not os.path.exists(dir):
        os.mkdir(dir)

    file_path = dir + f'/config.json'
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    with open(file_path, 'w') as file:
        json.dump(model_kwargs, file)

    dir += '/runs'
    if not os.path.exists(dir):
        os.makedirs(dir)

    for i, data_one_run in enumerate(data, start=1):
        file_path = dir + f'/run{i}.json'
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

        with open(file_path, 'w') as file:
            json.dump(data_one_run, file)

    hours, remainder = divmod(time_of_execution.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    path_to_file = '../data/log_runs.txt'
    with open(path_to_file, 'a') as fp:
        fp.write(f'{model_name} {model_num} {objective_name} {num_run}x{num_evaluations}'
                 f' {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} '
                 f'execution_time:{"{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))} \n')







