import dash_core_components as dcc
import dash_html_components as html
import dash_table
from compare.visualization.dash_server.layouts.common_layout import Menu

menu = Menu('comparison')

comparison_layout = html.Div(
    children=[
        html.Div("Comparison graph", className='graph-title'),
        html.Div(
            id='menu-header-comparison',
            children=[
                menu.get_objective_name_menu(add_class_name=False),
                html.Button('Clear', n_clicks=0, id='button-clear-comparison')
            ]
        ),
        html.Div(
            id='comparison-content',
            children=[
                dcc.Graph(
                    id='comparison-graph'
                ),
                html.Div(
                    children=[
                        html.Div(
                            id='comparison-menu',
                            children=[
                                html.Div(
                                    id='comparison-add-model-dropdowns',
                                    children=[
                                        menu.get_model_name_menu(),
                                        menu.get_num_evaluations_menu(),
                                        menu.get_model_num_menu()
                                    ]
                                ),
                                html.Button('Add', n_clicks=0, id='button-add-comparison')
                            ]
                        ),
                        dash_table.DataTable(
                            id='comparison-table',
                            columns=[{'name': 'model_name', 'id': 'model_name'},
                                     {'name': 'num_evaluations', 'id': 'num_evaluations'},
                                     {'name': 'model_num', 'id': 'model_num'},
                                     {'name': 'color', 'id': 'color'}],
                            data=[],
                            style_header={
                                'fontWeight': 'bold',
                            }
                        )
                    ]
                )
            ]
        )
    ]
)
