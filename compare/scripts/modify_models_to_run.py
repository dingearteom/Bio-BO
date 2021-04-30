import argparse
import json

objective_names = ['1_Bot_4_Sim', '2_ExpDivNoMig_5_Sim', '2_DivMig_5_Sim']

parser = argparse.ArgumentParser('Modifies models to run.')
parser.add_argument('model_name', nargs='?')
parser.add_argument('objective_name', nargs='?')
parser.add_argument('num_run', nargs='?', type=int)
parser.add_argument('num_evaluations', nargs='?', type=int)
parser.add_argument('model_num', nargs='?', type=int)
parser.add_argument('--clear', action='store_true')
parser.add_argument('--model_kwargs', default='{}')

args = parser.parse_args()

if args.clear:
    with open('models_to_run.json', 'w') as file:
        json.dump([], file)
else:
    objective_name = \
        (args.objective_name if not args.objective_name.isnumeric() else objective_names[int(args.objective_name) - 1])
    model_kwargs = (args.model_kwargs if hasattr(args, 'model_kwargs') else '{}')
    data = [args.model_name, objective_name, args.num_run, args.num_evaluations,
            args.model_num, json.loads(model_kwargs)]
    with open('models_to_run.json', 'r') as file:
        models_to_run = json.load(file)
    models_to_run.append(data)
    with open('models_to_run.json', 'w') as file:
        json.dump(models_to_run, file)