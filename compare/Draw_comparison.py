import pickle
import numpy as np
import math
import matplotlib.pyplot as plt
import os


class DrawComparison:
    def __init__(self, BayesianOptimization_data_file_name, GeneticAlgorithm_data_file_name, picture_file_name, real):
        self.BayesianOptimization_data_file_name = BayesianOptimization_data_file_name
        self.GeneticAlgorithm_data_file_name = GeneticAlgorithm_data_file_name
        self.picture_file_name = picture_file_name
        self.real = real

    def draw(self, alpha=0.5):
        with open(f'compare/data/Y_best/{self.BayesianOptimization_data_file_name}.pickle', 'rb') as fp:
            BayesianOptimization_Y_best = pickle.load(fp)
        with open(f'compare/data/Y_best/{self.GeneticAlgorithm_data_file_name}.pickle', 'rb') as fp:
            GeneticAlgorithm_Y_best = pickle.load(fp)

        assert len(BayesianOptimization_Y_best) == len(GeneticAlgorithm_Y_best)
        assert len(BayesianOptimization_Y_best[0]) == len(GeneticAlgorithm_Y_best[0])

        num_run = len(BayesianOptimization_Y_best)
        num_evaluation = len(BayesianOptimization_Y_best[0])

        def get_confidence_interval(arr, alpha):
            arr = sorted(arr)
            n = len(arr)
            return arr[int((1 - alpha) / 2) * n], arr[min(math.ceil(((1 + alpha) / 2) * n), n - 1)]

        GeneticAlgorithm_Y_best = np.array(GeneticAlgorithm_Y_best)
        BayesianOptimization_Y_best = np.array(BayesianOptimization_Y_best)

        GeneticAlgorithm_Y_best_mean = np.mean(GeneticAlgorithm_Y_best, axis=0)
        BayesianOptimization_Y_best_mean = np.mean(BayesianOptimization_Y_best, axis=0)

        GeneticAlgorithm_Y_best_range_low = []
        GeneticAlgorithm_Y_best_range_high = []
        for i in range(num_evaluation):
            low, high = get_confidence_interval(GeneticAlgorithm_Y_best[:, i].flatten(), alpha=alpha)
            GeneticAlgorithm_Y_best_range_low.append(low)
            GeneticAlgorithm_Y_best_range_high.append(high)

        BayesianOptimization_Y_best_range_low = []
        BayesianOptimization_Y_best_range_high = []
        for i in range(num_evaluation):
            low, high = get_confidence_interval(BayesianOptimization_Y_best[:, i].flatten(), alpha=alpha)
            BayesianOptimization_Y_best_range_low.append(low)
            BayesianOptimization_Y_best_range_high.append(high)

        plt.plot(range(1, num_evaluation + 1), GeneticAlgorithm_Y_best_mean, label='GeneticAlgorithm')
        plt.fill_between(range(1, num_evaluation + 1),
                         GeneticAlgorithm_Y_best_range_low, GeneticAlgorithm_Y_best_range_high, alpha=0.2)
        plt.plot(range(1, num_evaluation + 1), BayesianOptimization_Y_best_mean, label='BayesianOptimization')
        plt.fill_between(range(1, num_evaluation + 1),
                         BayesianOptimization_Y_best_range_low, BayesianOptimization_Y_best_range_high, alpha=0.2)
        plt.legend()

        pictures_dir = 'compare/data/pictures'
        if not os.path.exists(pictures_dir):
            os.mkdir(pictures_dir)
        if self.real:
            pictures_dir = 'compare/data/pictures/real'
        else:
            pictures_dir = 'compare/data/pictures/artificial'
        if not os.path.exists(pictures_dir):
            os.mkdir(pictures_dir)
        plt.savefig(f'{pictures_dir}/{self.picture_file_name}.png')
        plt.clf()
