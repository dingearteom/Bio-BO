import dash_core_components as dcc
import dash_html_components as html
import dash_table
from compare.visualization.dash_server.layouts.common_layout import Menu

menu = Menu('contour')

contour_layout = html.Div(
    children=[
        html.Div(children='Contour plot', className='graph-title'),
        html.Div(
            id='contour-main',
            children=[
                html.Div(
                    children=[
                        html.Div(
                            id='contour-menu',
                            children=[
                                menu.get_objective_name_menu(add_class_name=True),
                                menu.get_model_name_menu(),
                                menu.get_num_evaluations_menu(),
                                menu.get_model_num_menu(),
                                menu.get_num_run_menu()
                            ]
                        ),
                        html.Button('draw', n_clicks=0, id='button-draw-contour')
                    ]
                ),
                html.Div(
                    id='contour-plots',
                    children=[
                        html.Div(
                            children=[
                                html.Div(children='Mean', className='plot-title'),
                                dcc.Graph(
                                    id='contour-mean-plot'
                                )
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(children='Std', className='plot-title'),
                                dcc.Graph(
                                    id='contour-std-plot'
                                )
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(children='Acquisition', className='plot-title'),
                                dcc.Graph(
                                    id='contour-acquisition-plot'
                                )
                            ]
                        )
                    ]
                ),
                dash_table.DataTable(
                    id='contour-bottom-menu',
                    style_cell={}
                )
            ]
        )
    ]
)