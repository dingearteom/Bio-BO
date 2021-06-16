from compare.visualization.dash_server.call_backs.common_call_backs import Record
from compare.visualization.dash_server.app import app
from dash.dependencies import Output, Input, State
import deminf_data
import dash_core_components as dcc
import dash_html_components as html


def activate_contour_callbacks():
    record = Record('contour')
    record.register_app_callback_num_evaluations()
    record.register_app_callback_model_num()
    record.register_app_callback_num_run()

    @app.callback(
        [Output('contour-bottom-menu', 'columns'),
         Output('contour-bottom-menu', 'data'),
         Output('contour-bottom-menu', 'style_header_conditional')],
        [Input('button-draw-contour', 'n_clicks'),
         State('contour-objective-name', 'value')]
    )
    def add_bottom_menu(n_clicks, objective_name):
        f = deminf_data.Objective.from_name(objective_name, negate=True, type_of_transform='logarithm')
        columns = [{'name': f'x{i}', 'id': f'x{i}'}
                   for i in range(1, len(f.lower_bound) + 1)]
        style = [
            {
                'if': {
                    'column_id': 'x1'
                },
                'backgroundColor': 'green'
            },
            {
                'if': {
                    'column_id': 'x2'
                },
                'backgroundColor': 'green'
            },
        ]

        data = [row1, row2]
        return [columns, data, style]
