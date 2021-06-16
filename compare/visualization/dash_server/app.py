import dash
import dash_html_components as html
from compare.visualization.dash_server.layouts.comparison_graph import comparison_layout
from compare.visualization.dash_server.layouts.trajectories_graph import trajectories_layout
from compare.visualization.dash_server.layouts.contour_graph import contour_layout

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Bayesian Optimization"

app.layout = html.Div(
    children=[
        comparison_layout,
        trajectories_layout,
        contour_layout
    ]
)