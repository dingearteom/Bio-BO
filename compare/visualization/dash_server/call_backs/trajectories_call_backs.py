from compare.visualization.dash_server.app import app
from dash.dependencies import Output, Input, State
from compare.visualization.dash_server.call_backs.common_call_backs import Record
import plotly.graph_objects as go
import json
import os


def activate_trajectories_callbacks():
    record = Record('trajectories')
    record.register_app_callback_num_evaluations()
    record.register_app_callback_model_num()

    @app.callback(
        Output('trajectories-graph', 'figure'),
        [Input('button-draw-trajectories', 'n_clicks'),
         State('trajectories-objective-name', 'value'),
         State('trajectories-model-name', 'value'),
         State('trajectories-num-evaluations', 'value'),
         State('trajectories-model-num', 'value')]
    )
    def update_trajectories_graph(n_clicks, objective_name, model_name, num_evaluations, model_num):
        fig = go.Figure(layout=go.Layout(height=700))
        if n_clicks == 0:
            return fig

        dir = f'../../data/log/{objective_name}/{model_name}/{num_evaluations}_evaluations/model{model_num}/runs'
        for run_name in os.listdir(dir):
            with open(f'{dir}/{run_name}', 'r') as file:
                x, y = json.load(file)
            y_best = []
            for _y in y:
                if len(y_best) != 0:
                    y_best.append(min(_y, y_best[-1]))
                else:
                    y_best.append(_y)
            fig.add_trace(go.Scatter(x=list(range(1, num_evaluations + 1)),
                                     y=y_best,
                                     mode='lines',
                                     line={'color':'orange'},
                                     name=f'{run_name[:-5]}'))
        return fig


