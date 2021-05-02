import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

comparison_layout = html.Div(
    children=[
        html.Div("Comparison graph", className='graph-title'),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children='Objective name', className='menu-title'),
                        dcc.Dropdown(
                            id='comparison-objective-name',
                            value='1_Bot_4_Sim',
                            options=[{'label': '1_Bot_4_Sim', 'value': '1_Bot_4_Sim'},
                                     {'label': '2_ExpDivNoMig_5_Sim', 'value': '2_ExpDivNoMig_5_Sim'},
                                     {'label': '2_DivMig_5_Sim', 'value': '2_DivMig_5_Sim'}],
                            clearable=False
                        )
                    ],
                ),
                html.Button('Clear', n_clicks=0, id='button-clear-comparison')
            ],
            className='menu-header-comparison'
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
                            id='comparison-add-model-menu',
                            children=[
                                html.Div(
                                    id='comparison-add-model-dropdowns',
                                    children=[
                                        html.Div(
                                            className='comparison-add-model-dropdown',
                                            children=[
                                                html.Div(children='model name', className='menu-title'),
                                                dcc.Dropdown(
                                                    id='comparison-model-name',
                                                    value='BoTorch',
                                                    options=[{'label': 'BoTorch', 'value': 'BoTorch'},
                                                             {'label': 'GPyOpt', 'value': 'GPyOpt'},
                                                             {'label': 'Gadma', 'value': 'Gadma'}]
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className='comparison-add-model-dropdown',
                                            children=[
                                                html.Div(children='num evaluations', className='menu-title'),
                                                dcc.Dropdown(
                                                    id='comparison-num-evaluations'
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className='comparison-add-model-dropdown',
                                            children=[
                                                html.Div(children='model num', className='menu-title'),
                                                dcc.Dropdown(
                                                    id='comparison-model-num'
                                                )
                                            ]
                                        )
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
