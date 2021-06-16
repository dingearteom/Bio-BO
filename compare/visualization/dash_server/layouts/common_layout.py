import dash_core_components as dcc
import dash_html_components as html


class Menu:
    def __init__(self, graph_name: str):
        self.graph_name = graph_name

    def get_objective_name_menu(self, add_class_name: bool):
        children = [
           html.Div(children='Objective name', className='menu-title'),
           dcc.Dropdown(
               id=f'{self.graph_name}-objective-name',
               value='1_Bot_4_Sim',
               options=[{'label': '1_Bot_4_Sim', 'value': '1_Bot_4_Sim'},
                        {'label': '2_ExpDivNoMig_5_Sim', 'value': '2_ExpDivNoMig_5_Sim'},
                        {'label': '2_DivMig_5_Sim', 'value': '2_DivMig_5_Sim'}],
               clearable=False
           )
        ]
        if add_class_name:
            return html.Div(className=f'{self.graph_name}-dropdown', children=children)
        else:
            return html.Div(children=children)

    def get_model_name_menu(self):
        return html.Div(
            className=f'{self.graph_name}-dropdown',
            children=[
                html.Div(children='model name', className='menu-title'),
                dcc.Dropdown(
                    id=f'{self.graph_name}-model-name',
                    value='BoTorch',
                    options=[{'label': 'BoTorch', 'value': 'BoTorch'},
                             {'label': 'GPyOpt', 'value': 'GPyOpt'},
                             {'label': 'Gadma', 'value': 'Gadma'}]
                )
            ]
        )

    def get_num_evaluations_menu(self):
        return html.Div(
                className=f'{self.graph_name}-dropdown',
                children=[
                    html.Div(children='num evaluations', className='menu-title'),
                    dcc.Dropdown(
                        id=f'{self.graph_name}-num-evaluations'
                    )
                ]
            )

    def get_model_num_menu(self):
        return html.Div(
                className=f'{self.graph_name}-dropdown',
                children=[
                    html.Div(children='model num', className='menu-title'),
                    dcc.Dropdown(
                        id=f'{self.graph_name}-model-num'
                    )
                ]
            )

    def get_num_run_menu(self):
        return html.Div(
            className=f'{self.graph_name}-dropdown',
            children=[
                html.Div(children='num run', className='menu-title'),
                dcc.Input(
                    id=f'{self.graph_name}-num-run',
                    type='number',
                    min=1,
                    step=1
                )
            ],
        )




