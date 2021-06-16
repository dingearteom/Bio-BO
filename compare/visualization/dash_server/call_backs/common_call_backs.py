import os
from compare.visualization.dash_server.app import app
from dash.dependencies import Output, Input, State


class Record:
    def __init__(self, graph_name: str):
        self.graph_name = graph_name

    def register_app_callback_num_evaluations(self):
        app.callback(
            [Output(f'{self.graph_name}-num-evaluations', 'value'),
             Output(f'{self.graph_name}-num-evaluations', 'options')],
            [Input(f'{self.graph_name}-model-name', 'value'),
             Input(f'{self.graph_name}-objective-name', 'value')]
        )(suggest_num_evaluations)

    def register_app_callback_model_num(self):
        app.callback(
            [Output(f'{self.graph_name}-model-num', 'value'),
             Output(f'{self.graph_name}-model-num', 'options')],
            [Input(f'{self.graph_name}-num-evaluations', 'value'),
             State(f'{self.graph_name}-objective-name', 'value'),
             State(f'{self.graph_name}-model-name', 'value')]
        )(suggest_model_num)

    def register_app_callback_num_run(self):
        app.callback(
            [Output(f'{self.graph_name}-num-run', 'max'),
             Output(f'{self.graph_name}-num-run', 'placeholder')
             ],
            [Input(f'{self.graph_name}-model-num', 'value'),
             State(f'{self.graph_name}-objective-name', 'value'),
             State(f'{self.graph_name}-model-name', 'value'),
             State(f'{self.graph_name}-num-evaluations', 'value')]
        )(suggest_num_run)


def suggest_num_evaluations(model_name, objective_name):
    path = f'../../data/log/{objective_name}/{model_name}'
    options = []
    values = []
    none_output = ['none', [{'label': 'none', 'value': 'none'}]]
    if not os.path.exists(path):
        return none_output
    for name in os.listdir(path):
        assert name[-12:] == '_evaluations'
        values.append(int(name[:-12]))
    values = sorted(values)
    for value in values:
        options.append({'label': value, 'value': value})
    if len(values) == 0:
        return none_output
    return [values[0], options]


def suggest_model_num(num_evaluations, objective_name, model_name):
    path = f'../../data/log/{objective_name}/{model_name}/{num_evaluations}_evaluations'
    options = []
    values = []
    none_output = ['none', [{'label': 'none', 'value': 'none'}]]
    if not os.path.exists(path):
        return none_output
    for name in os.listdir(path):
        if os.path.isdir(f'{path}/{name}'):
            assert name[:5] == 'model'
            values.append(int(name[5:]))
    values = sorted(values)
    for value in values:
        options.append({'label': value, 'value': value})
    if len(values) == 0:
        return none_output
    return [values[0], options]


def suggest_num_run(model_num, objective_name, model_name, num_evaluations):
    path = f'../../data/log/{objective_name}/{model_name}/{num_evaluations}_evaluations/model{model_num}/runs'

    max_run = 0
    for name in os.listdir(path):
        assert name[:3] == 'run'
        max_run = max(max_run, int(name[3:-5]))

    return [max_run, f'Max Value: {max_run}']
