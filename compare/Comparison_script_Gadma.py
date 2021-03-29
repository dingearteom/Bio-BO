from models.Gadma import Gadma
import tqdm
import pickle
import sys
import os


objective_name = str(sys.argv[-3])
num_run = int(sys.argv[-2])
num_evaluation = int(sys.argv[-1])

progress_bar_Gadma = tqdm.tqdm(total=num_evaluation * num_run, desc='Gadma')
Gadma_Y_best = []

for i in range(num_run):
    model = Gadma(total=num_evaluation, objective_name=objective_name, progress_bar=progress_bar_Gadma)
    Y_best = model.fit()
    Gadma_Y_best.append(Y_best)

path_dir = 'compare/data/Y_best'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

with open(f"compare/data/Y_best/Y_best_Gadma_{objective_name}_saved.pickle", "wb") as fp:
    pickle.dump(Gadma_Y_best, fp)