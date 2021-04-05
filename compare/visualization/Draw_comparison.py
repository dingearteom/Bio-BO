import pickle
import numpy as np
import math
import matplotlib.pyplot as plt
import os


class DrawComparison:
    def __init__(self, objective_name):
        self.objective_name = objective_name
        self.BayesianOptimization_data_file_name = f'Y_best_BayesianOptimization_{objective_name}_saved'
        self.GeneticAlgorithm_data_file_name = f'Y_best_Gadma_{objective_name}_saved'

        with open(f'compare/data/Y_best/{self.BayesianOptimization_data_file_name}.pickle', 'rb') as fp:
            Y_best = pickle.load(fp)

        self.num_run = len(Y_best)
        self.num_evaluation = len(Y_best[0])

        with open(f'compare/data/Y_best/{self.GeneticAlgorithm_data_file_name}.pickle', 'rb') as fp:
            Y_best = pickle.load(fp)

        assert self.num_run == len(Y_best) and self.num_evaluation == len(Y_best[0]), 'num_run and num_evaluation ' \
                                                                                      'are not the same for' \
                                                                                      ' BayesianOptimization' \
                                                                                      'and Gadma. BayesianOptimization'

    def draw(self, ax, alpha=0.5, with_trajectories=False):

        self._draw('BayesianOptimization', ax, alpha)
        self._draw('Gadma', ax, alpha)
        if with_trajectories:
            self._draw_trajectories('Gadma', ax, alpha, sep=False)
            self._draw_trajectories('BayesianOptimization', ax, alpha, sep=False)
        ax.legend()

    def _draw(self, model, ax, alpha, color=None):
        if model == 'BayesianOptimization':
            with open(f'compare/data/Y_best/{self.BayesianOptimization_data_file_name}.pickle', 'rb') as fp:
                Y_best = pickle.load(fp)
        elif model == 'Gadma':
            with open(f'compare/data/Y_best/{self.GeneticAlgorithm_data_file_name}.pickle', 'rb') as fp:
                Y_best = pickle.load(fp)

        num_run = len(Y_best)
        num_evaluation = len(Y_best[0])

        def get_confidence_interval(arr, alpha):
            arr = sorted(arr)
            n = len(arr)
            return arr[int((1 - alpha) / 2) * n], arr[min(math.ceil(((1 + alpha) / 2) * n), n - 1)]

        Y_best = np.array(Y_best)
        Y_best_mean = np.median(Y_best, axis=0)

        Y_best_range_low = []
        Y_best_range_high = []
        for i in range(num_evaluation):
            low, high = get_confidence_interval(Y_best[:, i].flatten(), alpha=alpha)
            Y_best_range_low.append(low)
            Y_best_range_high.append(high)

        if color is None:
            color = ('blue' if model == 'Gadma' else 'orange')
        ax.plot(range(1, num_evaluation + 1), Y_best_mean,
                 label=f'{model}', color=color)
        ax.fill_between(range(1, num_evaluation + 1),
                         Y_best_range_low,
                         Y_best_range_high, alpha=0.2, color=color)

    def draw_trajectories(self, model, ax, alpha=0.5):
        '''

        :param model: string, Gadma or BayesianOptimization
        :return:
        '''
        self._draw_trajectories(model, ax, alpha, True)

    def _draw_trajectories(self, model, ax, alpha, sep):
        assert model == 'Gadma' or model == 'BayesianOptimization', f'Unknown model name {model}. ' \
                                                                    f'Only Gadma or BayesianOptimization are allowed'

        log_dir = f'compare/data/{model}_log/{self.objective_name}'

        if sep:
            self._draw(model, ax, alpha, 'red')

        for i in range(1, self.num_run + 1):
            with open(f'{log_dir}/log_{i}.pickle', 'rb') as fp:
                X = pickle.load(fp)
                Y = pickle.load(fp)
                Y_best = pickle.load(fp)
                Y_best = Y_best[:self.num_evaluation]
                color = ('blue' if model == 'Gadma' else 'orange')
                ax.plot(range(1, self.num_evaluation + 1), Y_best, color=color, alpha=0.1)
        ax.legend()


