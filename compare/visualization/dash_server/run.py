from compare.visualization.dash_server.app import app
from compare.visualization.dash_server.call_backs.trajectories_call_backs import activate_trajectories_callbacks
from compare.visualization.dash_server.call_backs.comparison_call_backs import activate_comparison_callbacks
from compare.visualization.dash_server.call_backs.contour_call_backs import activate_contour_callbacks


if __name__ == '__main__':
    activate_comparison_callbacks()
    activate_trajectories_callbacks()
    activate_contour_callbacks()
    app.run_server(debug=True)