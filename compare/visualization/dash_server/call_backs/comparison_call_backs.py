from compare.visualization.dash_server.app import app
from dash.dependencies import Output, Input, State
from copy import deepcopy
import os
import matplotlib.colors as mcolors
import plotly.graph_objects as go
import json
import numpy as np
import math
import dash
from compare.visualization.dash_server.call_backs.common_call_backs import Record


def activate_comparison_callbacks():
    record = Record('comparison')
    record.register_app_callback_num_evaluations()
    record.register_app_callback_model_num()

    @app.callback(
        [Output('comparison-table', 'data'),
         Output('comparison-table', 'style_data_conditional')
         ],
        [Input('button-clear-comparison', 'n_clicks'),
         Input('button-add-comparison', 'n_clicks'),
         State('comparison-model-name', 'value'),
         State('comparison-num-evaluations', 'value'),
         State('comparison-model-num', 'value'),
         State('comparison-table', 'data'),
         State('comparison-table', 'style_data_conditional')]
    )
    def update_table(n_clicks_clear, n_clicks, model_name, num_evaluations, model_num, data, style):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'button-clear-comparison' in changed_id:
            return [[], []]

        if n_clicks == 0:
            return [data, style]
        data = deepcopy(data)
        style = deepcopy(style)

        if style is None:
            style = []

        data.append({'model_name': model_name, 'num_evaluations': num_evaluations, 'model_num': model_num, 'color': ''})
        colors = list(mcolors.TABLEAU_COLORS.values())
        style.append(
            {
                'if': {
                    'row_index': len(data) - 1,
                    'column_id': 'color'
                },
                'backgroundColor': colors[len(data) - 1]
            }
        )

        return [data, style]

    @app.callback(
        Output('comparison-graph', 'figure'),
        [Input('button-clear-comparison', 'n_clicks'),
         Input('comparison-table', 'data'),
         State('comparison-table', 'style_data_conditional'),
         State('comparison-objective-name', 'value')]
    )
    def update_comparison_graph(n_clicks, data, style, objective_name):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        fig = go.Figure(layout=go.Layout(height=700))
        if 'button-clear-comparison' in changed_id:
            return fig
        alpha = 0.5
        min_num_evaluations = None
        for row in data:
            num_evaluations = row['num_evaluations']
            if min_num_evaluations is None or min_num_evaluations > num_evaluations:
                min_num_evaluations = num_evaluations

        for i, row in enumerate(data):
            model_name = row['model_name']
            num_evaluations = row['num_evaluations']
            model_num = row['model_num']
            color = None

            for style_cell in style:
                if style_cell['if']['row_index'] == i:
                    color = style_cell['backgroundColor']
                    break

            dir = f'../../data/log/{objective_name}/{model_name}/{num_evaluations}_evaluations/model{model_num}/runs'

            y_best = []
            for run_name in os.listdir(dir):
                with open(f'{dir}/{run_name}', 'r') as file:
                    _, y = json.load(file)
                _y_best = []
                for _y in y:
                    if len(_y_best) != 0:
                        _y_best.append(min(_y, _y_best[-1]))
                    else:
                        _y_best.append(_y)
                y_best.append(_y_best[:min_num_evaluations])

            num_evaluations = min_num_evaluations
            # for BoTorch
            for j in range(len(y_best)):
                if len(y_best[j]) < num_evaluations:
                    y_best[j] = y_best[j] + [y_best[j][-1]] * (num_evaluations - len(y_best[j]))
            ###

            y_best = np.array(y_best)
            num_run = y_best.shape[0]

            fig.add_trace(go.Scatter(x=list(range(1, num_evaluations + 1)),
                                     y=np.median(y_best, axis=0),
                                     mode='lines',
                                     line={'color': color},
                                     name=model_name))

            y_low = []
            y_high = []
            for evaluation in range(num_evaluations):
                y = sorted(y_best[:, evaluation])
                y_low.append(y[int(((1 - alpha) / 2) * num_run)])
                y_high.append(y[math.ceil(((1 + alpha) / 2) * num_run)])

            fig.add_trace(go.Scatter(x=list(range(1, num_evaluations + 1)) + list(range(num_evaluations, 0, -1)),
                                     y=y_low + y_high[::-1], fill='toself', fillcolor=color, mode='none', opacity=0.5,
                                     name=model_name, hoverinfo='none'))
        return fig



