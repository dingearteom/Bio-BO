import dash_core_components as dcc
import dash_html_components as html
from compare.visualization.dash_server.layouts.common_layout import Menu

menu = Menu('trajectories')

trajectories_layout = html.Div(
    children=[
        html.Div('Trajectories Graph', className='graph-title'),
        html.Div(
            id='trajectories-graph-plus-menu',
            children=[
                dcc.Graph(
                    id='trajectories-graph'
                ),
                html.Div(
                    children=[
                        html.Div(
                            id='trajectories-menu',
                            children=[
                                menu.get_objective_name_menu(add_class_name=True),
                                menu.get_model_name_menu(),
                                menu.get_num_evaluations_menu(),
                                menu.get_model_num_menu()
                            ]
                        ),
                        html.Button('draw', n_clicks=0, id='button-draw-trajectories')
                    ]
                )
            ]
        )
    ]
)